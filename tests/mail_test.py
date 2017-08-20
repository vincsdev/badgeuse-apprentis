import unittest
from badgeuse.Mail import Mail

class MailTest(unittest.TestCase):
    def setUp(self):
        self.mail = Mail()
        self.mail.ConfigurerServeurSMTP('<mail>', '<mdp>',
                               'smtp.gmail.com', 587)
        self.mail.Preparer(['<destinataires>'], 'Test', 'Message test')

    def test_piecejointe(self):
        self.assertTrue(self.mail.AjouterPiecesJointes(['<piece jointe>']), 'Au moins un problème lors de l\'ajout de pièce(s) jointe(s).')

    def test_envoi(self):
        self.assertTrue(self.mail.Envoyer(), 'Message non envoyé.')
