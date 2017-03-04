"""
Exports MLB 2017 Top 101 Prospects
"""

import csv

import requests


# fetch mlb 2017 top prospects list
resp = requests.get('http://m.mlb.com/gen/players/prospects/2017/playerProspects.json')

# get json representation of text returned by request
prospects = resp.json() # json() method from requests

found = []

# for each player capsule, extract name, mlb id, 
for player_block in prospects['prospect_players']['prospects']:
    # extract player card url
    player_card_url = ('http://m.mlb.com/player/{}/'
                       .format(player_block['player_id']))

    # extract player name
    player_name = '{} {} '.format(player_block['player_first_name'],
                                  player_block['player_last_name'])

    # envelope player attributes in sensible data structure
    player = {
        'rank': player_block['rank'],
        'id': player_block['player_id'],
        'name': player_name,
        'url': player_card_url,
    }

    # append to our list of found players
    found.append(player)

# create a csv writer capable of writing the data structures we've created
writer = csv.DictWriter(open('mlb-2017.csv', 'w'),
                        fieldnames=['rank', 'id', 'name', 'url'])
writer.writeheader() # ...and then write the header row

for player in found:
    writer.writerow(player) # write each player we've found
