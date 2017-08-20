import unittest
from badgeuse.Passage import Passage
import datetime

class PassageTest(unittest.TestCase):

    def setUp(self):
        self.idCarte = '00:11:22:33:44:55'
        self.date = datetime.datetime.now().date()
        self.heure = datetime.datetime.now().time()

        self.passage = Passage('00:11:22:33:44:55')

    def test_create(self):
        self.assertIsInstance(self.passage, Passage, 'Le type de l\'objet ne correspond pas à la classe attendue.')

    def test_tocsv(self):
        attendu = [self.date.strftime('%d/%m/%Y'),
                   self.heure.strftime('%H:%M:%S'),
                   self.idCarte]

        self.assertEqual(self.passage.ToCSV(), attendu, 'Le retour de la méthode ToCSV() n\'est pas celui attendu.')
