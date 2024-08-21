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
    cities = game.lists(City)
    uid_team = game.count(spr.Team) + 1
    uid_squad = game.count(spr.Squad) + 1
    uid_player = game.count(spr.Player) + 1
    # print(f'Team: {uid_team}, Squad: {uid_squad}, Player: {uid_player}')
    no_check = True
    with alive_bar(len(cities), force_tty=True) as bar:
        for city in cities:
            squads: list[spr.Squad] = []
            players: list[spr.Player] = []
            qtd_teams = city.max_teams
            teams = create_many_teams(max(qtd_teams.values()), uid_team, city)
            uid_team = uid_team + max(qtd_teams.values())
            for category in [Category.age_15_17, Category.age_18_19, Category.age_20_24, Category.age_25_29,
                             Category.age_30_up]:
                no_squad_qtd = random.randint(3, 5) * qtd_teams[category]
                no_squad_players = create_many_players(no_squad_qtd, uid_player, category)
                uid_player = uid_player + no_squad_qtd
                players = players + no_squad_players
                for team in teams:
                    if qtd_teams[category] > 0:
                        squad = create_squad(uid_squad, category, team)
                        uid_squad = uid_squad + 1
                        squads.append(squad)
                        squad_players = create_many_players(Decoder.ATHLETES_IN_SQUAD, uid_player, category, squad)
                        uid_player = uid_player + Decoder.ATHLETES_IN_SQUAD
                        players = players + squad_players
                        qtd_teams[category] = qtd_teams[category] - 1
            for team in teams:
                game.insert(team, no_check)
            for squad in squads:
                game.insert(squad, no_check)
            for player in players:
                game.insert(player, no_check)
            # print(f'Em {city.name} - {city.state().abbreviation} temos:'
            #       f'\t{len(teams)} time(s), {len(squads)} equipe(s) e {len(players)} jogadores.')
            bar()


def create_player(uid: int, category: Category, squad: spr.Squad | None = None) -> spr.Player:
    (name, surname) = generate_person_names()[0]
    age = random_age_by_category(category)
    skill = numpy.random.poisson(45)
    return spr.Player(uid, name, surname, age, skill, squad)


def create_many_players(quantity: int,
                        initial_uid: int, category: Category, squad: spr.Squad | None = None) -> list[spr.Player]:
    players: list[spr.Player] = []
    names = generate_person_names(quantity)
    for i in range(quantity):
        uid = initial_uid + i
        (name, surname) = names[i]
        age = random_age_by_category(category)
        skill = numpy.random.poisson(45)
        players.append(spr.Player(uid, name, surname, age, skill, squad))
    return players


def random_age_by_category(category: Category) -> int:
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
    if age >= 40:  # shake things up from 40+ age using poison distribution and probability
        if random.choices([True, False], [1/10, 9/10])[0]:
            age = 40
        else:
            age = numpy.random.poisson(40)
            diff = abs(age - 40)
            age = 40 + diff
    return age


def create_squad(uid: int, category: Category, team: spr.Team) -> spr.Squad:
    name = gen.Colors.random()
    return spr.Squad(uid, name, category, team)


def create_team(uid: int, city: City) -> spr.Team:
    name = generate_team_names()[0]
    return spr.Team(uid, name, city)


def create_many_teams(quantity: int, initial_uid: int, city: City) -> list[spr.Team]:
    teams = []
    if quantity < 1:
        return teams
    for index in range(quantity):
        uid = index + initial_uid
        name = generate_team_names(1)[0]
        team = spr.Team(uid, name, city)
        teams.append(team)
    return teams


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
