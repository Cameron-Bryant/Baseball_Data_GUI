import requests 
from bs4 import BeautifulSoup
from itertools import chain
import xlsxwriter
#Scraping, Visualizing, and Analyzing MLB Player Data 
###Step 1:> Scraping and Cleaning
#get html/put mlb stat sites here
sites = [
    'https://www.mlb.com/stats/',
    'https://www.mlb.com/stats/?page=2',
    'https://www.mlb.com/stats/?page=3',
    'https://www.mlb.com/stats/?page=4',
    'https://www.mlb.com/stats/?page=5',
    'https://www.mlb.com/stats/?page=6',
    'https://www.mlb.com/stats/?page=7'
]
def getRequests(locs):
    reqs = []
    for loc in locs:
        page = requests.get(loc)
        reqs.append(BeautifulSoup(page.content, 'html.parser'))
    return reqs

soups = []
raw_data = []
data_tags = []
player_tags = []
player_raw = []
soups = getRequests(sites)
for i in range(len(soups)):
    #get the data
    data_tags = soups[i].find_all('td')
    for dp in data_tags:
        raw_data.append(dp.contents)
    #get player names
    player_tags = soups[i].find_all('span', class_="full-3fV3c9pF")
    for tag in player_tags:
        player_raw.append(tag.contents)

#get categories, eg runs, hrs, homeruns
column_category_tags = soups[0].find_all('abbr', class_="bui-text cellheader bui-text")
cats = []
for cat in column_category_tags:
    cats.append(cat.contents)
    
#flatten the data
cats = list(chain.from_iterable(cats))
flattened_data = list(chain.from_iterable(raw_data))
player_flat = list(chain.from_iterable(player_raw))\

#join first and last names of the player, eg [['jane'], ['doe']...] to ['jane doe'...]
print(cats)
first = []
last = []
for i in range(len(player_flat)):
    if i % 2 == 0:
        first.append(player_flat[i])
    else:
        last.append(player_flat[i])
player_names = []
for i in range(len(last)):
    player_names.append(first[i] + ' ' + last[i])
    
#remove team abbr, add num, and find len of rows
teams = []
t_num = 0
row_len = 0
data = []
for i in range(len(flattened_data)):
    try:
        data.append(float(flattened_data[i]))
        row_len += 1
    except ValueError:
        teams.append(flattened_data[i])
        data.append(t_num)
        row_len = 0
        t_num += 1
       
def to_matrix(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]

def printGood(d):
    for i in range(len(d)):
        print(d[i])
#restructure data
col_len = len(teams)
clean_data = to_matrix(data, row_len + 1) #data is now a 2d list of players stats
#Save the data to an excel file
workbook = xlsxwriter.Workbook('C://Users//camer//Desktop//ScrapingData//MLB_Data.xlsx')#change address here for your computer
worksheet = workbook.add_worksheet()
#names
row = 1
for name in (player_names):
    worksheet.write(row, 0, name)
    row += 1 
#category
col = 1
for category in cats:
    worksheet.write(0, col, category)
    col += 1
#data
c = 2
r = 1
for data in clean_data:
    c = 2
    for dp in data:
        worksheet.write(r, c, dp)
        c += 1
    r += 1
workbook.close()
