Novo težavo imam glede cene. Cene so na avtonetu v html zapisane na več različnih načinov. Če ima avto kakšno akcijo potem ima pod ceno zapisano staro in novo ceno. Lahko ima tudi zapisano navadno in posebej ceno s financiranjem. Lahko sploh nima zapisane cene ampak samo pokliči za ceno.

    ponudba = oglas.find('div', class_="GO-Results-Price-Mid")
    for akcija in ponudba.find_all('div'):
        if len(akcija) == 2:
            cena = akcija[1].get_text(strip = True)
        else:
            cena = akcija.get_text(strip = True)
    podatki['cena'] = cena
Moja trenutna koda deluje za večino primerov ampak deluje preveč naivno, kajti ta if pokrije samo navadno možnost in če je akcija kjer je prva cena stara in druga nova, ne predela pa primerov ki sem jih zgoraj naštel in zato tudi vrne napako

  File "c:\Users\matej\UvP\Seminarska\import requests.py", line 22, in <module>
    for akcija in ponudba.find_all('div'):
                  ^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'find_all'
PS C:\Users\matej\UvP\Seminarska> 

Kar si lahko predstavljam ko cena ni določena, oziroma mora obstajati nek drug razlog kajti cena je vedno nekako določena

Ja ampak tu ni en container ki ima obe ceni

                        <div class="GO-Results-Price-TXT-Regular">69.900 €</div>

                            <div class="GO-Results-Price-TXT-BruttoNeto">oz. 57.295 € + DDV(*)</div>

Izgleda podobno kot ta primer. Kako lahko potem uporabim regex. Daj mi kakšen malo bolj konkreten primer



Thought for 24s
- Alright broski — sem ~85% prepričan, da spodnji vzorec pokriva tvoj primer (in podoben "pokliči za ceno" primer, čeprav slednjega nisi prilepil).

Napačna predpostavka: misliš, da moraš najprej najti en skupen kontejner, ki vsebuje obe ceni, in ju nato ločiti po poziciji (indeks 0 = stara, indeks 1 = nova). Ker takega skupnega kontejnerja ni — imaš dva ločena, neodvisna diva na isti ravni (siblinga) — pozicijska logika (len == 2, akcija[1]) nima trdne osnove, na kateri bi lahko gradil.

Rešitev: ne štej elementov, ampak preglej vsakega posebej po vsebini in pobiraj samo tiste, ki dejansko vsebujejo ceno (regex na €), ne glede na to, koliko jih je.

Ločen primer:

python
import re
from bs4 import BeautifulSoup

html = """
<div class="box">
  <div class="cena-redna">69.900 €</div>
  <div class="cena-neto">oz. 57.295 € + DDV(*)</div>
</div>
"""
box = BeautifulSoup(html, 'html.parser').find('div', class_='box')

cene = []
for element in box.find_all('div'):
    besedilo = element.get_text(strip=True)
    m = re.search(r'([\d.]+)\s*€', besedilo)
    if m:
        cene.append(float(m.group(1).replace('.', '')))

print(cene)              # [69900.0, 57295.0]
cena = cene[0] if cene else None   # vzemi PRVO najdeno – ne glede na to, ali jih je 1, 2 ali 0
Kaj počne vsak del:

re.search(r'([\d.]+)\s*€', besedilo) — najde številko (s pikami kot ločili tisočic) tik pred €; vrne None, če ga ni (npr. pri "pokliči za ceno" divu, ki nima €).
.replace('.', '') — odstrani pike (69.900 → 69900), preden pretvoriš v float.
cene seznam raste glede na to, koliko cen dejansko obstaja v tem oglasu — 0 (ni cene), 1 (navadna), 2 (akcija ali +DDV) ali celo 3 (akcija + DDV) — brez da bi to moral vnaprej predvideti.
cene[0] if cene else None — če ni najdene nobene cene (klic za ceno), dobiš None namesto crasha na praznem seznamu.
To še vedno ne loči nujno pravilno "redna cena" od "cena + DDV" — samo vzame prvo najdeno po vrstnem redu v HTML-ju, kar je za tvoj primer verjetno pravilno (redna je vedno prva), a je še vedno rahlo krhko.

Vprašanje zate: v tvojem HTML-ju vidim, da imata dva diva različna imena razredov (Price-TXT-Regular vs Price-TXT-BruttoNeto) — ali bi raje namesto cene[0] iskal specifično po class-u, ki vsebuje "TXT-Regular" (podobno kot Data-Top lambda prej), da si 100% prepričan, da vedno dobiš redno ceno, ne glede na vrstni red v HTML-ju?



Traceback (most recent call last):
  File "c:\Users\matej\UvP\Seminarska\import requests.py", line 23, in <module>
    for akcija in ponudba.find_all('div'):
                  ^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'find_all'

Dobivam to napako. Mislim da je možno da je pri nekaterih primerih cena napisana takoj v tistem uvodnem div in nima nobenih potomcev. Ali mi lahko narediš eno varovalo ki bo ščitilo proti ravno temu.



Thought for 13s
- Alright broski — sem ~85% prepričan, da spodnja varovalka pokrije oba primera, ki ju omenjaš (manjkajoč ponudba in cena brez notranjih divov).

Dva ločena problema, dve varovalki:

ponudba je None — enak vzorec kot vsi tvoji prejšnji NoneType crashi (drugačen/manjkajoč class na nekem tipu oglasa, npr. "pokliči za ceno" ali drugačna postavitev). Rešitev: preveri if ponudba is not None pred vstopom v zanko.
Cena je zapisana neposredno v ponudba, brez notranjih <div> — v tem primeru ponudba.find_all('div') vrne prazen seznam (ne crash, samo 0 elementov), zato tvoja zanka tiho ne najde nič. Rešitev: če je seznam prazen, preveri besedilo ponudba samega.
python
ponudba = oglas.find('div', class_="GO-Results-Price-Mid")

cene = []
if ponudba is not None:
    deli = ponudba.find_all('div') or [ponudba]   # če ni notranjih divov, preveri kar ponudba sam
    for del_ in deli:
        besedilo = del_.get_text(strip=True)
        m = re.search(r'([\d.]+)\s*€', besedilo)
        if m:
            cene.append(float(m.group(1).replace('.', '')))

podatki['cena'] = cene[0] if cene else None
Zakaj deli = ponudba.find_all('div') or [ponudba] deluje: prazen seznam [] je v Pythonu "falsy", zato or pade nazaj na desno stran in uporabi seznam z enim elementom — samim ponudba — namesto praznega seznama. Tako isti for deluje ne glede na to, ali je struktura ugnezdena ali ne.

Ker si prej opozoril tudi na "Price-Mid" vs "Top-Price-Mid" vzorec — glede na to, da si ta lambda trik že enkrat uporabil za Data-Top, ali naj ponudba = oglas.find('div', class_="GO-Results-Price-Mid") takoj zamenjava z class_=lambda c: c and 'Price-Mid' in c, da preventivno pokriješ tudi TOP oglase, še preden dobiš tretjo enako napako?