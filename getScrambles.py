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
    roundsList.reverse()

    if len(roundsList) > 1:
        roundsList.append('Get scrambles for all rounds')
        print()
        rawInp = pyip.inputMenu(roundsList, numbered=True)

        if rawInp == 'Get scrambles for all rounds':
            roundChoice = roundsList[:-1]
        else:
            roundChoice = [rawInp]
    else:
        roundChoice = [roundsList[0]]

    times = [rounds[i] for i in roundChoice]
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

    try:
        eventRounds = scramblesPage.find_all('div', class_='panel panel-default')
    except AttributeError:
        print('Sorry, but wcadb.net has no scrambles for this competition.')
        exit()

    fullDict = {}

    for ro in round:
        for cube in eventRounds:
            title = cube.find('a', class_='list-group-item').text.split()

            if f'{event} {ro}'.split() == title:
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

        fullDict[ro] = scramblesDict

    return fullDict


def writeToFile(infoTuple, scrambles):
    event, round, name, comp, times = infoTuple[1:]

    if len(round) == 1:
        filename = f'{event} {round[0]}.txt'
    else:
        filename = f'{event} all rounds.txt'

    with open(filename, 'w') as f:
        f.write(f'{name} {comp} {event} scrambles and times:\n')

        for bigInd, (iRound, groupScram) in enumerate(scrambles.items()):
            f.write(f'\n\n\n{iRound}:\n')

            for group, scramsList in groupScram.items():
                f.write(f'\nGroup {group}:\n\n')

                for index, scram in enumerate(scramsList):
                    f.write(f'{index + 1} ({times[bigInd][index]}): {scram}\n')

    print(f'\nScrambles retrieved. Look for "{filename}" in your current directory.')


def main():
    allDict = compsAndResults()
    eventTup = chooseRound(allDict)
    scrams = findScrambles(eventTup)
    writeToFile(eventTup, scrams)

    # give possibility to export to a csv/xlsx file
    # try to find group with pypdf2


main()
