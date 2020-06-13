import bs4
import requests
import pyinputplus as pyip


def prepareSoup(site):
    page = requests.get(site)
    page.raise_for_status()

    soup = bs4.BeautifulSoup(page.text, 'lxml')

    return soup


def compsAndResults():
    print('Enter WCA ID:', end=' ')

    while True:
        wca = input().upper()
        print(f'Searching database for {wca}...\n')

        cuberPage = prepareSoup(f'https://wcadb.net/person.php?id={wca.upper()}')
        cuberName = cuberPage.find('h1', class_='h3 text-center').text

        if cuberName != '':
            break

        print(f'No competitor found for WCA ID {wca}. Try again:', end=' ')

    compsTab = cuberPage.find('div', id='competitions_tab')
    compsTags = compsTab.select('div[class="panel panel-default"]')

    compDict = {c.find('strong').text: i for i, c in enumerate(compsTags)}

    if len(list(compDict.keys())) == 1:
        compChoice = list(compDict.keys())[0]
    else:
        compChoice = pyip.inputMenu(list(compDict.keys()), numbered=True)

    compTag = compsTags[compDict[compChoice]]

    linkTag = compTag.select_one('span[class="pull-right"] a')
    compInfo = (compChoice, 'https://wcadb.net' + linkTag.get('href'))

    eventsRows = compTag.select('tbody tr')

    eventsAndRounds = {}

    for row in eventsRows:
        data = row.find_all('td')
        eventName = data[0].find('a').text
        round = data[1].text
        times = [data[i].text for i in range(5, 10) if len(data[i].text) > 0]

        if len(eventName) > 0:
            lastEvent = eventName
            eventsAndRounds[eventName] = {round: times}
        else:
            eventsAndRounds[lastEvent][round] = times

    return {(cuberName, wca): {compInfo: eventsAndRounds}}


def chooseRound(infoDict):
    events = list(list(infoDict.values())[0].values())[0]
    print()

    if len(list(events.keys())) == 1:
        eventChoice = list(events.keys())[0]
    else:
        eventChoice = pyip.inputMenu(list(events.keys()), numbered=True)

    rounds = events[eventChoice]
    roundsList = list(rounds.keys())

    if len(roundsList) > 1:
        print()
        roundChoice = pyip.inputMenu(roundsList, numbered=True)
    else:
        roundChoice = roundsList[0]

    times = rounds[roundChoice]
    compTup = list(list(infoDict.values())[0].keys())[0]
    comp = compTup[0]
    compLink = compTup[1]
    name = list(infoDict.keys())[0][0]

    return (compLink, eventChoice, roundChoice, name, comp, times)


def findScrambles(dataTuple):
    link, event, round = dataTuple[:3]
    print('\nLocating scrambles. This may take several seconds for larger competitions...')

    fullSoup = prepareSoup(link)
    scramblesPage = fullSoup.select_one('div[id="scrambles_tab"]')
    eventRounds = scramblesPage.find_all('div', class_='panel panel-default')

    for cube in eventRounds:
        if event in cube.text and round in cube.text:
            scrambleTable = cube.find('tbody')
            break

    scramblesDict = {}

    for row in scrambleTable.find_all('tr'):
        data = row.find_all('td')

        if 'Ex' not in data[1].text:
            if data[0].text not in scramblesDict:
                scramblesDict[data[0].text] = [data[2].text]
            else:
                scramblesDict[data[0].text].append(data[2].text)

    return scramblesDict


def writeToFile(infoTuple, scrambles):
    event, round, name, comp, times = infoTuple[1:]
    filename = f'{event} {round}.txt'

    with open(filename, 'w') as f:
        f.write(f'{name} {comp} {event} {round} scrambles and times:\n\n\n')

        for group, scramsList in scrambles.items():
            f.write(f'Group {group}:\n\n')

            for index, scram in enumerate(scramsList):
                f.write(f'{index + 1} ({times[index]}): {scram}\n')

            f.write('\n')

    print(f'\nScrambles retrieved. Look for "{filename}" in your current directory.')


def main():
    allDict = compsAndResults()
    eventTup = chooseRound(allDict)
    scrams = findScrambles(eventTup)
    writeToFile(eventTup, scrams)

    # give possibility to export to a csv/xlsx file
    # give option to get all scrambles for all rounds of an event


main()
