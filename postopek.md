1. Iskanje pravilnega načina zbiranja podatkov. (Claude - Analiza podatkov z bs)
    Zaradi varnostnih omejitev strani avto.net requests.get() ne deluje in ne vrne željenenih rezultatov, (response.status_code = 403)
    Namesto tega, bo uporabljen isti način kot na predavanju (with open("") as f), ampak bo potrebno več ročnega dela. Vsaka stran na avtonetu prikazuje približno 50 oglasov, željena velikost vzorca pa je 200-300 avtov na posamezno znamko. Poleg tega avto.net "skriva" večino rezultatov iskanja. Preveč grobo iskanje (npr. BMW) vrne 1.000 rezultatov glede na uporabljeno razvrščanje namesto vseh ~5.000. Zaradi tega bo med zajemanjem podatkov uporabljenih več različnih razvrščanj in strani ki se bodo uporabile bodo naključne oziroma izbrane za bolj nazoren prikaz nekaterih primerjav.

2. Ecoding težava. (Claude - Analiza podatkov z bs)
    Avto.net je starejša stran ki je zapisana v starejšem kodiranju zato encoding="UTF-8" ni primerna ampak jo zamenja encoding="cp1250"
    Podrobnosti kako sem prišel do rešitve so v pogovoru s Claudeom

3. Iskanje in izbira strani.
    Prvih 5/6 strani izbranih med najnovejšimi oglasi nato 4 glede na ceno. Posebej pozornost da so izbrani pri vseh znamkah blizu določenih cenovnih rangov - 50.000€, 70.000€, 90.000€ in najboljše kar ponuja posamezna znamka. Cilj izbora je poleg poskušanja prirediti naključnosti na manjšem izboru tudi ustreznost pri željenih primerjavah, zato je bila dodatna pozornost namenjena izbiranju oglasov na določenih cenovnih rangih.

4. Dodajanje tehničnih podatkov o vsakem avtu.
    Pri vseh avtih se zapišejo vsi podatki ki so podani, torej pri električnih ki imajo podane različne podatke kot ostali, dobijo svoje 'vrstice' in ostale imajo večinoma prazne. Posledično bo tabela pri električnih avtomobilih večinoma prazna (NaN), kar bo lahko vplivalo na nekatere primerjave. 
    Največ težav pri ceni, kjer je pomagal Claude (Web scraping with bs4...). Zapis cene se je razlikoval na več različnih načinov. Vsakič je bila cena gnezdena v 'div', class_="GO-Results-Price-Mid" ampak zaradi akcijskih cen in nekaterih oglasov, ki ne izdajajo cene javno (Pokličite za ceno) se gnezdeni elementi razlikujejo od oglasa do oglasa. Koda težavo reši tako da pregleda če ni gnezdenih elementov (morda cena zapisana že takoj v začetku), nato v primeru da je več gnezdenih elementov novo spremenljivko m spremeni za vsak element, da na koncu vzame znižano ceno in ne prvotne. 

5. Zanka za vse datoteke s podatki in deduplikacija
    Po preverjanju ustreznosti funkcije izlusci_avte je bilo treba najti način da se izvede na vseh html datotekah in vse dobljene podatke shraniti v eno velik seznam slovarjev. To sem dosegel z enostavno for zanko, ampak je bilo treba dodati import os za uporabo os.path. Tu sem se uprl na Claude za napotek in nato zapisal potrebno zanko. Kot zadnji del pridobivanja ustreznega seznama avtomobilov je bila deduplikacija. Zaradi načina izbora podatkov je obstajala velika možnost da se nekateri oglasi ponovijo. Pred opravljeno deduplikacijo je bilo vseh avtomobilov v seznamu 1480, po pa 1409. Torej je vzorec še vedno dovolj velik za opravljanje željenih primerjav in analiz. 