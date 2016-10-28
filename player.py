#!/usr/bin/python

from datetime import datetime
import os
import pandas as pd
import urllib2

from bs4 import BeautifulSoup

class Player(object):

    GAME_LOG_URL = 'http://www.basketball-reference.com/players/a/%s/gamelog/%d/'

    DATE_STAT = 'date_game'
    DATE_FORMAT = '%Y-%m-%d'

    WEEK_0_START = datetime.strptime('2015-10-26', DATE_FORMAT)

    STATS_TO_COLLECT = [
        'fg',
        'fga',
        'pts',
        'fg3',
        'fg3a',
        'ft',
        'fta',
        'orb',
        'drb',
        'trb',
        'ast',
        'stl',
        'blk',
        'tov',
        'gs',
        'pf'
    ]

    def __init__(self,
        name,
        short_name):

        self.name = name
        self.short_name = short_name
        self.stats = {}

    def __str__(self):
        return 'Player: %s' % (self.name)

    def __repr__(self):
        return self.name

    def get_filename_path(self, year):
        name_parts = self.name.split(' ')
        return 'cache/%s-%d.html' % (self.short_name, year)

    def get_game_log_url(self, year):
        return self.GAME_LOG_URL % (self.short_name, year)

    def get_year_stats(self, year):
        # Check if it's already loaded in memory.
        if year not in self.stats:
            self.load_gamelog_stats(year)

        return self.stats[year]

    def get_games_started(self, year):
        stats = self.get_year_stats(year)
        return stats.sum(axis=0)['gs']

    def load_gamelog_stats(self, year):
        # Check if it's already cached on disk.
        if not os.path.isfile(self.get_filename_path(year)):
            content = urllib2.urlopen(self.get_game_log_url(year)).read()
            with open(self.get_filename_path(year), 'w') as f:
                f.write(content)

        # Drink the soup.
        soup = BeautifulSoup(open(self.get_filename_path(year)), 'html.parser')
        
        game_log = []

        for table in soup.find_all('table'):
            # Only load regular season stats.
            if table.get('id', '') == 'pgl_basic':
                for game in table.find_all('tr'):
                    game_data = {}
                    for stat in game.find_all('td'):
                        data_stat = stat.get('data-stat', None)
                        if data_stat == self.DATE_STAT:
                            game_data[data_stat] = datetime.strptime(stat.get_text(), self.DATE_FORMAT)
                        elif data_stat and data_stat in self.STATS_TO_COLLECT:
                            game_data[data_stat] = int(stat.get_text())

                    if game_data:
                        game_log.append(game_data)

                # Break out once we've found and parsed the regular season stats.
                break

        soup.decompose()
        self.stats[year] = pd.DataFrame(game_log).set_index(self.DATE_STAT)