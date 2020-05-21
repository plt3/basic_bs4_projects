import requests
import bs4


class Competitor:

    aobjlist = []  # not sure objlists are necessary, but could be useful later
    anameslist = []
    bobjlist = []
    bnameslist = []

    def __init__(self, tag, event):
        self.rank = tag.find('td', class_='pos').text.strip()
        self.name = tag.find('td', class_='name').text.strip()
        self.result = tag.find('td', class_='result').text.strip()
        self.country = tag.find('td', class_='country').text.strip()
        self.competition = tag.find('td', class_='competition').text.strip()

        if event == 'a':
            Competitor.aobjlist.append(self)
            Competitor.anameslist.append(self.name)
        else:
            Competitor.bobjlist.append(self)
            Competitor.bnameslist.append(self.name)


def createobjs(url, event):
    eventpage = requests.get(url)
    eventpage.raise_for_status()

    soup = bs4.BeautifulSoup(eventpage.text, 'lxml')

    table = soup.find('tbody')

    competitorelems = table.find_all('tr')

    for elem in competitorelems:
        Competitor(elem, event)


createobjs('https://www.worldcubeassociation.org/results/rankings/555/average', 'a')
createobjs('https://www.worldcubeassociation.org/results/rankings/sq1/single', 'b')

for name in Competitor.anameslist:
    if name in Competitor.bnameslist:
        print(name, end=': ')  # gives names that are in both, but might want to do it with objlists
        print(Competitor.bobjlist[Competitor.bnameslist.index(name)].rank)
