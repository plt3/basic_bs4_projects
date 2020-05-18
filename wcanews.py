import requests
import bs4


def preparesoup(url):
    res = requests.get(url)
    res.raise_for_status()

    wcasoup = bs4.BeautifulSoup(res.text, 'html.parser')
    return wcasoup


def onlytext(soup):
    paragraphs = soup.select('div[class="panel-body"] > p, div[class="panel-body"] > ul')
    for tag in paragraphs:
        print(tag.get_text(), file=newsfile)


while True:
    try:
        userinterest = input('\nEnter keywords of news to get from the WCA: ')
        print()

        cubesoup = preparesoup('https://www.worldcubeassociation.org')

        allnews = cubesoup.select('div[class="panel panel-default panel-wca-post"]')

        interestedlist = []

        newsfile = open('WCA news digest.txt', 'w')
        print('WCA news digest for keyword ' + userinterest, end=':\n\n\n', file=newsfile)

        for story in allnews:
            if userinterest in story.get_text().lower():
                if interestedlist != []:
                    print('\n\n----------------------\n\n', file=newsfile)

                interestedlist.append(1)

                title = story.select('h3[class="panel-title"] > a')[0]
                print(title.get_text(), file=newsfile)
                fullpagelink = 'https://www.worldcubeassociation.org' + title.get('href')
                print(fullpagelink + '\n', file=newsfile)

                if 'Read more' in story.get_text():
                    longpage = preparesoup(fullpagelink)
                    onlytext(longpage)
                else:
                    onlytext(story)

        if interestedlist == []:
            raise ValueError('No results found. Please try again.')

        newsfile.close()
        print(str(len(interestedlist)) + ' posts found that matched your interests. Look for a file')
        print('named "WCA news digest.txt" in your current directory. ')
        break

    except ValueError as e:
        print(e)
