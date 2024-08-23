from tests.base_test import BaseTest
import entities.sports as spr
import pprint
import helpers.creators as cre
from entities.game import Game
import random
import os


class MainTest(BaseTest):
    test_description = "Inserção de times."
    file_name = os.path.basename(__file__)

    def run(self):
        try:
            my_game = Game()
            teams = cre.create_many_teams(10, 1, random.choice(my_game.lists(spr.City)))
            (insertion_success, failed_insertions) = my_game.insert_many(teams)
            if not insertion_success:
                print(f'Failed inserting some items:')
                for obj in failed_insertions:
                    print(obj)
            teams = my_game.lists(spr.Team)
            print(f'Printing successful insertions:')
            for team in teams:
                print(team)
                pprint.pprint(team.city.inhabitants)
            team = random.choice(teams)
            print(f'{team.name} de {team.city.name} - {team.city.micro_region.medium_region.state.abbreviation}:')
            pprint.pprint(team.city.inhabitants)
            pprint.pprint(team.city.max_teams)
        except Exception as e:
            self.error(e)


def test():
    MainTest()
