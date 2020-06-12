import requests
import bs4
import re
import os
import time
import threading

# NOTE: like actually don't run this with more than 500 requests. That's not very nice to XKCD


def preparesoup(site):
    xkcdpage = requests.get(site)
    xkcdpage.raise_for_status()

    xkcdsoup = bs4.BeautifulSoup(xkcdpage.text, 'lxml')

    return xkcdsoup


def download_img(url):
    fullpage = preparesoup(url)

    images = fullpage.select('div[id="comic"] img')

    comicimage = images[0].get('src')

    imagepage = requests.get('https://xkcd.com' + comicimage)

    numberpattern = re.compile(r'(\d+)')
    numbers = numberpattern.search(url)

    filename = 'xkcd' + str(numbers.group()) + '.jpg'

    with open('xkcd comics/' + filename, 'wb') as f:
        for chunk in imagepage.iter_content(100000):
            f.write(chunk)


def firstNum():
    fullpage = preparesoup('https://xkcd.com')
    tag = fullpage.select('div[id="middleContainer"]')
    midstr = tag[0].get_text()

    linkpattern = re.compile(r'(https://xkcd.com/)(\d+)')
    found = linkpattern.search(midstr)

    return int(found.groups()[1])


def fullDownload(start, stop):
    for i in range(start, stop, -1):
        link = f'https://xkcd.com/{i}/'
        print('Downloading xkcd number ' + str(i), end=':\n')
        download_img(link)


def main():
    userAmt = int(input('How many xkcd comics would you like to download? '))
    print()
    start = time.time()

    os.makedirs('xkcd comics')

    begin = firstNum()

    oldNum = begin

    threadList = []

    for i in range(begin - 10, begin - userAmt, - 10):
        threadObj = threading.Thread(target=fullDownload, args=[oldNum, i])
        threadObj.start()
        threadList.append(threadObj)
        oldNum = i

    fullDownload(oldNum, begin - userAmt)

    for item in threadList:
        item.join()

    end = time.time()
    print('\nDone. Look for an "xkcd comics" folder in your current directory.')
    print(f'done in {end - start} seconds')


main()
