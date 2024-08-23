from tests.base_test import BaseTest
import helpers.creators as cre
from entities.game import Game
import os


class MainTest(BaseTest):
    test_description = "Populando jogo com times, equipes e jogadores."
    file_name = os.path.basename(__file__)

    def run(self):
        try:
            # Import Data
            my_game = Game()
            # Create Data
            cre.populate_game(my_game)

            print('Game is populated. Let\'s play!')
            print(my_game)
        except Exception as e:
            self.error(e)


def test():
    MainTest()
