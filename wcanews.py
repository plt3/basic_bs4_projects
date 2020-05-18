import requests
import bs4


def preparesoup(url):
    res = requests.get(url)
    res.raise_for_status()

    wcasoup = bs4.BeautifulSoup(res.text, 'html.parser')
    return wcasoup


def onlytext(soup):
    paragraphs = soup.select('div[class="panel-body"] > p')
    for tag in paragraphs:
        print(tag.get_text())


while True:
    try:
        userinterest = input('\nEnter keywords of news to get from the wca: ')
        print()

        cubesoup = preparesoup('https://www.worldcubeassociation.org')

        allnews = cubesoup.select('div[class="panel panel-default panel-wca-post"]')

        interestedlist = []

        for story in allnews:
            if userinterest in story.get_text().lower():
                interestedlist.append(1)
                title = story.select('h3[class="panel-title"] > a')[0]
                print(title.get_text())
                fullpagelink = 'https://www.worldcubeassociation.org' + title.get('href')
                print(fullpagelink)
                print()

                if 'Read more' in story.get_text():
                    longpage = preparesoup(fullpagelink)
                    onlytext(longpage)
                else:
                    onlytext(story)

                if allnews.index(story) != len(allnews) - 1:
                    print('\n----------------------\n')

        if interestedlist == []:
            raise ValueError('No results found. Please try again.')

        break

    except ValueError as e:
        print(e)
