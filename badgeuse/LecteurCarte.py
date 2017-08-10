import datetime
from smartcard.scard import *
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from badgeuse.Passage import *


class Lecteur(CardObserver):
    def __init__(self, q):
        self._q = q

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
            assert hresult == SCARD_S_SUCCESS
            hresult, readers = SCardListReaders(hcontext, [])
            assert len(readers) > 0
            reader = readers[0]

            hresult, hcard, dwActiveProtocol = SCardConnect(hcontext,
                                                            reader,
                                                            SCARD_SHARE_SHARED,
                                                            SCARD_PROTOCOL_T0 |
                                                            SCARD_PROTOCOL_T1)

            hresult, response = SCardTransmit(hcard, dwActiveProtocol,
                                              [0xFF, 0xCA, 0x00, 0x00, 0x00])
            res = ""
            for b in response:
                res += format(b, "02x") + ":"
            self._q.put(Passage(res[:-7]))


if __name__ == '__main__':
    cardmonitor = CardMonitor()
    lecteur = Lecteur()
    cardmonitor.addObserver(lecteur)

    sleep(60)

    cardmonitor.deleteObserver(cardobserver)

