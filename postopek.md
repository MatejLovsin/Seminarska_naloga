1. Iskanje pravilnega načina zbiranja podatkov. (Claude - Analiza podatkov z bs)
    Zaradi varnostnih omejitev strani avto.net requests.get() ne deluje in ne vrne željenenih rezultatov, (response.status_code = 403)
    Namesto tega, bo uporabljen isti način kot na predavanju (with open("") as f), ampak bo potrebno več ročnega dela. Vsaka stran na avtonetu prikazuje približno 50 oglasov, željena velikost vzorca pa je 200-300 avtov na posamezno znamko. Poleg tega avto.net "skriva" večino rezultatov iskanja. Preveč grobo iskanje (npr. BMW) vrne 1.000 rezultatov glede na uporabljeno razvrščanje namesto vseh ~5.000. Zaradi tega bo med zajemanjem podatkov uporabljenih več različnih razvrščanj in strani ki se bodo uporabile bodo naključne oziroma izbrane za bolj nazoren prikaz nekaterih primerjav.

2. Ecoding težava. (Claude - Analiza podatkov z bs)
    Avto.net je starejša stran ki je zapisana v starejšem kodiranju zato encoding="UTF-8" ni primerna ampak jo zamenja encoding="cp1250"
    Podrobnosti kako sem prišel do rešitve so v pogovoru s Claudeom

3. Iskanje in izbira strani.
    Prvih 5/6 strani izbranih med najnovejšimi oglasi nato 4 glede na ceno. Posebej pozornost da so izbrani pri vseh znamkah blizu določenih cenovnih rangov - 50.000€, 70.000€, 90.000€ in najboljše kar ponuja posamezna znamka. Cilj izbora je poleg poskušanja prirediti naključnosti na manjšem izboru tudi ustreznost pri željenih primerjavah, zato je bila oddatna pozornost namenjena izbiranju oglasov na določenih cenovnih rangih.