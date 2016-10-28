#!/usr/bin/python

from datetime import datetime
from league import League
from player import Player
from team import Team

YEAR = 2016

DATE_FORMAT = '%Y-%m-%d'
WEEK_0_START = datetime.strptime('2015-10-26', DATE_FORMAT)

NBA = League()

# TODO: move this logic into team.get_starters()
for team in NBA.get_teams(YEAR):
    roster = sorted(team.get_roster(), key=lambda player: player.get_games_started(YEAR), reverse=True)
    starters = roster[0:5]
    print team
    print starters
