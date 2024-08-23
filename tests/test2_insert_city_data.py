from tests.base_test import BaseTest
from entities.game import Game
import os


class MainTest(BaseTest):
    test_description = "Inserção de localidades e importação de população."
    file_name = os.path.basename(__file__)

    def run(self):
        try:
            Game()
        except Exception as e:
            self.error(e)


def test():
    MainTest()
