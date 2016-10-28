#!/usr/bin/python

import os
import urllib2

from team import Team

from bs4 import BeautifulSoup

class League(object):

    LEAGUE_INFO_URL = 'http://www.basketball-reference.com/leagues/NBA_%d.html'

    def __init__(self):
        self.teams = {}

    @staticmethod
    def get_filename_path(year):
        return 'cache/%d.html' % year

    @classmethod
    def get_league_info_url(cls, year):
        return cls.LEAGUE_INFO_URL % year

    def get_teams(self, year):
        if year not in self.teams:
            self.load_teams(year)
        return self.teams[year]

    def load_teams(self, year):
        if not os.path.isfile(self.get_filename_path(year)):
            content = urllib2.urlopen(self.get_league_info_url(year)).read()
            with open(self.get_filename_path(year), 'w') as f:
                f.write(content)

        soup = BeautifulSoup(open(self.get_filename_path(year)), 'html.parser')

        teams = []

        for table in soup.find_all('table'):
            if table.get('id', '') in ['divs_standings_W', 'divs_standings_E']:
                for team in table.find_all('tr'):
                    for team_name in team.find_all('th'):
                        if team_name.get('data-stat', '') == 'team_name':
                            for links in team_name.find_all('a'):
                                short_name = links['href'].split('/')[2]
                                teams.append(Team(short_name))

        self.teams[year] = teams
