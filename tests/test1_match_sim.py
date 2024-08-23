from tests.base_test import BaseTest
from services.match import play_match
from faker import Faker
import os


class MainTest(BaseTest):
    test_description = "Simulação de uma partida simples."
    file_name = os.path.basename(__file__)

    def run(self):
        try:
            fake = Faker('pt_BR')

            # Parâmetros para a distribuição de Poisson (média de gols por partida e variação por mando de campo)
            time_casa = (fake.company(), 1.5)
            time_visitante = (fake.company(), 1.2)
            dispar_mando = 0.1

            # Simula o número de gols para cada time
            resultado = play_match(time_casa[1], time_visitante[1], dispar_mando)
            gols_casa = resultado[0]
            gols_visitante = resultado[1]

            # Imprime o resultado do jogo
            print(f"Resultado do jogo: {time_casa[0]} {gols_casa} - {gols_visitante} {time_visitante[0]}")
        except Exception as e:
            self.error(e)


def test():
    MainTest()
