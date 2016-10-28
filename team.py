#!/usr/bin/python

import os
import urllib2

from player import Player
from bs4 import BeautifulSoup

class Team(object):

    ROSTER_URL = 'http://www.basketball-reference.com/teams/%s/%d.html'

    PLAYER_NAME_STAT = 'player'
    PLAYER_SHORT_NAME_ATTR = 'data-append-csv'

    def __init__(self, short_name, year):
        self.short_name = short_name.upper()
        self.roster = []
        self.year = year

    def __str__(self):
        return 'Team: %s' % self.short_name

    def __repr__(self):
        return self.short_name

    def get_filename_path(self):
        return 'cache/%s-%d.html' % (self.short_name.lower(), self.year)

    def get_roster_url(self):
        return self.ROSTER_URL % (self.short_name, self.year)

    def get_roster(self):
        # Check if it's already loaded in memory.
        if not self.roster:
            self.load_roster()

        return self.roster

    def load_roster(self):
        if not os.path.isfile(self.get_filename_path()):
            content = urllib2.urlopen(self.get_roster_url()).read()
            with open(self.get_filename_path(), 'w') as f:
                f.write(content)

        # Drink the soup.
        soup = BeautifulSoup(open(self.get_filename_path()), 'html.parser')

        for table in soup.find_all('table'):
            # Only load the roster table for now.
            if table.get('id', '') == 'roster':
                for player in table.find_all('tr'):
                    name = None
                    short_name = None
                    for stat in player.find_all('td'):
                        data_stat = stat.get('data-stat', None)
                        if data_stat == self.PLAYER_NAME_STAT:
                            player_name = stat.get_text()
                            player_short_name = stat.get(self.PLAYER_SHORT_NAME_ATTR, None)
                            self.roster.append(Player(player_name, player_short_name))

                # Break out once we've found and parsed the regular season stats.
                break
