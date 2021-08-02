import mangadex

api = mangadex.Api()

boruto_last_chapter_info = api.get_manga_list(title = "Boruto")

print(boruto_last_chapter_info)



# import requests


# body = {
# "username": "itachipower",
# "password": "itachi",
# "email": "dp754@scarletmail.rutgers.edu"
# }

# a = requests.post("https://api.mangadex.org/account/create", data=body)


# print(a.content)


# Import the MangaDexPy library
import MangaDexPy
cli = MangaDexPy.MangaDex()
# cli.login("username", "password")

# Get manga with id b9797c5b-642e-44d9-ac40-8b31b9ae110a.
manga = cli.get_manga("32d76d19-8a05-4db0-9fc2-e0b0648fe9d0")
# print(manga.title + "'s latest volume:")
print(manga.last_volume)
# print(manga.title + "'s latest chapter:")
print(manga.last_chapter)




import requests
from bs4 import BeautifulSoup
import urllib.request

def textsearch():
  #manga_file = open("managa.txt").readlines()
  ##assuming your text file has 3 titles
  manga_file = ["Vinland Saga"]

  manga_html = "https://www.mangaupdates.com/search.html"

  manga_page = requests.get(manga_html)

#   manga_page = urllib.request.urlopen(manga_html)

  found = 0

  soup = BeautifulSoup(manga_page.content, 'html.parser')
  ##use BeautifulSoup to parse the section of interest out
  ##use 'inspect element' in Chrome or Firefox to find the interesting table
  ##in this case the data you are targeting is in a <div class="alt"> element
  chapters = soup.findAll("div", attrs={"class":"alt p-1"})
  ##chapters now contains all of the sections under the dates on the page
  ##so we iterate through each date to get all of the titles in each
  ##<tr> element of each table

  print(chapters)

  for dated_section in chapters:
      rows = dated_section.findAll("tr")
      for r in rows:
          title = r.td.text
          print(title)
          #url = r.td.a.href
          if title in manga_file:
              found +=1 
              print("New chapter found")
              print(r)
  if found >0:
      print("Found a total of title")
  else:
      print("No chapters found")


textsearch()


import mangadex
api = mangadex.Api()

x = api.manga_feed(id="46e530ce-0766-4cbd-b005-5e6fb0ba5e71")


print(sorted(x, key = lambda x: x.createdAt))

# print(x[4].data)