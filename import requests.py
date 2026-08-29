with open("podatki/audi_stran1.html", encoding="cp1250") as f:
    html = f.read()

import re
import bs4
juha = bs4.BeautifulSoup(html, 'html.parser')

for povezava in juha.find_all('a'):
    url = povezava.get('href')
    if 'details.asp?' in url:
        ime = povezava.string
        id = int(re.search(r'\d{8}', url).group(0))
        print({'id': id, 'ime': ime})