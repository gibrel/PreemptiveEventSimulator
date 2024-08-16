from __future__ import annotations
import random
import numpy
import entities.generator as gen
from helpers.json_decoder import Decoder
from entities.locations import City
import entities.sports as spr
from entities.game import Game
from helpers.enums import Category
from alive_progress import alive_bar


def populate_game(game: Game) -> None:
    """
    Populates a game with teams, squads and players.
    :param game: The game entity to be populated.
    :return: None
    """
    cities = game.list(City)
    with alive_bar(len(cities), force_tty=True) as bar:
        for city in cities:
            qtd_teams = city.max_teams
            teams: list[spr.Team] = []
            squads: list[spr.Squad] = []
            players: list[spr.Player] = []
            for _ in range(0, max(qtd_teams.values())):
                team = create_team(game, city)
                teams.append(team)
                # print(f'Created team: {team}')
            while not all(value == 0 for value in qtd_teams.values()):
                for category in [Category.age_15_17, Category.age_18_19, Category.age_20_24, Category.age_25_29,
                                 Category.age_30_up]:
                    if qtd_teams[category] > 0:
                        try:
                            team = teams[max(qtd_teams.values()) - 1]
                        except IndexError:
                            print(f'{max(qtd_teams.values()) - 1}/{len(teams)} in {category} at {city.name}')
                        squad = create_squad(game, category, team)
                        squads.append(squad)
                        # print(f'Created squad: {squad}')
                        for _ in range(Decoder.ATHLETES_IN_SQUAD):
                            player = create_player(game, category, squad)
                            players.append(player)
                            # print(f'Created {team}, {squad.name} player: {player}')
                        for _ in range(3):
                            player = create_player(game, category, None)
                            players.append(player)
                            # print(f'Created no team/squad player: {player}')
                        qtd_teams[category] = qtd_teams[category] - 1
                    # print(f'Ended category {category}')
                # print(f'Check if all are 0: {qtd_teams.values()}')
            # print(f'{cities.index(city)} of {len(cities)}')
            bar()


def create_player(game: Game, category: Category, squad: spr.Squad | None = None) -> spr.Player:
    players = game.list(spr.Player)
    uid = len(players) + 1
    (name, surname) = generate_person_names()[0]
    if category is Category.age_15_17:
        age = random.randint(15, 17)
    elif category is Category.age_18_19:
        age = random.randint(18, 19)
    elif category is Category.age_20_24:
        age = random.randint(20, 24)
    elif category is Category.age_25_29:
        age = random.randint(25, 29)
    else:  # category is Category.age_30_up:
        age = random.randint(30, 40)
    if age == 40:  # shake things up from 40+ age
        age = random.randint(40, 50)
    skill = numpy.random.poisson(45)
    player = spr.Player(uid, name, surname, age, skill, squad)
    game.insert(player)
    return player


def create_squad(game: Game, category: Category, team: spr.Team) -> spr.Squad:
    squads = game.list(spr.Squad)
    uid = len(squads) + 1
    name = gen.Colors.random()
    squad = spr.Squad(uid, name, category, team)
    game.insert(squad)
    return squad


def create_team(game: Game, city: City) -> spr.Team:
    teams = game.list(spr.Team)
    uid = len(teams) + 1
    name = generate_team_names()[0]
    team = spr.Team(uid, name, city)
    game.insert(team)
    return team


def create_many_teams(game: Game, quantity: int) -> list[spr.Team]:
    teams = []
    if quantity < 1:
        return teams
    base = len(game.list(spr.Team))
    for index in range(0, quantity):
        uid = index + base + 1
        name = generate_team_names(1)[0]
        city = random.choice(game.list(City))
        team = spr.Team(uid, name, city)
        teams.append(team)
        game.insert(team)
    return list(set(teams).intersection(game.list(spr.Team)))


def import_locations():
    Decoder.decode_locations()
    Decoder.decode_inhabitants()


def generate_team_names(quantity: int = 1) -> list[str]:
    name_list = []
    if quantity > 0:
        for _ in range(quantity):
            name_list.append(f'{gen.Animal.random().capitalize()} {gen.Adjective.random().capitalize()}')
    return name_list


def generate_person_names(quantity: int = 1) -> list[(str, str)]:
    name_list = []
    if quantity > 0:
        for _ in range(quantity):
            name_list.append((gen.Name.random().capitalize(), gen.Surname.random().capitalize()))
    return name_list
