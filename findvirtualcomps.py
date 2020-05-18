import requests
import bs4

userend = int(input('Enter how many virtual competitions you would like to get: '))

res = requests.get('https://www.worldcubeassociation.org/posts/unofficial-online-competitions')
res.raise_for_status()

wcasoup = bs4.BeautifulSoup(res.text, 'html.parser')

comps = wcasoup.select('div[class="panel-body"] > ul > li')

with open('virtualcomps.txt', 'w') as f:
    f.write('Virtual competitions coming up:\n\n')

    for comp in comps[:userend]:
        f.write(comp.get_text() + '\n')
        f.write(comp.select('a')[0].get('href') + '\n\n')
