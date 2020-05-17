import requests
import bs4
import re
import os


def preparesoup(site):
    xkcdpage = requests.get(site)
    xkcdpage.raise_for_status()

    xkcdsoup = bs4.BeautifulSoup(xkcdpage.text, 'html.parser')

    return xkcdsoup


def download_img(url):
    fullpage = preparesoup(url)

    images = fullpage.select('div[id="comic"] > img')

    comicimage = images[0].get('src')

    imagepage = requests.get('https://xkcd.com' + comicimage)

    numberpattern = re.compile(r'(\d+)')
    numbers = numberpattern.search(url)

    filename = 'xkcd' + str(numbers.group()) + '.jpg'

    with open('xkcd comics/' + filename, 'wb') as f:
        for chunk in imagepage.iter_content(100000):
            f.write(chunk)


def firstlink():
    fullpage = preparesoup('https://xkcd.com')
    tag = fullpage.select('div[id="middleContainer"]')
    midstr = tag[0].get_text()

    linkpattern = re.compile(r'https://xkcd.com/\d+/')
    found = linkpattern.search(midstr)

    return found.group()


def prevlink(url):
    fullpage = preparesoup(url)

    prev = fullpage.select('a[rel="prev"]')

    return 'https://xkcd.com' + prev[0].get('href')


def main():
    useramt = int(input('How many xkcd comics would you like to download? '))
    print()

    os.makedirs('xkcd comics')

    link = firstlink()
    numpattern = re.compile(r'\d+')

    for i in range(1, useramt + 1):
        number = numpattern.search(link)
        print('Downloading xkcd number ' + number.group(), end=':\n')
        download_img(link)
        prevone = prevlink(link)
        link = prevone

    print('\nDone. Look for an "xkcd comics" folder in your current directory.')


main()
