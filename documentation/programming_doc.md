# Programátorská dokumentace

## <a name="table_of_contents"></a>Obsah
1. [Obsah](#table_of_contents)
2. [Použité technologie](#technologies)
3. [Minimum OS/HW requirements](#requirements)
4. [Server maintenance](#)
    1. [První spuštění](#first_start)
    2. [Aktualizace serveru](#server_update)
    3. [Spuštění serveru](#server_start)
    4. [Vypnutí serveru](#server_shutdown)
    5. [Co ještě popsat v dokumentaci - TODO](#todo)
5. [Obsah souboru xb-1/production/.env](#envfile)


## <a name="technologies"></a>Použité technologie
- Virtualizace:
    - Docker
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

## <a name="requirements"></a>Minimum OS/HW requirements
- OS:
    - Debian 9/10
    - Přístup k serveru jakou superuser
- HW:
    - 2 GB RAM
    - 24 GB SSD

## <a name="server_maintenance"></a>Server maintenance

### <a name="first_start"></a>První spuštění

- Přihlaste se do systému s účtem s administrátorskými právy (uživatel s povolením sudo příkazů)
- Nainstalujte si docker a docker-compose
- Povolte docker daemon, aby se server znovu zapnul při restartu serveru
    - `sudo systemctl enable docker`
- Vytvořte nového uživatele **s uid 5544**, s jakýmkoli jménem. (Tento uživatel bude následně spravovat web)
    - `sudo useradd -m -u 5544 -G docker -s /bin/bash username`
        - přepínač -m vytvoří uživateli složku v home adresáři
        - přepínač -u nastaví uživateli specifikované uid
        - přepínač -G přidá uživatele do docker skupiny (Bez této skupiny by uživatel nemohl ovládat docker)
        - přepínač -s nastaví uživateli defautní shell
- Nastavte uživateli nové heslo
    - `sudo passwd username`
- Odhlašte se a přihlaste pod účtem právě vytvořeného uživatele
- Stáhněte si tento projekt
    - zadejte `git clone https://gitlab.fit.cvut.cz/trinhxu2/xb-1.git`
    - zadejte `cd xb-1` pro přejití do složky s projektem
- v souboru `production/.env` a v souboru nastavte proměnné produkčního serveru ([popsané v sekci níže](#envfile))
- autentizujte se gitlab deploy tokenem (Autentizační token vám vygeneruje a předá správce git repozitáře projektu)
    - `sudo docker login -u <<nazev_tokenu>> -p <<klic_tokenu>> gitlab.fit.cvut.cz:5000`
- přejděte do složky production
    - `cd production`
- zavolejte skript pro update serveru
    - `sh update.sh`
- zavolejte skript pro start serveru
    - `sh start.sh`
- pro zobrazení logu dockeru ve chvíli, kdy server beží, zavolejte
    - `sh log.sh`

### <a name="server_update"></a>Aktualizace serveru
- V případě, že proběhly nějaké změny zdrojových kódů aplikace zavolejte tyto příkazy
- Přejděte do složky production
    - `cd xb-1/production`
- Pokud proběhly změny i mimo django aplikaci (např. v konfiguraci databáze, nginxu či dockeru) bude potřeba aktualizovat celý repozitář:
    - `git pull`
- Následně spusťte skript pro update serveru
    - `sh update.sh`
        - Skript stáhne nově sestavený balíček django aplikace a aktualizuje jím dosavadní docker image
        - Před svým během během skript vždy provede kompletní zálohu databáze
- Po dokončení aktualizace zůstane server vypnutý, proto zavolejte skript pro jeho zapnutí
    - `sh start.sh`

### <a name="server_start"></a>Spuštění serveru
- Přejděte do složky production
    - `cd xb-1/production`
- Zavolejte skript pro start serveru
    - `sh start.sh`
        - Skript před spuštěním serveru provede kompletní zálohu databáze

### <a name="server_shutdown"></a>Vypnutí serveru
- Přejděte do složky production
    - `cd xb-1/production`
- Zavolejte
    -  `docker-compose down`

### <a name="todo"></a>Co ještě popsat v dokumentaci - TODO
- nahrání zálohy databáze

## <a name="envfile"></a>Obsah souboru xb-1/production/.env
ukázkový obsah souboru .env:
>DEBUG=0  
SECRET_KEY=**change_this**  
DJANGO_ALLOWED_HOSTS=*  
DATABASE=postgres  
SQL_ENGINE=django.db.backends.postgresql  
SQL_HOST=db  
SQL_PORT=5432  
SQL_USER=xb1_user  
POSTGRES_USER=xb1_user  
SQL_PASSWORD=hello_xb1  
POSTGRES_PASSWORD=hello_xb1  
SQL_DATABASE=xb1_dev  
POSTGRES_DB=xb1_dev  

- DEBUG
    - Zanechte 0 pro běh aplikace v produkčním režimu
    - Při přepnutí na 1 se zapne debug mód, což ohrozí bezpečnost aplikace
- SECRET_KEY
    - Zde vložte náhodně generovaný string bez mezer o délce 50 znaků
    - Lze použít například tento [generátor](https://miniwebtool.com/django-secret-key-generator/)
    - secret key slouží k lepšímui zabezpečení serveru, podrobnější info [zde](https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECRET_KEY)
- DJANGO_ALLOWED_HOSTS
    - Touto hodnotou sprecifikujete, přes jaké domény bude server dostupný
    - Pokud zde zadáte `*`, server nebude příchozí volání nijak omezovat
    - Pro lepší zabezpečení zadejte doménové jméno serveru, například `xb1-fans.sic.cz`
    - Pokud bude na server odkazovat více doménových jmen, napište je za sebe, odděleny mezerou: `xb1-fans.sic.cz xb1.cz`
    - podrobnější info ohledně allowed hosts [zde](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)
- DATABASE=postgres
    - neměňte
- SQL_ENGINE=django.db.backends.postgresql
    - neměňte
- SQL_HOST=db
    - neměňte
- SQL_PORT=5432
    - neměňte
- SQL_USER=xb1_user
    - jméno uživate databáze, musí se shodovat s POSTGRES_USER
- POSTGRES_USER=xb1_user
    - jméno uživate databáze, musí se shodovat s SQL_USER
- SQL_PASSWORD=hello_xb1
    - heslo uživate databáze, musí se shodovat s POSTGRES_PASSWORD
- POSTGRES_PASSWORD=hello_xb1
    - heslo uživate databáze, musí se shodovat s SQL_PASSWORD
- SQL_DATABASE=xb1_dev
    - jméno databáze, musí se shodovat s POSTGRES_DB
- POSTGRES_DB=xb1_dev
    - jméno databáze, musí se shodovat s SQL_DATABASE
- TODO chtělo by to sjednotit tyto zbytečně zdvojené proměnné a odstranit proměnné, co se nesmí měnit (nahardcodit je do django settings)
