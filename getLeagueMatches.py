from bs4 import BeautifulSoup


import requests


page = requests.get('https://watch.lolesports.com/schedule?leagues=lcs,lec,lck')
soup = BeautifulSoup(page.content, 'html.parser')

html = list(soup.children)[1]
print(soup.find_all('p', class_='results-label'))