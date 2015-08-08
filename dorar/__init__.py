# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re


class Dorar:
    def __init__(self):
        self.base = "http://dorar.net/"

    def openHadithApi(self, key):
        keyurl = "dorar_api.json?skey="
        key = re.split(" ", key)
        if key:
            src = "+".join(key)
        else:
            src = key
        openurl = requests.get(self.base+keyurl+src).json()

        jsontext = openurl['ahadith']['result']
        return jsontext
    def getHadith(self, jsontext):
        soup = BeautifulSoup(jsontext)
        hadits = soup.findAll("p", "hadith")
        return [x.text for x in hadits]



    def getInfo(self, jsontext):
        soup = BeautifulSoup(jsontext)
        info = soup.findAll("p", "hadith-info")
        info = [x.text for x in info]
        infos = []
        for x in info:
            pattern = re.compile(u"الدرجة")
            ganti = u"   -   الدرجة"
            hasil = re.sub(pattern, ganti, x)
            pattern1 = re.compile(u"	 المحدث")
            ganti1 = u"المحدث"
            hasil1 = re.sub(pattern1, ganti1, hasil)
            infos.append(hasil1)
        return infos

    def searchHadith(self, cari):
        text = self.openHadithApi(cari)
        hadith = self.getHadith(text)
        info = self.getInfo(text)
        hasil = []
        for x in range(len(hadith)):
            y = hadith[x] + "\n" +info[x]
            hasil.append(y)
        return "\n\n".join(hasil)
