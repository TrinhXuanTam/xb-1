# Programátorská dokumentace
## Použité technologie
- Backend server:
    - python 3.7
    - django 3.0.3
- Webový server (reverzní proxy server):
    - nginx
- Python knihovny:
    - asgiref==3.2.3
    - Django==3.0.3
    - django-admin-tools==0.9.0
    - django-ckeditor==5.9.0
    - django-cleanup==4.0.0
    - django-crispy-forms==1.9.0
    - django-js-asset==1.2.2
    - django-model-utils==4.0.0
    - Pillow==7.1.1
    - pytz==2019.3
    - six==1.14.0
    - sqlparse==0.3.0
    - whitenoise==5.0.1
    - Pillow==7.1.1
    - django-crispy-forms==1.9.0
    - django-cleanup==4.0.0
    - selenium

## Minimum OS/HW requirements
- OS:
    - Debian 9/10
    - Přístup k serveru jakou superuser
- HW:
    - 2 GB RAM
    - 24 GB SSD


## Návod na instalaci (Debian server)
- stáhněte si zip tohoto projektu: https://gitlab.fit.cvut.cz/trinhxu2/xb-1/-/archive/master/xb-1-master.zip
- tento zip vyextrahujte
- v souboru setup.sh upravte nasledujici promenne:
    - `port_number` - zde zadejte na jakem portu aplikace pobezi
    - `server_name` - zde zadejte public IP serveru / domenove jmeno
    - `home_folder` - zde zadejte cestu do home slozky uzivatele (napr.: `/home/dev`)
- pridejte skriptu prava pro spusteni: `chmod +x setup.sh`
- spuste skript: `./setup.sh` (Behem behu skriptu budete pozadani o potvrzeni instalaci balicku pomoci `y` a pro zadani hesla pro sudo prikazy)
- skript nejprve stahne potrebne zavislosti, nasledne spusti konfiguraci django serveru, nakonec nakonfiguruje nginx server.
- po dokonceni behu skriptu, zacne byt server dostupny pres zvolenou adresu a port
- log soubory nginx jsou v adresari `/var/log/nginx/`
- pro restart serveru zadejte (např při změně zdrojových souborů django serveru): `sudo service uwsgi restart`
