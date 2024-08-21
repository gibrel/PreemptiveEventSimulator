import helpers.creators as cre
from entities.game import Game
import entities.sports as spr

# Import and Create Data
my_game = Game()
cre.populate_game(my_game)
print('Game is populated. Let\'s play!')
print(my_game)

# Lambda list with filter
print(f'\nFound {my_game.count(spr.Player, lambda x: x.uid <= 50)} players with uid <= 50')
my_game.prints(spr.Player, lambda x: x.uid <= 50)
print(f'\nFound {my_game.count(spr.Squad, lambda x: x.uid <= 25)} squads with uid <= 25')
my_game.prints(spr.Squad, lambda x: x.uid <= 25)
print(f'\nFound {my_game.count(spr.Team, lambda x: x.uid <= 12)} teams with uid <= 12')
my_game.prints(spr.Team, lambda x: x.uid <= 12)
