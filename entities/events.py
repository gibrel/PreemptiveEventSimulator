from abc import abstractmethod
from entities.sports import Team


class Event:
    """

    """

    def __init__(self, name: str, type):
        self.name = name
        self.type = type
        self.current_step = 0

    # @property
    # def current_step(self) -> int:
    #     return self.current_step

    @abstractmethod
    def run_step(self):
        """

        :return:
        """
        pass

    @abstractmethod
    def print_step(self, phase_number: int):
        """

        :param phase_number:
        :return:
        """
        pass

    @abstractmethod
    def print_rank(self):
        """

        :return:
        """
        pass


class Cup:
    """

    """

    def __init__(self, name: str, teams: list[Team]):
        self.name = name
        self.participants = teams

    def define_order(self):
        """

        :return:
        """

    def run_phase(self):
        """

        :return:
        """

    def print_phase(self, phase_number: int):
        """

        :param phase_number:
        :return:
        """

    def print_rank(self):
        """

        :return:
        """