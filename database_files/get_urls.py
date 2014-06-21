import pprint

def getBetween(strSource, strStart,strEnd):
    start = strSource.find(strStart) + len(strStart)
    end = strSource.find(strEnd,start)
    return strSource[start:end]

file = open('list2014.html', 'r')

html = file.readlines()
links = []
for line in html:
  if "<a href=" in line:
    link = 'http://www.artsandscience.utoronto.ca/ofr/timetable/winter/' + getBetween(line, '<a href=', '>').replace('"', '')
    links.append(link)
pprint.pprint(links)
