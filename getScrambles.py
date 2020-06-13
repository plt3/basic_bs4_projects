import bs4
import requests
import pyinputplus as pyip


def prepareSoup(site):
    page = requests.get(site)
    page.raise_for_status()

    soup = bs4.BeautifulSoup(page.text, 'lxml')

    return soup


def allComps(wcaId):
    cuberPage = prepareSoup(f'https://wcadb.net/person.php?id={wcaId.upper()}')

    compsTab = cuberPage.find('div', id='competitions_tab')

    compsTags = compsTab.select('div[class="panel panel-default"] span[class="pull-right"] a')

    return {comp.text.lower(): (comp.get('href'), comp.text) for comp in compsTags}


def getCompEvents(wcaId, fullSoup):
    personsTab = fullSoup.find('div', id='persons_tab')
    cuberResults = personsTab.select('div[class="panel panel-default"]')

    for index, cuber in enumerate(cuberResults):
        wcaLink = cuber.select_one('span[class="pull-right"] a').get('href')
        if wcaId in wcaLink.upper():
            indivTag = cuberResults[index]
            break

    eventsRows = indivTag.select('tbody tr')

    eventsAndRounds = {}

    for row in eventsRows:
        data = row.find_all('td')
        eventName = data[0].text
        round = data[1].text

        if len(eventName) > 0:
            lastEvent = eventName
            eventsAndRounds[eventName] = [round]
        else:
            eventsAndRounds[lastEvent].append(round)

    return eventsAndRounds


def findScrambles(event, round, fullSoup):
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


def writeToFile(wca, infoTuple, scrambles):
    comp, event, round = infoTuple

    with open(f'{event} {round}.txt', 'w') as f:
        f.write(f'{comp} {event} {round} scrambles:\n\n\n')

        for group, scramsList in scrambles.items():
            f.write(f'Group {group}:\n\n')

            for index, scram in enumerate(scramsList):
                f.write(f'{index + 1}: {scram}\n')

            f.write('\n')


def main():
    wca = input('Enter WCA ID: ').upper()

    while True:
        print(f'Searching database for {wca}...')
        possDict = allComps(wca)

        if len(possDict) != 0:
            break

        wca = input(f'No competitions found for WCA ID {wca}. Try again: ').upper()

    print('Enter competition you\'d like to retrieve scrambles for (or enter "help" for all competitions):', end=' ')

    while True:
        comp = input()

        if comp == 'help':
            print()
            for event in possDict.values():
                print(event[1])

            print('\nEnter competition:', end=' ')
            continue

        if comp.lower() not in possDict.keys():
            print(f'Sorry, but no competition "{comp}" found for WCA ID "{wca}".')
            print('Try again:', end=' ')
            continue

        break

    print('Parsing competitors. This may take several seconds for large competitions...\n')
    compSoup = prepareSoup('https://wcadb.net' + possDict[comp.lower()][0])
    cuberEvents = getCompEvents(wca, compSoup)
    eventChoice = pyip.inputMenu(list(cuberEvents.keys()), lettered=True)
    print()

    if len(cuberEvents[eventChoice]) > 1:
        roundChoice = pyip.inputMenu(cuberEvents[eventChoice], lettered=True)
    else:
        roundChoice = cuberEvents[eventChoice][0]

    roundScrambles = findScrambles(eventChoice, roundChoice, compSoup)

    dataTuple = (possDict[comp.lower()][1], eventChoice, roundChoice)

    writeToFile(wca, dataTuple, roundScrambles)

    print(f'Scrambles retrieved. Look for "{eventChoice} {roundChoice}.txt" in your current directory.')

    # print times competitor got after each scramble (and competitor name too at top)
    # give possibility to export to a csv/xlsx file
    # give option to get all scrambles for all rounds of an event


main()
