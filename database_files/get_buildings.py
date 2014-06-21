from bs4 import BeautifulSoup
import pprint
html = open('buildings.html', 'r').read()
soup = BeautifulSoup(html)
buildings = soup.find_all('dl')
data = {}
for building in buildings:
  data[building.dt.get_text().encode('utf-8').split(" | ")[1]] = building.dd.get_text().encode('utf-8').strip()
pprint.pprint(data)
