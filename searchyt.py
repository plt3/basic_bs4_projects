import requests
import bs4
import webbrowser

usersearch = input('What would you like to search for on YouTube? ').split()
urlstr = 'https://www.youtube.com/results?search_query=' + '+'.join(usersearch)

gottenpage = requests.get(urlstr)
gottenpage.raise_for_status()

ytsoup = bs4.BeautifulSoup(gottenpage.text, 'html.parser')

rawlist = ytsoup.select('a', class_="yt-simple-endpoint style-scope ytd-video-renderer")

vidlist = []
urllist = []

for elem in rawlist:
    elemurl = str(elem.get('href'))
    if elemurl.startswith('/watch') and elemurl not in urllist:
        vidlist.append(elem)

    urllist.append(elemurl)

for video in vidlist[:4]:
    print(video)
    print()
    print(video.get('href'))
    print()
    print(video.attrs)
    print()
    print('-----------------------')
    print()
