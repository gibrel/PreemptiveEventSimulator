from tests.base_test import BaseTest
import helpers.creators as cre
from entities.game import Game
import entities.sports as spr
import os


class MainTest(BaseTest):
    test_description = "Search players by name and skill."
    file_name = os.path.basename(__file__)

    def run(self):
        try:
            # Import and Create Data
            my_game = Game()
            cre.populate_game(my_game)
            print('Game is populated. Let\'s play!')
            print(my_game)

            # Search tests
            search_name = "Gabriel"
            lambda_name = lambda x: x.name == search_name
            ret = my_game.contains(spr.Player, lambda_name)
            print(ret)
            ret = my_game.count(spr.Player, lambda_name)
            print(ret)

            # Advanced search tests
            search_above_skill = 65
            lambda_name_skill = lambda x: x.name == search_name and x.skill > search_above_skill
            ret = my_game.lists(spr.Player, lambda_name_skill)
            print(f'\nFound {len(ret)} players named "{search_name}" with skill above {search_above_skill}')
            my_game.prints(spr.Player, lambda_name_skill)
        except Exception as e:
            self.error(e)


def test():
    MainTest()
