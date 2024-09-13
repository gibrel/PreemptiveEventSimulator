from textual import on
from textual.app import App
from textual.widgets import Footer, Header, Label, ListView, ListItem
import helpers.creators as cre
from entities.game import Game
from textual.widgets import Static
import entities.locations as loc


class LeftSidebar(ListView):
    entity_list: list

    def __init__(self, entity_list=[]):
        super().__init__()
        self.entity_list = entity_list
        
    def compose(self):
        for entity in self.entity_list:
            yield ListItem(Label(entity.name))


class Body(Static):
    entity_list: list

    def __init__(self, entity_list=[]):
        super().__init__()
        self.entity_list = entity_list
        
    def compose(self):
        for entity in self.entity_list:
            yield Static(entity.name)


class PreemptiveEventSimulatorApp(App):
    BINDINGS = [
        # (key, action_name, description)
    ]
    TITLE = "Preemptive Event Simulator v0.0.0z"
    CSS_PATH = "main.tcss"
    app_game: Game

    def compose(self):
        yield Header(show_clock=True)
        yield LeftSidebar(self.app_game.lists(loc.Region))
        yield Body(self.app_game.lists(loc.State))
        yield Footer()

    def initialize_data(self):
        self.app_game = Game()
        cre.populate_game(self.app_game)


if __name__ == "__main__":
    app = PreemptiveEventSimulatorApp()
    app.initialize_data()
    app.run()
