#!/usr/bin/python2

from pwn import *
import requests
from bs4 import BeautifulSoup

cities = {
    'Albania' : 'Tirana',
    'Czech Republic' : 'Prague',
    'North Carolina' : 'Raleigh',
    'West Virginia' : 'Charleston',
    'Republic of the Congo' : 'Brazzaville',
    'Brazzaville' : 'Ouagadougou',
    'Idaho' : 'Boise',
    'Vermont' : 'Montpelier',
    'East Timor (Timor-Leste)' : 'Dili',
    'Delaware' : 'Dover',
    'Kiribati' : 'Tarawa',
    'Utah' : 'Salt Lake City',
    'Maine' : 'Augusta',
    'Michigan' : 'Lansing',
    'Tuvalu' : 'Funafuti',
    'Arkansas' : 'Little Rock',
    'Oregon' : 'Salem',
    'Rhode Island' : 'Providence',
    'Illinois' : 'Springfield',
    'Macedonia' : 'Skopje',
    'South Carolina' : 'Columbia',
    'Tennesse' : 'Nashville',
    'South Dakota' : 'Pierre',
    'Texas' : 'Austin',
    'Mississipi' : 'Jackson',
    'Mississippi' : 'Jackson',
    'Wisconsin' : 'Madison',
    'Minnesota' : 'St. Paul',
    'Virginia' : 'Virginia',
    'Wyoming' : 'Cheyenne',
    'Connecticut' : 'Hartford',
    'Colorado' : 'Denver',
    'California' : 'Sacramento',
    'Washington' : 'Olympia',
    'New Mexico' : 'Santa Fe',
    'Iowa' : 'Des Moines',
    'Georgia' : 'Atlanta',
    'Alaska' : 'Juneau',
    'Kentucky' : 'Frankfort',
    'Arizona' : 'Phoenix',
    'North Dakota' : 'Bismarck',
    'Ohio' : 'Columbus',
    'Tennessee' : 'Nashville',
    'Missouri' : 'Jefferson City',
    'Maryland' : 'Annapolis',
    'Yemen' : 'Sana\'a',
    'Democratic Republic of the Congo' : 'Kinshasa',
    'New York' : 'Albany',
    'Pennsylvania' : 'Harrisburg',
    'Alabama' : 'Montgomery',
    'Massachusetts' : 'Boston',
    'New Hampshire' : 'Concord',
    'Oklahoma' : 'Oklahoma City',
    'Montana' : 'Helena',
    'Virginia' : 'Richmond',
    'Nebraska' : 'Lincoln',
    'Indiana' : 'Indianapolis',
    'Haiti' : 'Port-au-Prince',
    'Louisiana' : 'Baton Rouge',
    'New Jersey' : 'Trenton',
    'Hawaii' : 'Honolulu',
    'Kansas' : 'Topeka',
    'Florida' : 'Tallahassee',
    'Nevada' : 'Carson City',
    '' : '',
    '' : '',
    '' : '',


    'Bosnia and Herzegovina' : 'Sarajevo',
    'Guinea-Bissau' : 'Bissau',
    'Portugal' : 'Lisbon',
    'Cyprus' : 'Nicosia',
    'Mexico' : 'Mexico City',
    'South Sudan' : 'Juba',
    'Morocco' : 'Rabat',
    'Slovakia' : 'Bratislava',
    'Brunei' : 'Bandar Seri Begawan',
    'Lebanon' : 'Beirut',
    'Ireland' : 'Dublin',
    'India' : 'New Delhi',
    'Sweden' : 'Stockholm',
    'Saudi Arabia' : 'Riyadh',
    'Somalia' : 'Mogadishu',
    'Panama' : 'Panama City',
    'Egypt' : 'Cairo',
    'San Marino' : 'San Marino',
    'Serbia' : 'Belgrade',
}

raw = requests.get('https://geographyfieldwork.com/WorldCapitalCities.htm').text
scraper = BeautifulSoup(raw, 'html.parser')

table = scraper.find('table', {'id' : 'anyid'})

rows = table.find_all('tr')[1:-1]

for r in rows:
    f = [x.text for x in r.find_all('td')]
    if f[0] not in cities:
        cities[f[0]] = f[1]

r = remote('chall2.2019.redpwn.net', 6001)

def read(r):
    line = ''

    while not line.endswith('\n'):
        try:
            line += r.recv(1)
        except:
            print(line)
            exit()
    return line

while True:
    line = read(r)

    while 'capital of' not in line:
        print(line.replace('\n', ''))
        line = read(r)
    
    print(line)
    city = line[23:-2]

    capital = cities[city]

    print(capital)
    r.sendline(capital)

r.interactive()
