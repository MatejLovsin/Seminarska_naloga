with open("podatki/mercedes_stran1.html", encoding="cp1250") as f:
    html = f.read()

import re
import bs4
juha = bs4.BeautifulSoup(html, 'html.parser')

for oglas in juha.find_all('div', class_="row bg-white position-relative GO-Results-Row GO-Shadow-B"):
    povezava = oglas.find('a')
    url = povezava.get('href')
    if '&display' in url:
        id = int(re.search(r'\d{8}', url).group(0))
    naslov = oglas.find('div', class_="GO-Results-Naziv bg-dark px-3 py-2 font-weight-bold text-truncate text-white text-decoration-none")
    ime = naslov.find('span').get_text()
    print({'id': id, 'ime': ime})