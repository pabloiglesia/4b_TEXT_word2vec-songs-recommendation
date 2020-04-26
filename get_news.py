import requests
from bs4 import BeautifulSoup
from functools import reduce
import re
import pandas as pd
import time

def extract_new(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    title = soup.find("h1").get_text()
    content = soup.find("div", {"class": "ue-l-article__body"})
    ps = content.find_all("p")
    text = [p.get_text() for p in content.find_all("p")]
    text = reduce(lambda a,b: a+b,text)

    return text[:-45], title


def getLinks(url,sufix):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')

    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^https://www.elmundo.es/{}".format(sufix))}):
        links.append(link.get('href'))

    return links

sections = [
    ['espana','https://www.elmundo.es/espana.html?intcmp=MENUHOM24801&s_kw=espana'],
    ['opinion','https://www.elmundo.es/opinion.html?intcmp=MENUHOM24801&s_kw=opinion'],
    ['economia','https://www.elmundo.es/economia.html?intcmp=MENUHOM24801&s_kw=economia'],
    ['internacional','https://www.elmundo.es/internacional.html?intcmp=MENUHOM24801&s_kw=internacional'],
    ['deportes','https://www.elmundo.es/deportes.html?intcmp=MENUHOM24801&s_kw=deportes'],
    ['cultura','https://www.elmundo.es/cultura.html?intcmp=MENUHOM24801&s_kw=cultura'],
    ['television','https://www.elmundo.es/television.html?intcmp=MENUHOM24801&s_kw=television'],
    ['tecnologia','https://www.elmundo.es/tecnologia.html?intcmp=MENUHOM24801&s_kw=tecnologia'],
    ['ciencia-y-salud','https://www.elmundo.es/ciencia-y-salud.html?intcmp=MENUHOM24801$s_kw=ciencia-salud'],

]
news = []
for section in sections:
    print("Recopilando {}".format(section[0]))
    links =  getLinks(section[1],section[0])
    for link in links:
        try:
            text, title = extract_new(link)
            news.append([section[0], section[1], link, title.replace('|', ' ').replace('\n', ' '), text.replace('|', ' ').replace('\n', ' ')])
        except:
            pass

df = pd.DataFrame(news, columns =['SECTION', 'SECTION_URL', 'NEW_URL', 'NEW_TITLE', 'NEW'])
df.to_csv('noticias.csv', index=False, sep='|')