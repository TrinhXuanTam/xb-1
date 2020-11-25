Návod na instalaci a deploy (Debian server)
===========================================

- nainstalujte si docker a docker-compose
- stáhněte si tento projekt
    - vytvořte novou složku a přejděte do ní
    - zadejte `git init`
    - zadejte `git clone git@gitlab.fit.cvut.cz:trinhxu2/xb-1.git`
- v souboru `production/.env.prod` a v souboru `production/.env.prod.db` nastavte proměnné produkčního serveru (popsané v sekci níže = TODO)
- autentizujte se gitlab deploy tokenem (Autentizační token vám předá správce git repozitáře projektu): `sudo docker login -u <<nazev_tokenu>> -p <<klic_tokenu>> gitlab.fit.cvut.cz:5000`
- zadejte prikaz `./start.sh`

Zapnutí projektu pro development
================================

zapnutí serveru
---------------
v home adresáři `sudo docker-compose up`, případně `sudo docker-compose up -d` pro běh v detached módu (bez viditelného logu)

pokud za běhu budete chtít zadávat další příkazy např. migrate apod, otevřte si druhé okno v konzoli (Ctrl + Shift + T) a tam je zadávejte

vypnutí serveru
---------------
`Ctrl + C`

vytvoření migrací databáze
--------------------------
`sudo docker-compose exec web python manage.py makemigrations`

aplikování migrací na databázi
------------------------------
`sudo docker-compose exec web python manage.py migrate`

vytvoreni superusera
--------------------
`sudo docker-compose exec web python manage.py createsuperuser`

tvorba prekladu
---------------
preklad v templatu:
 1. v hlavicce templatu `{% load i18n %}`
 2. preklad: `{% trans "What I want to translate." %}`

preklad v py souborech:
 1. `from django.utils.translation import ugettext_lazy as _`
 2. preklad: `_("What I want to translate.")`

pred prvnim spustenim stahnete gettext (linux) `sudo apt-get install gettext`
 1. `sudo docker-compose exec web python manage.py makemessages  -l 'cs'` - vytvori seznam prekladu
 2. `sudo docker-compose exec web python manage.py compilemessages` - zkompiluje sepsane preklady


nahrani uzivatelskych skupin do db
----------------------------------
`sudo docker-compose exec web python manage.py loaddata groups.json` - TODO otestovat

export uzivatelskych skupin do json
-----------------------------------
`sudo docker-compose exec web python manage.py dumpdata --indent 1 auth.group > groups.json` - TODO otestovat

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
