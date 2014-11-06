import os
import pprint
import MySQLdb
from bs4 import BeautifulSoup

c = db.cursor()

#empty db
c.execute('''DROP TABLE data''')
db.commit()
c.execute('''
CREATE TABLE data (
   id INT NOT NULL AUTO_INCREMENT,
   name VARCHAR(100) NOT NULL,
   course_code VARCHAR(100) NOT NULL,
   session_code VARCHAR(100) NOT NULL,
   time VARCHAR(255) NOT NULL,
   location_name VARCHAR(255) NOT NULL,
   location VARCHAR(255) NOT NULL,
   PRIMARY KEY ( id )
);
''')
db.commit()

pages = os.listdir('courses_2014')
for page in pages:
  file = open('courses_2014/' + page, 'r')
  html = file.read()
  soup = BeautifulSoup(html)
  course_table = soup.table
  trs = course_table.find_all('tr')
  last_data = ['', '', '', '', '', '' , '', '']
  if page == 'assem.html':
    course_code = ''
    for tr in trs:
      tds = tr.find_all('td')
      if len(tds) == 1 and len(tds[0].find_all('div')) == 0:
        title = tds[0].get_text()
        if ':' in title[:10]:
          #course code found
          course_code = title[:9]
      elif len(tds) in [5, 6]:
        data = []
        for td in tds:
          text = td.get_text().encode('utf-8')
          if text == '\xc2\xa0':
            text = ''
          data.append(text)
        if 'Section' not in data[0] and data[3].lower() not in ['', 'tba']:
          if data[0] == '':
            data[0] = last_data[0]
          if ' ' in data[3]:
            data[3] = data[3].split(' ')[0]
          name = course_code + ' ' + data[0]
          location = ''
          if name in locations.keys():
            location = locations[name]
          else:
            if course_code[:6] in locations2.keys():
              location = locations2[course_code[:6]]
            else:
              if course_code[:3] in locations3.keys():
                location = locations3[course_code[:3]]
          if location != '':
            location_name = building_names[location]
            db_entry = (name, course_code, data[0], data[3], location_name, location)
            c.execute("INSERT INTO data (name, course_code, session_code, time, location_name, location) VALUES (%s, %s, %s, %s, %s, %s)", db_entry)
            #push to DB
            #print db_entry
          last_data = data[:]
  else:
    for tr in trs:
      tds = tr.find_all('td')
      if len(tds) in [9, 10]:
        data = []
        for td in tds:
          text = td.get_text().encode('utf-8')
          if text == '\xc2\xa0':
            text = ''
          data.append(text)
        if 'Course' not in data[0] and data[5].lower() not in ['', 'tba']:
          if data[0] == '':
            data[0] = last_data[0]
          if data[1] == '':
            data[1] = last_data[1]
          if data[3] == '':
            data[3] = last_data[3]
          if ' ' in data[5]:
            data[5] = data[5].split(' ')[0]
          data[1] = data[1][:1]
          data[3] = data[3][:5]
          name = data[0] + ' ' + data[3]
          location = ''
          if name in locations.keys():
            location = locations[name]
          else:
            if data[0][:6] in locations2.keys():
              location = locations2[data[0][:6]]
            else:
              if data[0][:3] in locations3.keys():
                location = locations3[data[0][:3]]
          if location != '':
            name = data[0] + data[1] + ' ' + data[3]
            location_name = building_names[location]
            db_entry = (name, data[0] + data[1], data[3], data[5], location_name, location)
            #print db_entry
            c.execute("INSERT INTO data (name, course_code, session_code, time, location_name, location) VALUES (%s, %s, %s, %s, %s, %s)", db_entry)
            #push to db
            #print db_entry
          last_data = data[:]

db.commit()
db.close()
print 'Done'
