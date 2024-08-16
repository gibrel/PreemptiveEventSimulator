import pprint
import helpers.creators as gen
import entities.sports as spr
from entities.game import Game

my_game = Game()
gen.create_many_teams(my_game, 10)
teams = my_game.list(spr.Team)
for team in teams:
    print(team)
    pprint.pprint(team.city.inhabitants)
team = teams[4]
print(f'{team.name} de {team.city.name} - {team.city.micro_region.medium_region.state.abbreviation}:')
pprint.pprint(team.city.inhabitants)
pprint.pprint(team.city.max_teams)
