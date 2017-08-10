

Installation

sudo python3 setup.py install

sudo systemctl daemon-reload

# Lancement du service au démarrage de la machine
sudo systemctl enable badgeuse-apprentis.service

# Lancement du service
sudo systemctl start badgeuse-apprentis.service

# Arret du service
sudo systemctl stop badgeuse-apprentis.service

# Information de l'état du service
sudo systemctl status badgeuse-apprentis.service

# Log relatifs au service
sudo journalctl -f -u badgeuse-apprentis.service
