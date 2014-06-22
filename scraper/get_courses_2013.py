import os
import pprint
import sqlite3
from bs4 import BeautifulSoup

buildings = {'AB': '50  St. George Street, M5S 3H4',
 'AD': '172 St. George Street, M5R 0A3',
 'AH': '121  St. Joseph Street, M5S 1J4',
 'AN': "95  Queen's Park, M5S 2C7",
 'AP': '19  Russell Street, M5S 2S2',
 'AR': '230  College Street, M5T 1R2',
 'BA': '40  St. George Street, M5S 2E4',
 'BC': "75a   Queen's Park, M5S 1K7",
 'BF': '4  Bancroft Avenue, M5S 1C1',
 'BH': '1  Elmsley Place,',
 'BI': '100  College Street, M5G 1L5',
 'BL': '140  St. George Street, M5S 3G6',
 'BN': '320  Huron Street, M5S 3J7',
 'BR': '81  St. Mary Street, M5S 1J4',
 'BS': '50  St. Joseph Street, M5S IJ4',
 'BT': '93  Charles St. West, M5S 1K9',
 'BW': '89  Charles Street West, M5S 1K6',
 'CA': '370  Huron Street, M5S 2G4',
 'CB': '112  College St, M5G 1L6',
 'CD': '56  Spadina Road,',
 'CE': '229  College Street, M5T 1R4',
 'CF': '95  St. Joseph Street, M5S 2R9',
 'CG': "14  Queen's Park Crescent West, M5S 3K9",
 'CH': "31  King's College Circle, M5S 1A1",
 'CN': '89  Chestnut Street, M5G 1R1',
 'CR': '100  St. Joseph Street, M5S 1J4',
 'CS': '158  St. George Street, M5S 2V8',
 'CU': '33  St. George Street, M5S 2E3',
 'CX': '245 College Street,',
 'DC': '160  College Street, M5S 3E1',
 'DN': '124  Edward Street, M5G 1G6',
 'DR': "21  King's College Circle, M5S 3J3",
 'EA': "11  King's College Road, M5S 1A4",
 'EH': '81  St. Mary Street, M5S 1J4',
 'EJ': "80  Queen's Park, M5S 2C5",
 'EL': "11  King's College Road (rear), M5S 3J2",
 'EM': "75  Queen's Park, M5S 1K7",
 'EP': '149 College Street, M5T 1P5',
 'ER': '7  Glen Morris Street, M5S 1H9',
 'ES': '33  Willcocks Street, M5S 3B3',
 'EX': '255  McCaul Street, M5T 1W7',
 'FA': '720  Spadina Avenue, M5S 2T9',
 'FC': '41  Willcocks Street, M5S 1C7',
 'FE': '371  Bloor Street West, M5S 2R7',
 'FG': '150  College Street, M5S 1A8',
 'FH': "84  Queen's Park, M5S 2C5",
 'FI': '222  College Street, M5T 3J1',
 'FS': "59  Queen's Park Crescent East, M5S 2C4",
 'GA': '223  College Street, M5T 1R4',
 'GB': '35  St. George Street, M5S 1A4',
 'GC': '150  Charles Street West, M5S 1K9',
 'GD': '60  Harbord Street, M5S 1A1',
 'GE': '150  St. George Street, M5S 3G7',
 'GH': '8  Elmsley Place,',
 'GI': '15  Devonshire Place, M5S 1H8',
 'GM': '4  Glen Morris Street, M5S 1J1',
 'GO': '100 Devonshire Place,',
 'GS': '65  St. George Street, M5S 2E5',
 'GU': '16  Bancroft Avenue, M5S 1C1',
 'HA': '170  College Street (rear of), M5S 3E3',
 'HH': '7  Hart House Circle, M5S 3H3',
 'HI': '44  Devonshire Place, M5S 2E2',
 'HS': '155  College Street, M5T 1P8',
 'HU': '215  Huron Street, M5S 1A2',
 'IA': '703  Spadina Avenue, M5S 2J4',
 'IN': '2  Sussex Avenue, M5S 1J5',
 'IR': '121  St. George Street, M5S 2E8',
 'IS': '111  St. George Street, M5S 2E8',
 'JH': '170  St. George Street, M5R 2M8',
 'JP': '90 Wellesley Street West, M5S 1C5',
 'KL': '113  St. Joseph Street, M5S 1J4',
 'KP': '569  Spadina Crescent, M5S 2J7',
 'KS': '214  College Street, M5T 2Z9',
 'KX': '59  St. George Street, M5S 2E6',
 'LA': '15  Devonshire Place, M5S 1H8',
 'LB': '89  Charles Street West, M5S 1K6',
 'LC': '70  St. Mary Street, M5S 1J3',
 'LG': '655  Spadina Avenue, M5S 2H9',
 'LH': '65  Charles Street West, M5S 1K5',
 'LI': "125 Queen's Park, M5S 2C7",
 'LM': '80  St. George Street, M5S 3H6',
 'LW': "78  Queen's Park, M5S 2C5",
 'MA': '4  Devonshire Place, M5S 2E1',
 'MB': '170  College Street, M5S 3E3',
 'MC': "5  King's College Road, M5S 3G8",
 'ME': "39  Queen's Park Crescent East, M5S 2C3",
 'MF': '100  Devonshire Place, M5S 2C9',
 'MG': '140  Charles Street West, M5S 1K9',
 'MH': "59  Queen's Park Crescent East, M5S 2C4",
 'MK': '315  Bloor Street West, M5S 1A3',
 'ML': "39A   Queen's Park Crsc. E, M5S 2C3",
 'MM': '63  St. George Street, M5S 2Z9',
 'MN': '6  Elmsley Place,',
 'MO': '75  St. George Street, M5S 2E5',
 'MP': '255  Huron Street, M5S 1A7',
 'MR': "12  Queen's Park Crescent W, M5S 1S8",
 'MS': "1  King's College Circle, M5S 1A8",
 'MU': '1  Devonshire Place, M5S 3K7',
 'MZ': '2  Elmsley Place,',
 'NB': '563  Spadina Crescent, M5S 2J7',
 'NF': "73  Queen's Park Crescent East, M5S 1K7",
 'NR': '45  Willcocks Street, M5S 1C7',
 'OA': '263  McCaul Street, M5T 1W7',
 'OG': '92  College Street, M5S 1L5',
 'OH': '50  St. Joseph Street, M5S 1J4',
 'OI': '252  Bloor Street West, M5S 1V6',
 'PB': '144  College Street, M5S 3M2',
 'PG': '45  St. George Street, M5S 2E5',
 'PH': '3  Elmsley Place,',
 'PI': "59  Queen's Park Crescent East, M5S 2C4",
 'PL': "90 Queen's Park,",
 'PR': "71  Queen's Park Crescent East, M5S 1K7",
 'PT': "6  King's College Road, M5S 3H5",
 'RB': '120  St. George Street, M5S 1A5',
 'RG': '100 Wellesley Street West, M5S 1C5',
 'RJ': '85  Charles Street West, M5S 1K5',
 'RL': '130  St. George Street, M5S 1A5',
 'RM': '254-256   McCaul Street, M5T 1W5',
 'RS': '164  College Street, M5S 3G9',
 'RT': '105  St. George Street, M5S 3E6',
 'RU': '500  University Avenue, M5G 1V7',
 'RW': '25  Harbord Street, M5S 3G5',
 'SA': '713  Spadina Avenue, M5S 2J4',
 'SB': '487  Spadina Crescent, M5S 2T4',
 'SC': '21  Sussex Avenue, M5S 1J6',
 'SD': '73  St. George Street, M5S 2E5',
 'SF': "10  King's College Road, M5S 3G4",
 'SG': '49  St. George Street, M5S 2E5',
 'SI': "27  King's College Circle, M5S 1A1",
 'SK': '246  Bloor Street West, M5S 1V4',
 'SM': "7 and 9 King's College Circle, M5S 3K1",
 'SN': '63  Charles Street West, M5S 1K5',
 'SO': '12  Hart House Circle, M5S 3J9',
 'SP': '1  Spadina Crescent, M5S 2J5',
 'SR': '70  St. Joseph Street,',
 'SS': '100  St. George Street, M5S 3G3',
 'ST': '17  Russell Street, M5S 2S2',
 'SU': '40  Sussex Avenue, M5S 1J7',
 'SV': '96  St. Joseph Street,',
 'TC': '6  Hoskin Avenue, M5S 1H8',
 'TF': "57  Queen's Park Crescent East, M5S 2C4",
 'TH': "47  Queen's Park Crescent East, M5S 2C3",
 'TR': '7  Hart House Circle, M5S 3H3',
 'TT': '455  Spadina Avenue, M5S 2G8',
 'TZ': "6  Queen's Park Crescent West, M5S 3H2",
 'UB': '89  Charles Street West, M5S 1K6',
 'UC': "15  King's College Circle, M5S 3H7",
 'UP': '79  St. George Street, M5S 2E5',
 'VA': '299  Bloor Street West,',
 'VC': '91  Charles Street West, M5S 1K7',
 'VI': "25 King's College Circle, M5S 1A1",
 'VP': '299 Bloor Street West,',
 'WA': '123  St. George Street, M5S 2E8',
 'WB': '184-200   College Street, M56 3E5',
 'WE': '300  Huron Street, M5S 2Z3',
 'WI': '40  Willcocks Street, M5S 1C6',
 'WN': '5  Elmsley Place,',
 'WO': '321  Bloor St. West, M5S 1S5',
 'WR': '45  Walmer Road, M5R 2X2',
 'WS': '55  Harbord Street, M5S 2W6',
 'WT': '85  St. George Street, M5S 2E5',
 'WW': '119  St. George Street, M5S 1A9',
 'WY': '5  Hoskin Avenue, M5S 1H7',
 'XQ': "43  Queen's Park Crescent East, M5S 2C3",
 'XX790': '30  Charles St. West,',
 'XX791': '35  Charles St. West,',
 'ZC': '88  College Street, M5G 1L4'}

master_dict = {}

pages = os.listdir('courses_2013')
for page in pages:
  file = open('courses_2013/' + page, 'r')
  html = file.read()
  soup = BeautifulSoup(html.split('<!-- END WAYBACK TOOLBAR INSERT -->')[1])
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
          if ' ' in data[4]:
            data[4] = data[4].split(' ')[0]
          data[4] = data[4].strip()
          name = course_code + ' ' + data[0]
          db_entry = (name, course_code, data[0], data[4])
          #push to DB
          if data[4] in buildings.keys():
            if name[:3] in master_dict.keys():
              master_dict[name[:3]].append(buildings[data[4]])
            else:
              master_dict[name[:3]] = [buildings[data[4]]]
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
        if 'Course' not in data[0] and data[6].lower() not in ['', 'tba']:
          if data[0] == '':
            data[0] = last_data[0]
          if data[1] == '':
            data[1] = last_data[1]
          if data[3] == '':
            data[3] = last_data[3]
          if ' ' in data[6]:
            data[6] = data[6].split(' ')[0]
          data[4] = data[4].strip()
          data[1] = data[1][:1]
          data[3] = data[3][:5]
          name = data[0] + ' ' + data[3]
          db_entry = (name, data[0], data[3], data[6])
          if data[6] in buildings.keys():
            if name[:3] in master_dict.keys():
              master_dict[name[:3]].append(buildings[data[6]])
            else:
              master_dict[name[:3]] = [buildings[data[6]]]
          #push to db
          last_data = data[:]

def most_common(lst):
    return max(set(lst), key=lst.count)

for key in master_dict:
  arr = master_dict[key][:]
  master_dict[key] = most_common(arr)

pprint.pprint(master_dict)
