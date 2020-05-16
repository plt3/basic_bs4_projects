import requests
import bs4
import webbrowser

usersearch = input('\nWhat would you like to search for on YouTube? ').split()
urlstr = 'https://www.youtube.com/results?search_query=' + '+'.join(usersearch)

gottenpage = requests.get(urlstr)
gottenpage.raise_for_status()

ytsoup = bs4.BeautifulSoup(gottenpage.text, 'html.parser')

rawlist = ytsoup.select('a[href^="/watch"][title]')

print('\n%d results found. How many would you like to display?' % len(rawlist), end=' ')
useramt = int(input())
print()

for i in range(useramt):
    print()
    print(str(i + 1) + '. ' + rawlist[i].get('title'))

usernum = int(input('\n\nEnter number of video you would like to watch: '))

chosenurl = 'https://www.youtube.com' + rawlist[usernum - 1].get('href')
webbrowser.open(chosenurl)
