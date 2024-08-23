from tests.base_test import BaseTest
import helpers.creators as cre
from entities.game import Game
import entities.sports as spr
import matplotlib.pyplot as plt
import os


class MainTest(BaseTest):
    test_description = "Check age distribution with plot."
    file_name = os.path.basename(__file__)

    def run(self):
        try:
            my_game = Game()
            cre.populate_game(my_game)
            print('Game is populated. Let\'s play!')
            print(my_game)

            players = my_game.lists(spr.Player)
            age_distribution: dict[int, int] = {}
            for player in players:
                if player.age in age_distribution.keys():
                    age_distribution[player.age] = age_distribution[player.age] + 1
                else:
                    age_distribution[player.age] = 1
            age_distribution = dict(sorted(age_distribution.items()))
            print(age_distribution)

            plt.bar(range(len(age_distribution)), list(age_distribution.values()), align='center')
            plt.xticks(range(len(age_distribution)), list(age_distribution.keys()))
            plt.show()
        except Exception as e:
            self.error(e)


def test():
    MainTest()
