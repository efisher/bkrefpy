#!/usr/bin/python

from datetime import datetime
from league import League
from player import Player
from team import Team

DATE_FORMAT = '%Y-%m-%d'

WEEK_0_START = datetime.strptime('2015-10-26', DATE_FORMAT)

YEAR = 2016

nba = League()

for team in [Team('GSW', YEAR)]: #nba.get_teams(YEAR):
    roster = sorted(team.get_roster(), key=lambda player: player.get_games_started(YEAR))
    print roster


# warriors = Team('GSW')
# warriors_roster = warriors.get_roster(2015)

# print 'Roster in 2015...'
# print warriors_roster

# player = random.choice(warriors_roster)
# print 'Getting stats for %s...' % player
# last_year_stats = player.get_year_stats(2015)
# print last_year_stats

# print 'number of 10+ point games:...'
# print len(last_year_stats[last_year_stats.pts >= 10])

# print 'equal points and rebounds games:...'
# print last_year_stats[last_year_stats.pts == last_year_stats.trb]
# # for p in PLAYERS:
# #     (first_name, last_name) = p.split(' ')
# #     dude = Player(first_name, last_name)
# #     twenty_16_stats = dude.get_year_stats(2016)
# #     print p
# #     print twenty_16_stats[twenty_16_stats.ast > 4]