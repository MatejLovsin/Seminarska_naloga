with open("podatki/mercedes_stran1.html", encoding="cp1250") as f:
    html = f.read()

import re
import bs4


def izlusci_avte(juha):
    rezultati = []
    for oglas in juha.find_all('div', class_="row bg-white position-relative GO-Results-Row GO-Shadow-B"):
        podatki = {}

# dodeljevanje unikatnega id, vsakemu oglasu

        id = None   # zagotovimo, da se id ne ponovi, če ni najden v URL-ju
        povezava = oglas.find('a')
        url = povezava.get('href')
        if '&display' in url:
            id = int(re.search(r'\d{8}', url).group(0))

        podatki['id'] = id

# dodajanje imena

        naslov = oglas.find('div', class_="GO-Results-Naziv bg-dark px-3 py-2 font-weight-bold text-truncate text-white text-decoration-none")
        ime = naslov.find('span').get_text()

        podatki['ime'] = ime

# cena

        ponudba = oglas.find('div', class_="GO-Results-Price-Mid")

        cene = []
        if ponudba is not None:
            deli = ponudba.find_all('div') or [ponudba]   # če ni notranjih divov, preveri kar ponudba sam
            for del_ in deli:
                besedilo = del_.get_text(strip=True)
                m = re.search(r'([\d.]+)\s*€', besedilo)
                if m:
                    cene.append(int(m.group(1).replace('.', '')))

        podatki['cena'] = cene[0] if cene else None

# pridobivanje tehničnih podatkov o vsakem avtu. Data mora razlikovati med podatki pri top ponudbah in mobilni verziji predstavitve podatkov
    
        data = oglas.find('div', class_=lambda c: c and 'Data-Top' in c and 'd-none' not in c)
        tabela = data.find('table')
        for vrstica in tabela.find_all('tr'):
            celica = vrstica.find_all('td')
            if len(celica) == 2:
                kljuc = celica[0].get_text(strip = True)
                vrednost = celica[1].get_text(strip = True)
                podatki[kljuc] = vrednost
    
        rezultati.append(podatki)
    return rezultati


# zanka, čez vse datoteke s podatki, vrne velik seznam vsi_avti

import os

vsi_avti = []
for ime_datoteke in os.listdir('podatki'):
    pot = os.path.join('podatki', ime_datoteke)
    with open(pot, encoding='cp1250') as f:
        soup = bs4.BeautifulSoup(f.read(), 'html.parser')
    vsi_avti.extend(izlusci_avte(soup))

# deduplikacija glede na id avta

unikatni = {}
for avto in vsi_avti:
    unikatni[avto['id']] = avto
koncni_seznam = list(unikatni.values())

print(koncni_seznam[:10])

# pretvorba v csv

import csv
import pandas as pd

df = pd.DataFrame(koncni_seznam)
df.to_csv("avti.csv", index=False, encoding="utf-8-sig")