import helpers.creators as cre
from entities.game import Game

# Import Data
my_game = Game()
# Create Data
cre.populate_game(my_game)

print('Game is populated. Let\'s play!')
print(my_game)
