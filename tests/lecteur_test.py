import unittest
import time
from smartcard.CardMonitoring import CardMonitor, CardObserver
from multiprocessing import Queue
from badgeuse.LecteurCarte import Lecteur

class LecteurCarteTest(unittest.TestCase):
    def setUp(self):
        self.q = Queue()
        self.cardmonitor = CardMonitor()
        self.lecteur = Lecteur(self.q)
        self.cardmonitor.addObserver(self.lecteur)

    def test_lecturecarte(self):
        print('\nVous avez 10 secondes pour présenter une ou plusieurs cartes au lecteur.')
        time.sleep(10)

        self.assertNotEqual(self.q.qsize(), 0, 'Le lecteur n\'a lu aucune carte.')
        self.cardmonitor.deleteObserver(self.lecteur)
