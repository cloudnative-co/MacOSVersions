import requests
import bs4
from bs4 import BeautifulSoup
import json


class Versions(list):

    name_dict = dict()


    def __init__(self):
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " \
            + "AppleWebKit/537.36 (KHTML, like Gecko) " \
            + "Chrome/70.0.3538.77 Safari/537.36"
        headers = {'User-Agent': ua}
        session = requests.Session()
        url = "https://support.apple.com/en-us/HT201260"
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        names=[]
        for h2 in soup.find_all("h2"):
            if h2.text == "Check About This Mac":
                continue
            if h2.text == "Earlier versions of OS X":
                break
            names.append(h2.text)
            self.name_dict[h2.text] = list()

        count = 0
        for tbl in soup.find_all('table'):
            name = names[count]
            for tr in tbl.find_all("tr"):
                data = tr("td")
                if len(data) == 0:
                    continue
                d = {
                    "name": name,
                    "version": data[0].text.strip(),
                    "build": data[1].text.strip()
                }
                self.append(d)
                self.name_dict[name].append(d)

            count = count + 1

    def name(self, name: str = None):
        if name is None:
            return self.name_dict
        return self.name_dict[name]

    def latest(self, name: str = None):
        if name is None:
            return self[0]
        return self.name_dict[name][0]

    def oldest(self, name: str = None):
        if name is None:
            return self[-1]
        return self.name_dict[name][-1]

    def names(self):
        return self.name_dict.keys()
