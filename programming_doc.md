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

## Návod na instalaci (Debian server)
- spustě příkaz `sudo sh install.sh`
    - tento script stáhne potřebné závislosti pro běh django serveru
    - následně vytvoří serveru virtuální prostředí
    - nainstaluje potřebné python knihovny
    - zinicializuje django server
- spustě příkaz `sudo sh install_nginx.sh`
    - tento script stáhne potřebné závislosti pro běh nginx reverse proxy serveru
    - vytvoří konfigurační soubory, pro nalinkování serveru
- spusťte příkaz `sudo sh run.sh`
    - tento script spustí nginx server

*Tyto scripty zatím nejsou funkční, ale brzy je zprovozníme*