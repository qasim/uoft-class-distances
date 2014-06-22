import urllib2
from bs4 import BeautifulSoup
import pprint

url = 'http://www.artsandscience.utoronto.ca/ofr/timetable/winter/sponsors.htm'
html = urllib2.urlopen(url).read().split('<hr>')[0]

soup = BeautifulSoup(html)

urls = []
for link in soup.find_all('a'):
  path = 'http://www.artsandscience.utoronto.ca/ofr/timetable/winter/'
  file = link.get('href').encode('utf-8')
  if '/' in file:
    urls.append(file)
  else:
    urls.append(path + file)

pprint.pprint(urls)
