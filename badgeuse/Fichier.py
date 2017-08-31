import os
import sys
import datetime
import time
import logging
import csv
import shutil

class FichierCSV:
    def __init__(self, nomfichier):
        self._nomfichier = nomfichier

    def EcrireLigne(self, ligne):
        with open(self._nomfichier, 'a') as fichiercsv:
            csvwriter = csv.writer(fichiercsv,
                                   delimiter=',',
                                   quotechar='|',
                                   quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(ligne)

    def ConcatenerFichiers(self, listefichiers):
        with open(self._nomfichier, 'w+') as fichiercsv:
            for fichier in listefichiers:
                shutil.copyfileobj(open(fichier, 'r'), fichiercsv)
            fichiercsv.close()

    def Existe(self):
        if os.path.exists(self._nomfichier):
            return True
        else:
            return False

