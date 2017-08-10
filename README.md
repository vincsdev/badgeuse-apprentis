# Badgeuse apprentis

## Getting started

### Installing
```
# python3 setup.py install
```

Reload to discover new daemons
```
# systemctl daemon-reload
```

Enable start-up at boot
```
# systemctl enable badgeuse-apprentis.service
```

To start the service
```
# systemctl start badgeuse-apprentis.service
```

To stop the service
```
# systemctl stop badgeuse-apprentis.service
```

Information about service state
```
# systemctl status badgeuse-apprentis.service
```

Log from service
```
# journalctl -f -u badgeuse-apprentis.service
```
