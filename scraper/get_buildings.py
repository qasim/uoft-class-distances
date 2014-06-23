from bs4 import BeautifulSoup
import pprint
html = open('buildings.html', 'r').read()
soup = BeautifulSoup(html)
buildings = soup.find_all('dl')
data = {}
for building in buildings:
  splitter = building.dt.get_text().encode('utf-8').split(" | ")
  data[building.dd.get_text().encode('utf-8').strip()] = splitter[0]
pprint.pprint(data)
