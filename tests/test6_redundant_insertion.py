from tests.base_test import BaseTest
import helpers.creators as cre
from entities.game import Game
import entities.sports as spr
import os


class MainTest(BaseTest):
    test_description = "Insert redundant uid value."
    file_name = os.path.basename(__file__)

    def run(self):
        try:
            # Import and Create Data
            my_game = Game()
            cre.populate_game(my_game)
            print('Game is populated. Let\'s play!')
            print(my_game)

            # Redundant insertion test
            redundant_uid = my_game.lists(spr.Player)[-1].uid
            redundant_player = spr.Player(redundant_uid, "Fulano", "de Tal", 18, 99)
            success = my_game.insert(redundant_player)
            print(f'\nResult of inserting redundant uid {redundant_player.uid} -> success = {success}')
            lambda_redundant_uid = lambda x: x.uid == lambda_redundant_uid
            ret = my_game.lists(spr.Player, lambda_redundant_uid)
            my_game.prints(spr.Player, lambda_redundant_uid)
        except Exception as e:
            self.error(e)


def test():
    MainTest()
