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

        for tbl in soup.find_all('table'):
            for tr in tbl.find_all("tr"):
                data = tr("td")
                if len(data) == 0:
                    continue
                name =  data[0].text.strip()
                version = data[1].text.strip()
                ver_code = version.split(".")
                major = ver_code[0]
                minnor = ver_code[1]
                if not (major.isdecimal() and minnor.isdecimal()):
                    continue
                if (len(ver_code)) == 2:
                    ver_code.append("0")
                latest_rev = int(ver_code[2])
                self.name_dict[name] = list()

                for revision in range(latest_rev, -1, -1):
                    version_code = [
                        major,
                        minnor,
                    ]
                    if revision != 0:
                        version_code.append(str(revision))
                    d = {
                        "name": name,
                        "version": ".".join(version_code)
                    }
                    self.append(d)
                    self.name_dict[name].append(d)

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
