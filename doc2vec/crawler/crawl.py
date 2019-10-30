import requests
from bs4 import BeautifulSoup

from tqdm import tqdm

def crawl(opt):
    url = opt.url
    res = requests.get(url)
    txt = res.text
    soup = BeautifulSoup(txt, "lxml")
    all_p = soup.find_all('p', 'left')
    papers = {}
    for paper in tqdm(all_p):
        title = paper.find('a').text.strip()
        assert title != 'PDF'
        link = paper.find('a')['href']
        res2 = requests.get(link)
        soup2 = BeautifulSoup(res2.text, 'lxml')
        authors = soup2.find('div', 'main_entry').find_all('span', 'name')
        authors = [i.text.strip() for i in authors]
        section = soup2.find('div', 'entry_details')
        section = section.find('div','item issue').find_all('div','value')[-1].text.strip()
        abstract = soup2.find('div', 'item abstract')
        abstract = abstract.find('p').text
        if not isinstance(abstract, str):
            ipdb.set_trace()
        papers[title] = {'abstract':abstract,
            'authors':authors,
            'section':section
            }
    return papers
