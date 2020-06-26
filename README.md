Návod na instalaci a deploy (Debian server)
===========================================
- stáhněte si zip tohoto projektu: https://gitlab.fit.cvut.cz/trinhxu2/xb-1/-/archive/master/xb-1-master.zip
- tento zip vyextrahujte a prejdete do jeho slozky
- v souboru setup.sh upravte nasledujici promenne:
    - `port_number` - zde zadejte na jakem portu aplikace pobezi
    - `server_name` - zde zadejte public IP serveru / domenove jmeno
    - `home_folder` - zde zadejte cestu do home slozky uzivatele (napr.: `/home/dev`)
- pridejte skriptu prava pro spusteni: `chmod +x setup.sh`
- spuste skript: `./setup.sh` (Behem behu skriptu budete pozadani o potvrzeni instalaci balicku pomoci `y`, pro zadani hesla pro sudo prikazy a pro vytvoreni superusera database serveru)
- skript nejprve stahne potrebne zavislosti, nasledne spusti konfiguraci django serveru, nakonec nakonfiguruje nginx server.
- po dokonceni behu skriptu, zacne byt server dostupny pres zvolenou adresu a port
- log soubory nginx jsou v adresari `/var/log/nginx/`
- pro restart serveru zadejte (např při změně zdrojových souborů django serveru): `sudo service uwsgi restart`

Zapnutí projektu
================


Instalace
---------
Pro prvni zapnuti serveru zadejte: `sudo sh install.sh`


Spusteni serveru
----------------
Pokud jste jiz provedli prvni instalaci, server spustite takto: `sh run.sh`


Zapnuti na linux subsystemu pro windows
---------------------------------------
Nemuzu zarucit ze to bude na 100% fungovat

instalace: `sudo -H ./windows_install.sh`

spusteni: `./windows_run.sh`


prvni zapnuti projektu ve windows powershellu
---------------------------------------------
! pro python muzete mit v systemu jiny alias nez `python`, pokud `python` nefunguje zkuste `python3`/`py`/`py3`

* aby spravne fungovalo virtualni prostredi v powershellu, je nutne ho spustit v rezimu spravce a spustit: `Set-ExecutionPolicy Unrestricted -Force`
* prejdete do home directory projektu (pro spusteni initial webu prejdete do slozky initial_web)
* vytvorte novy virtual enviroment (`virtualenv xb1_env`)
* zapnete virtual enviroment (`./xb1_env/Source/activate.ps1`)
* stahnete potrebne zavislosti (`pip install -r requirements.txt`)
* prejdete do slozky, ve ktere je django projekt (`cd xb1`)
* zapnete django server (`python manage.py runserver`) - zobrazi se hlasky, "You have xx unaplied migratoions..." -> nejsou aplikovane migrace do databaze
* vypnete server a spuste (`python manage.py migrate`), aplikuji se zmeny v aplikaci do databaze
* zapnete django server (`python manage.py runserver`)


spusteni serveru ve windows powershellu
---------------------------------------
* prejdete do home directory projektu
* zapnete virtual enviroment (`./xb1_env/Source/activate.ps1`)
* prejdete do slozky, ve ktere je django projekt (`cd xb1`)
* zapnete django server (`python manage.py runserver`)


zaponuti virtualenv
-------------------
`source xb1_env/bin/activate`


vypnuti virtualenv
------------------
`deactivate`


vytvoreni superusera
--------------------
`python3 manage.py createsuperuser`

tvorba prekladu
---------------
preklad v templatu:
 1. v hlavicce templatu `{% load i18n %}`
 2. preklad: `{% trans "What I want to translate." %}`

preklad v py souborech:
 1. `from django.utils.translation import ugettext_lazy as _`
 2. preklad: `_("What I want to translate.")`

pred prvnim spustenim stahnete gettext (linux) `sudo apt-get install gettext`
 1. `python manage.py makemessages  -l 'cs'` - vytvori seznam prekladu
 2. `python manage.py compilemessages` - zkompiluje sepsane preklady


nahrani uzivatelskych skupin do db
----------------------------------
`python3 manage.py loaddata groups.json`

export uzivatelskych skupin do json
-----------------------------------
`python manage.py dumpdata --indent 1 auth.group > groups.json`

typy uzivatelskych prav
-----------------------
Kazdy model automaticky generuje tyto 4 druhy prav:
`add_modelname`, `change_modelname`, `delete_modelname`, `view_modelname`
(modelname odpovida nazvu modelu v lower case)

K pravum se pristupuje skrze nazev aplikace: `articles.add_article`

Jestlize chci zabranit aby uzivatel mohl vstoupit na stranku:
1. V templatu, co obsahuje odkaz na stranku musi byt odkaz podminen pravem:
    - pr.: `{%if perms.articles.change_article %} <a href="{% url 'articles:article_update' pk=article.pk %}">Edit article</a> {%endif%}`
    - Odkaz na editaci clanku se zobrazi jen uzivateli co ma prislusna opravneni
2. Opravneni musi byt osetrene i na samotnem view (nestaci jen skryt tlacitko, uzivatel si muze domyslet jaka je url)
    - `from django.contrib.auth.mixins import PermissionRequiredMixin`
    - kazde view, ktere ma omezeni pristupu musi dedit tuto tridu
    - je nutne specifikovat, jake je nutne opravneni: `permission_required = "articles.add_article"`
    - viz articles.views.ArticleCreateView


Code of conduct
===============


Výběr tasku
-----------
V záložce [Issues](https://gitlab.fit.cvut.cz/trinhxu2/xb-1/issues) vyberte otevřený úkol, který **nemá label** "Ve vývoji".

![](images/assignEmployee.png)
Následně se přiřaďte pod tento task, kliknutím na **assign yourself**.

![](images/assignLabel.png)
Tasku přidejte label **Ve vývoji** (Lépe je pak vidět, že task je obsazený).

![](images/createBranch.png)
Vytvořte si pro task novou větev na Gitlabu. **Nepracujte ve větvi master!**
Klikněte na **Create merge request**.
Zvolte že chcete jen branch.
Jméno nové branche neměnte, source branch ponechte master.


Commitování změn
----------------
V commit message popište stručně, anglicky co jste ve změně udělali.


Odevzdání tasku
---------------
Pokud jste již úkol dodělali, udělejte do něj merge master větve.
Následně vytvořte nový merge request na větev master a za assignee dejte jméno **@ridzodan**.
Pokud je v titlu commit message, přepiště title na název úkolu/branche.
Do komentáře zapište, kolik času jste na úkolu strávili. (např.: `/spend 2h 10m`)
Klikněte na **submit merge request**.
