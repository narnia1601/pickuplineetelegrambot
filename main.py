from bs4 import BeautifulSoup
import requests
import spacy
import re
import markovify
import string

class PickupLine:
    def __init__(self):
        self.linkList = []
        self.urlLen = 22
        self.categoryLinkDict = {}

    def getCategoriesAndLinks(self):
        categories = []
        categoryLinks = []
        url = 'https://pickupline.net'
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')
        for link in soup.find_all('a', class_='_self'):
            text = link.get('href')[self.urlLen:]
            if text not in categoryLinks:
                categoryLinks.append(text)
            if link.text != '':
                categories.append(link.text)
        for i in range(len(categories)):
            self.categoryLinkDict[categories[i]] = categoryLinks[i]

    def writeLines(self, f, line):
        f.write(f'{line}\n')

    def getPickupLines(self):
        self.getCategoriesAndLinks()
        for topic in self.categoryLinkDict:
            f = open(f'{topic}file.txt', 'a')
            url = 'https://pickupline.net'
            url = url + self.categoryLinkDict[topic]
            result = requests.get(url)
            soup = BeautifulSoup(result.text, 'html.parser')
            for link in soup.find_all('a', class_='pt-cv-href-thumbnail'):
                url = link.get('href')
                result = requests.get(url)
                soup = BeautifulSoup(result.text, 'html.parser')
                for line in soup.find_all('td', class_='column-1'):
                    text = line.text
                    self.writeLines(f, text)
