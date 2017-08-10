import os
import sys
import smtplib
import logging
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '


class Mail:
    def ConfigurerServeurSMTP(self, utilisateur, motdepasse, url, port):
        self._expediteur = utilisateur
        self._motdepasse = motdepasse
        self._serveur = url
        self._port = port

    def Preparer(self, destinataires, sujet, texte):
        self._destinataires = destinataires

        # Création du message
        self._message = MIMEMultipart()
        self._message['Subject'] = sujet
        self._message['To'] = COMMASPACE.join(self._destinataires)
        self._message['From'] = self._expediteur
        self._message.preamble = '''You will not see this in a MIME-
                                    aware mail reader.\n'''
        self._message.attach(MIMEText(texte, 'html'))  # ou 'plain'

    def AjouterPiecesJointes(self, listePJ):
        # Ajout des pièces jointes
        for file in listePJ:
            try:
                with open(file, 'rb') as fp:
                    msg = MIMEBase('application', "octet-stream")
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment',
                               filename=os.path.basename(file))
                self._message.attach(msg)
            except:
                logging.error("Impossible d'ouvrir les pièces jointes.'. Erreur: ",
                               sys.exc_info()[0])

    def Envoyer(self):
        # Envoi de l'email'
        try:
            with smtplib.SMTP(self._serveur, self._port) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(self._expediteur, self._motdepasse)
                s.sendmail(self._expediteur, self._destinataires,
                           self._message.as_string())
                s.close()
            loging.info("Email envoyé!")
        except:
            logging.error("Impossible d'envoyer le mail'. Erreur: ", sys.exc_info()[0])


if __name__ == '__main__':
    mail = Mail()
    mail.ConfigurerServeurSMTP('vincent.saulnier.94@gmail.com', 'mimine94',
                               'smtp.gmail.com', 587)
    mail.Preparer(['vini.chou.vc@gmail.com'], 'Test', 'Message test')
    mail.AjouterPiecesJointes(['''/home/vini/Documents/PFE_Session2/Développements
                                  /Badgeuse/donnees/2017_07_30.csv'''])
    mail.Envoyer()
