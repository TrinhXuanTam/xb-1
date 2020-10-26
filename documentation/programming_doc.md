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

## Minimum OS/HW requirements
- OS:
    - Debian 9/10
    - Přístup k serveru jakou superuser
- HW:
    - 2 GB RAM
    - 24 GB SSD


## Návod na instalaci (Debian server)
- stáhněte si zip tohoto projektu: https://gitlab.fit.cvut.cz/ridzodan/sp1-initial-web/-/archive/master/sp1-initial-web-master.zip
- tento zip vyextrahujte v domovském adresáři uživatele
- následně přesuňte obsah extrahované složky o level výše (tedy do home adresáře uživatele): `mv sp1-initial-web-master/* .`
- **před voláním následujících skriptů se ujistěte, že složka xb1 z git repositáře je v home adresáři uživatele (případně je nutné upravit cestu k projektu v konfiguračních souborech  nginxu)**
- v souboru **nginx_conf** nastavte port (proměnná **listen**) a adresu serveru/doménu (proměnná **server_name**). Změňte výskyt proměnné *ridzodan* za jméno vašeho usera. Soubor uložte.
- v souboru **xb1.ini** změňte proměnnou **base**, tak aby odkazovala na váš home adresář. Soubor uložte
- spustě příkaz `chmod +x setup_django_server.sh`
- spustě příkaz `./setup_django_server.sh`
    - tento script stáhne potřebné závislosti pro běh django serveru
    - následně vytvoří serveru virtuální prostředí
    - nainstaluje potřebné python knihovny
    - zinicializuje django server
- spustě příkaz `chmod +x setup_nginx_server.sh`
- spustě příkaz `./setup_nginx_server.sh`
    - tento script stáhne potřebné závislosti pro běh nginx reverse proxy serveru
    - vytvoří konfigurační soubory, pro nalinkování serveru
    - server by v tuto chvíli již měl být dostupný na zadané adrese.
- pro restart serveru zadejte (např při změně zdrojových souborů django serveru): `sudo service uwsgi restart`