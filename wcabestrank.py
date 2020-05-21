import requests
import bs4


class Competitor:

    aobjlist = []
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


def findbest():
    overlaplist = []

    for cuber in Competitor.aobjlist:
        if cuber.name in Competitor.bnameslist:
            arank = int(cuber.rank)
            brank = int(Competitor.bobjlist[Competitor.bnameslist.index(
                cuber.name)].rank)
            overlaplist.append(((cuber.name, arank + brank)))

    overlaplist.sort(key=lambda tup: tup[1])

    return overlaplist[0]


def getuserevents():
    eventlist = ['333', '222', '444', '555', '666', '777', '333bf', '333fm',
                 '333oh', 'clock', 'minx', 'pyram', 'skewb', 'sq1', '444bf',
                 '555bf', '333mbf']

    typelist = ['single', 'average']

    inputlist = []

    firstcounter = 0
    secondcounter = 0
    thirdcounter = 0

    while True:
        try:
            if firstcounter == 0:
                eventa = input('Enter first event (or enter "events" to see options): ')

                if eventa == 'events':
                    print('Events: ' + ', '.join(eventlist))
                    continue
                elif eventa not in eventlist:
                    raise ValueError

                inputlist.append(eventa)
                eventlist.remove(eventa)
                firstcounter = 1

            if secondcounter == 0:
                typea = input('Enter "single" or "average": ')

                if typea not in typelist:
                    raise Exception

                inputlist.append(typea)
                secondcounter = 1

            if thirdcounter == 0:
                eventb = input('Enter second event (or enter "events" to see options): ')

                if eventb == 'events':
                    print('Events: ' + ', '.join(eventlist))
                    continue
                elif eventb not in eventlist:
                    raise ValueError

                inputlist.append(eventb)
                thirdcounter = 1

            typeb = input('Enter "single" or "average": ')

            if typeb not in typelist:
                raise Exception

            inputlist.append(typeb)
            break

        except ValueError:
            if firstcounter == 0:
                print(f'"{eventa}" not an available event. Please try again.')
            else:
                print(f'"{eventb}" not an available event. Please try again.')
        except Exception:
            print('Enter "single" or "average". Please try again.')

    return inputlist


def main():
    print()

    userchoices = getuserevents()

    urla = 'https://www.worldcubeassociation.org/results/rankings/' + '/'.join(
        userchoices[:2])

    urlb = 'https://www.worldcubeassociation.org/results/rankings/' + '/'.join(
        userchoices[2:])

    createobjs(urla, 'a')
    createobjs(urlb, 'b')

    name, rank = findbest()
    placea = ' '.join(userchoices[:2])
    placeb = ' '.join(userchoices[2:])

    print(f'\n{name} is the cuber with the best sum of {placea} and {placeb}'
          f' ranks, with a sum of {rank}.')


main()
