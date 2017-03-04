"""
Exports Baseball Prospectus 2017 Top 101 Prospects
"""

import csv
import collections
from urllib import parse

import requests

from lxml import html


def take_first(values, default=None):
    """Takes the first value from a non-generator iterable.

    Args:
        values: Iterable of values

    Returns:
        Value if found, otherwise given default value
    """

    if values is None or len(values) == 0:
        return default

    return values[0]


# fetch bp 2017 top prospects list
resp = requests.get('http://www.baseballprospectus.com/article.php?articleid=31160')

# parse html, healing broken/unbalanced tags
doc = html.fromstring(resp.content)

# bookkeeping
found = []

# run our xpath on the parsed html document
player_capsule_nodes = doc.xpath('//div[@class="article"]//span[@class="playerdef"]/..')

# for each player capsule, extract name, bp id, 
for rank, player_block in enumerate(player_capsule_nodes):
    assert player_block.tag == 'strong', html.tostring(player_block)

    # extract player card url
    player_card_url = take_first(
        player_block.xpath('./span[@class="playerdef"]/a/@href')
    )

    # extract player name
    player_name = player_block.xpath('./span[@class="playerdef"]/a/text()')

    # extract player id
    url_bits = parse.urlparse(player_card_url)
    qs = parse.parse_qs(url_bits.query)
    player_id = qs.get('id', None)

    # envelope player attributes in sensible data structure
    player = {
        'rank': rank + 1, # `enumerate` is 0-based
        'id': take_first(player_id),
        'name': take_first(player_name),
        'url': player_card_url,
    }

    # append to our list of found players
    found.append(player)

# create a csv writer capable of writing the data structures we've created
writer = csv.DictWriter(open('bp-2017.csv', 'w'),
                        fieldnames=['rank', 'id', 'name', 'url'])
writer.writeheader() # ...and then write the header row

for player in found:
    writer.writerow(player) # write each player we've found
