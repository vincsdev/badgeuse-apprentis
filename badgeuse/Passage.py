import datetime


class Passage:
    def __init__(self, idcarte):
        self._date = datetime.datetime.now().date()
        self._heure = datetime.datetime.now().time()
        self._idCarte = idcarte

    def ToCSV(self):
        return [self._date.strftime('%d/%m/%Y'),
                self._heure.strftime('%H:%M:%S'),
                self._idCarte]

if __name__ == '__main__':
    p1 = Passage('00:22:55:88:99:66')
    print(p1.ToCSV())

    p2 = Passage('00:22:55:88:99:99')
    print(p2.ToCSV())

