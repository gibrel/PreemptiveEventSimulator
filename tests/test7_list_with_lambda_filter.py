from tests.base_test import BaseTest
import helpers.creators as cre
from entities.game import Game
import entities.sports as spr
import os


class MainTest(BaseTest):
    test_description = "List with search parameters."
    file_name = os.path.basename(__file__)

    def run(self):
        try:
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
        except Exception as e:
            self.error(e)


def test():
    MainTest()
