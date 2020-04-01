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

    Co jsou naše konkurenční stránky:
    - fan page časopisů
    - oficiální stránky časopisů

    Co obsahují konkurenční weby:
    - články na téma daného časopisu
    - občas i ukázku článku z tištěné verze
    - diskuze pod články
    - prodej předplatného a dalších předmětů, vztahující se k časopisu
    - soutěže
    - uživatelská sekce (fanart sekce, diskuze na volné téma)

    
5. Funkční požadavky

    Web je spravován správci (uživateli administrátory). Dále existují běžní uživatelé, kteří mohou využít níže popsaných funkcí. Hlavním obsahem webu jsou články, ke kterým se vážou různé funkcionality v závislosti na typu uživatele. 
    Dále je možné využít live chat nebo podpořit provozovatele zakoupením zboží v e-shopu.
    
   Uživatelská sekce:
    - uživatelé se mohou nacházet ve dvou stavech:
        - aktivní = možnost přihlášení, práva běžného uživatele/administrátora
        - neaktivní = nemožnost se přihlásit a zamezení práv běžného uživatele/administrátora, při pokusu o přihlášení mu bude sděleno, že je uživatel neaktivní, a nabídne mu znovu zaslání potvrzovacího emailu, či změny emailu
        - zabanovaný = nemožnost se přihlásit a zamezení práv běžného uživatele/administrátora + nemožnost použít aktivační link (zabanování během registrace, např. překročení limitu odeslaných žádostí,... ), při pokusu o přihlášení mu bude sděleno, že je uživatel zabanovaný (důvod banu, délka banu)
    - na každé stránce se nachází vysouvací sidebar na levé straně, který nabízí různé funkcionality pro registrované uživatele (kontakt, zobrazení profilu, logout)
    - registrace uživatelů: 
        - k registraci je nutné zadat přezdívku, e-mail a zvolit si heslo (včetně potvrzení)
        - poté se uživateli pošle zpráva s aktivačním linkem (validní pouze 24 hodin od odeslání) na zadaný email
        - uživatel je v tuto chvíli označen jako neaktivní a nebude mu dovoleno se přihlásit bez potvrzení (v případě, že by se pokusil přihlásit s účtem v neaktivním stavu, bude mu oznámeno, že účet je neaktivní a bude mu nabídnuta možnost zadat email znova nebo znovu zaslání zprávy s aktivačním linkem)
        - po rozkliknutí validního linku bude uživatel ve aktivním stavu a budou mu zpřístupněny uživatelské funkcionality.
    - sekce profil uživatele bude obsahovat:
        - vyplnění bližších kontaktních údajů (trvalé bydliště, jméno, příjmení) pro automatické vyplnění při objednávání z e-shopu, popřípadě změna těchto údajů
        - změna hesla
        - změna emailu (stejný způsob potvrzování jako při registraci)
        - změna hesla a emailu bude notifikována na email uživatele (při změně emailu bude zaslána notifikace  na email před změnou)
        - deaktivace účtu
    - práva běžného registrovaného uživatele:
        - přidávání/smazání/editace vlastních komentářů k článkům
        - přístup k profilové sekci, ve které může editovat svůj profil
        - kontakt s administrátory
        - možnost se zapojit k diskuzím
    - práva administrátorů:
        - správa uživatelů (zabanování/odbanování uživatele, resetování hesla pro daného uživatele, přidání práv administrátora danému účtu, změna přezdívky libovolného uživatele)
        - zabanování znamená, převod uživatele do neaktivního stavu
        - odbanování znamená, převod uživatele z neaktivního stavu do aktivního stavu
        - přidávání/smazání/editace vlastních komentářů k článkům
        - přístup k profilové sekci, ve které může editovat svůj profil
        - možnost se zapojit k diskuzím a jejich moderaci
        - možnost smazání komentářů k diskuzi/článku, které nejsou v souladu s podmínkami viz. sekce komentář
        - možnost přidání/editace/smazání vlastních článků

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

    - funkcionality pro administrátora
        - přidání nové položky do eshopu
        - přehled aktuálních objednávek
        - přehled již proběhlých objednávek
        - souhrn již proběhlých objednávek

    Ostatní:
    - při pomalém načítání na jakékoliv stránce se objeví animace pomalého načítání (točící se kolečko)

6. Nefunkční požadavky

    Responzivita:
    - Podpora počítačových rozlišení (1280x720, 1920x1080, 3840×2160)
    - Podpora mobilních rozlišení (540×960, 1280×720, 1920×1080)
    - Podpora velmi nízkých rozlišení vzhledek k základnímu designu stránek nebude zajištěna (méně než 540×960)  
    
    Datové nároky:
    - Podpora jednotného designu napříč uživatelsky přístupných stránkách (použitelnost cache paměti)
    - Podpora jednotného designu pro administrátorské stránky nebude zajištěna, nevyhovující forma pro administrační stránky
    - Více stránková aplikace, větší nároky než OnePage aplikace
    - Grafické komponenty především pozadí a další obrázky budou velikostně a tedy kvalitativně omezeny pro dosažení nejmenších datových nároků při zachování dostatečné grafické kvality

    Backend framework:
    - Použití Django frameworku psaném v jazyce Python (přesná verze včetně dalších požadovaných knihoven je obsažená v souboru ./../requirements.txt)
    - Framework byl vybrán na základě současné situace ve vývoji webových aplikací a kvality, kdy nejpřeněji splňuje dodané zadání, především implementace bezpečnostích prvků (CSRF)
    
    Grafická forma:
    - Aplikační vzhled bude rozdělen na dva nezávislé grafické celky (uživatelský, administrátoský)
    - Použití ucelených a přehledných šablon včetně volně dostupných piktogramů a emotikonů pro znázornění některých klíčových funcionalit
    