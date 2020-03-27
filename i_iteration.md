Projekt XB-1
=============

Úvod
----

Tento dokument je první iterací a současně povinnou částí projektu XB-1

Osnova
------

1. Základní popis projektu
2. Popis práce a její rozdělení členům týmu
3. Analýza autorských práv původní webové aplikace
4. Analýza konkurenčních stránek
5. Funkční požadavky
6. Nefunkční požadavky

Obsah
-----

1. Základní popis projektu

    Cílem projektu týmu Ikarie je vytvoření nové plně funkční webové aplikace, která bude sdružovat komunitu Sci-Fi časobisu XB-1.
    Projekt by měl nahradit v současnosti již nefunkční systém. Základním požadavkem projektu je především správná a bezpečná funkčnost základních funkcí potřebných pro správu a využívání fanouškovské webové aplikace, přesný výpis požadovaných funcionalit lze nalézt v sekci 5.1 Funkční požadavky.
    Design webové části nové aplikace by měl být inspirován starým vzhledem včetně znovu použití loga, které bylo dodáno zadavatelem projektu.
    Jelikož nebyly dodány žádné nároky na jazykové provedení, bude projekt vyvíjen v jazyku Python za pomoci frameworku Django. Konkrétní jazyk a framework byly vybrány po analýze současného trhu s webovými aplikacemi, kde je v současné době nejpoužívanějším frameworkem právě Django a to především kvůli své spolehlivosti, jednoduchosti a bezpečnosti, protože mnoho bezpečnostích mechanismů je již implementováno.
    
2. Popis práce a její rozdělení členům týmu

    Práce na webových projektech lze obecně rozdělit do několika samostatných částí vývoj frontendu, vývoj backendu, testování. Zároveň lze práci rozdělit na jednotlivé úkoly, které vyplývají ze specifického zadání projektu, např. vývoj systému pro uživatele, vývoj redakčního systému pro administrátora, správa eshopu, objednávek a platba.
    
    Členové týmu včetně rozdělení práce:  
    Daniel Ridzoň **(ridzodan)** - *Vedoucí týmu, správa git a merge requestů*  
    Tomáš Kovářík **(kovart12)** - *Rozhraní eshop, testování*  
    David Trinch **(trinhxu2)** - *PLACE_HOLDER*  
    Adam Tran **(tranvuqu)** - *PLACE_HOLDER*  
    Petr Šmejkal **(smejkp13)** - *frontend vývojář, testování*
    
    
3. Analýza autorských práv původní webové aplikace

    Součástí projektu je i analýza všech práv vztahujících se na současnou nefunkční verzi webové aplikace dodanou externí firmou zadavateli.
    V současné době podle slov zadavatele se na serveru nachází pouze zlomek původních zdrojových kodů (jazyk neuveden), a protože nový projekt bude vyvíjen bez přístupu k původních zbývajícím zdrojovým kodům bude tedy zajištěna ochrana před možným proviněním proti autorskému zákonu.
    Zároveň s tím musí být zajištěna dostatečná originalita nového vzhledu webové aplikace, aby nebyla porušena autorská práva.
    Ze slov zadavatele vyplývá, že je autorem/má povolení použít již dodané logo původní aplikace avšak nemá právo použít původní design a pozadí.
    Autorský zákon chránící díla včetně webového design, který je jako originální uspořádání a upravení již implementovaných komponent také předmětem autorského zákona.
    Zároveň však zmiňuje že design webových stránek, který je často z mnoha různých důvodů podřizován velkému množství konvencí, včetně používání veřejně dostupných frameworků, může vykazovat určité rysové podobnosti s dílem jiného autora, protože tato podobnost neplyne z tvořivé činnosti autorů, ale ze základních prvků používaného framworku.

4. Analýza konkurenčních stránek

    Mekty mekty
    
5. Funkční požadavky

    Web je spravován správci (uživateli administrátory). Dále existují běžní uživatelé, kteří mohou využít níže popsaných funkcí. Hlavním obsahem webu jsou články, ke kterým se vážou různé funkcionality v závislosti na typu uživatele. 
    Dále je možné využít live chat nebo podpořit provozovatele zakoupením zboží v e-shopu.
    
    Uživatelská sekce:
    - na každé stránce se nachazí vysouvací sidebar na levé straně, který nabízí růžné funkcionality uživatelské sekce
    - registrace uživatelů - k registraci je nutné zadat přezdívku, e-mail a zvolit si heslo (včetně potvrzení), registrace musí být potvrzená odkazem v e-mailu

    - správa uživatelů (práva administrátora)
        - zabanování uživatele
        - resetování hesla pro daného uživatele
        - přidání práv administrátora danému účtu
        - změna přezdívky libovolného uživatele
    
    - funkcionality běžného uživatele
        - změna hesla

    Články a komentáře:
    - úvodní stránka zobrazuje aktuální (nejnovější) články
    - v sekci na pravé straně stránky je možné vybírat ze seznamu článků

    - funkcionality pro administrátora
        - vyvoření článku
        - smazání článku
        - úprava článku
        - přidání komentáře
        - smazání komentáře

    - funkcionality pro běžného uživatele
        - zobrazování článků
        - přidání komentáře
    
    - funkcionality pro neregistrované uživatele
        - zobrazování článků

    Live Chat:
    - real-time chatování pro registrované uživatele 

    Eshop:
    - přijímání objednávek
    - zpracování objednávek

    Ostatní:
    - při pomalém načítání na jakékoliv stránce se objeví animace pomalého načítání (točící se kolečko)

6. Nefunkční požadavky

    *Grafická forma* - Webová aplikace, tedy všechny její stránky by měly používat stejnou grafickou formu pro zabezpečení co možná nějvětší čitelnosti a přehlednosti, a to včetně administrátoských stránek. Zároveň budou využity volně dostupné ikony a piktogramy pro větší názornost klíčových funcionalit.  
    *Responzivita* - Vzhled webových stránek se automaticky bude měnit podle rozlišení zobrazovacího zařízení, především při nízkých rozlišeních a telefoních zařízeních.  
    *Datové nároky* - Aplikace je koncipována jako více stránková aplikace, tedy bude mít mírně větší datové nároky než one-page aplikace.  
    *Django* - Programovací framework byl vybrán na základě volně dostupných analýz současně existujících webových řešení, kde Django excelovalo v kategoriích požadovaných v zadání projektu.  
