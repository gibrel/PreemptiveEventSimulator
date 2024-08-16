import pprint
import helpers.creators as cre
import entities.locations as loc
from entities.game import Game

my_game = Game()
print(my_game)
cities = [my_game.list(loc.City)[0], my_game.list(loc.City)[2785],
          my_game.list(loc.City)[-1]]
for city in cities:
    print(city)
    pprint.pprint(city.inhabitants)
    pprint.pprint(city.max_teams)
teams = cre.create_many_teams(my_game, 10)
for team in teams:
    print(team)
