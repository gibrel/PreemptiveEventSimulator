import helpers.creators as cre
from entities.game import Game

my_game = Game()
cre.populate_game(my_game)
print('Game is populated. Let\'s play!')
print(my_game)
