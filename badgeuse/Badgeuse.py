import os
import sys
import signal
import datetime
import time
import configparser
import logging
import csv
import shutil
from multiprocessing import Process, Queue
from badgeuse.Passage import *
from badgeuse.Mail import *
from badgeuse.LecteurCarte import *


CONFIG_FILE = '/etc/badgeuse-apprentis/config'


def lire_carte(q, f):
    cardmonitor = CardMonitor()
    lecteur = Lecteur(q)
    cardmonitor.addObserver(lecteur)

    while True:
        if(f.qsize() > 0):
            try:
                if(f.get(True) == 'fin'):
                    break
            except:
                pass
        time.sleep(1)

    logging.info('Arrêt du lecteur')
    cardmonitor.deleteObserver(lecteur)
    f.put('fin')


def creer_processus_lecteur(q, f):
    logging.info('Activation du lecteur')
    p = Process(target=lire_carte, args=(q, f))
    p.start()


def ajoutSecs(tm, secs):
    date = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    date = date + datetime.timedelta(seconds=secs)
    return date.time()

def main():
    # Lecture du fichier de configuration
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    # Emplacement de stockage des fichiers CSV générés
    _dossierDonnees = config['DIRECTORY']['DATA_DIRECTORY']
    if not os.path.exists(_dossierDonnees):
        os.makedirs(_dossierDonnees)

    # Emplacement de stockage des fichiers de logs
    _dossierLogs = config['DIRECTORY']['LOG_DIRECTORY']
    if not os.path.exists(_dossierLogs):
        os.makedirs(_dossierLogs)

    # Configuration des logs
    logging.basicConfig(filename=_dossierLogs + 'badgeuse-apprentis.log',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',level=config.getint('LOG', 'LOG_LEVEL'))

    # Initialisation des buffers de communication avec le lecteur
    q = Queue()
    f = Queue()

    # Configuration des horaires
    _heureDebut = datetime.datetime.strptime(config['FONCTIONNEMENT']['HEURE_DEBUT'], '%H:%M:%S').time()
    _heureCollecte = datetime.datetime.strptime(config['FONCTIONNEMENT']['HEURE_COLLECTE'], '%H:%M:%S').time()
    _finSemaine = config.getint('FONCTIONNEMENT', 'FIN_SEMAINE')

    _lecteurEstActif = False

    logging.info("Démarrage du service")
    # Boucle principale
    while True:
        if q.qsize() > 0:
            with open(nomFichierCSV, 'a') as fichiercsv:
                csvwriter = csv.writer(fichiercsv,
                                       delimiter=',',
                                       quotechar='|',
                                       quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(q.get(False).ToCSV())

        if not _lecteurEstActif and \
           datetime.datetime.now().time() >= _heureDebut and \
           datetime.datetime.now().time() < _heureCollecte:
            # Activation du lecteur
            creer_processus_lecteur(q, f)
            _lecteurEstActif = True
            
            # Définition du nom du fichier CSV
            nomFichierCSV = _dossierDonnees
            nomFichierCSV += datetime.datetime.now()\
            .strftime('%Y_%m_%d')
            nomFichierCSV += '.csv'

        # Vérification s'il est l'heure de la collecte
        if datetime.datetime.now().time() >= _heureCollecte and \
           datetime.datetime.now().time() < ajoutSecs(_heureCollecte, 10):

            # Test si il y a eu des passages dans la journée
            if os.path.exists(nomFichierCSV):
                # Envoi du mail
                mail = Mail()
                mail.ConfigurerServeurSMTP(config['SMTP']['SMTP_UTILISATEUR'],
                                           config['SMTP']['SMTP_MOTDEPASSE'],
                                           config['SMTP']['SMTP_URL'],
                                           config['SMTP']['SMTP_PORT'])
                mail.Preparer(config['MAIL']['MAIL_QUOTIDIEN_DESTINATAIRE'].split(','),
                              config['MAIL']['MAIL_QUOTIDIEN_OBJET']
                              .format(datetime.datetime.now().strftime('%d/%m/%Y')),
                              config['MAIL']['MAIL_QUOTIDIEN_MESSAGE']
                              .format(datetime.datetime.now() \
                              .strftime('%d/%m/%Y')))
                mail.AjouterPiecesJointes([nomFichierCSV])
                mail.Envoyer()
                logging.info("Mail envoyé")
            else:
                logging.info("Pas de passage le " + datetime.datetime.today().date())

            # Vérification si c'est la fin de semaine
            if datetime.datetime.today().weekday() == _finSemaine:

                # Vérification de la présence d'au moins un fichier
                # dans la semaine
                aujourdhui = datetime.datetime.today().date()
                semaine = [aujourdhui + datetime.timedelta(days=i) \
                           for i in range(0 - aujourdhui.weekday(),
                           5 - aujourdhui.weekday())]
                fichierPassages = []
                for jour in semaine:
                    fichier = _dossierDonnees + jour.strftime('%Y_%m_%d') + '.csv'
                    if os.path.exists(fichier):
                        fichierPassages.append(fichier)

                nomFichierCSVsemaine = _dossierDonnees + 'semaine_' + \
                                       datetime.datetime.now().strftime('%Y') + \
                                       '_' + str(datetime.datetime.now() \
                                       .isocalendar()[1]) + '.csv'

                # Si au moins un fichier, création du fichier de la semaine
                if len(fichierPassages) > 0:
                    with open (nomFichierCSVsemaine, 'w+') as fichiercsv:
                        for fichier in fichierPassages:
                            shutil.copyfileobj(open(fichier, 'r'), fichiercsv)
                        fichiercsv.close()
                else:
                    logging.info("Pas de passage la semaine " +
                                 str(datetime.datetime.now().isocalendar()[1]))

                if os.path.exists(nomFichierCSVsemaine):
                    # Envoi du mail
                    mail = Mail()
                    mail.ConfigurerServeurSMTP(config['SMTP']['SMTP_UTILISATEUR'],
                                               config['SMTP']['SMTP_MOTDEPASSE'],
                                               config['SMTP']['SMTP_URL'],
                                               config['SMTP']['SMTP_PORT'])
                    mail.Preparer(config['MAIL']['MAIL_HEBDOMADAIRE_DESTINATAIRE'].split(','),
                                  config['MAIL']['MAIL_HEBDOMADAIRE_OBJET']
                                  .format(datetime.datetime.now()
                                  .isocalendar()[1]),
                                  config['MAIL']['MAIL_HEBDOMADAIRE_MESSAGE']
                                  .format(datetime.datetime.now() \
                                  .isocalendar()[1]))
                    mail.AjouterPiecesJointes([nomFichierCSVsemaine])
                    mail.Envoyer()
                    logging.info("Mail envoyé")

                # Arret du lecteur de badge
                f.put('fin')
                time.sleep(2)
                if(f.qsize() > 0):
                    try:
                        if(f.get(False) == 'fin'):
                            _lecteurEstActif = False
                    except:
                        logging.error("Lecteur toujours actif")
                # Attente du vendredi à 20h au lundi à 6h (2 jours + 10h)
                time.sleep(config.getfloat('FONCTIONNEMENT', 'TEMPORISATION_ENTRE_SEMAINE') * 60 * 60)

            else:
                # Arret du lecteur de badge
                f.put('fin')
                time.sleep(2)
                if(f.qsize() > 0):
                    try:
                        if(f.get(True) == 'fin'):
                            _lecteurEstActif = False
                    except:
                        logging.error("Lecteur toujours actif")
                 # Attente du lendemain matin
                time.sleep(config.getfloat('FONCTIONNEMENT', 'TEMPORISATION_ENTRE_JOUR') * 60 * 60)

        else:
            time.sleep(1)

    logging.info("Arrêt du service")


if __name__ == '__main__':
    main()

