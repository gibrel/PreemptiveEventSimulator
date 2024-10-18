from __future__ import annotations
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Footer, Header, Static, Tree, Label
import helpers.creators as cre
from entities.game import Game
import entities.locations as loc
import entities.sports as spr


class PreemptiveEventSimulatorApp(App):
    BINDINGS = [
        # (key, action_name, description)
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    TITLE = "Preemptive Event Simulator v0.0.002"
    CSS_PATH = "main.tcss"
    app_game: Game

    def initialize_data(self):
        self.app_game = Game()
        cre.populate_game(self.app_game)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="sidebar"):
            yield Tree(self.app_game.get_first(loc.Country).name)
        with Horizontal():
            yield Static('\n' + (self.TITLE + " ")* 10 + '\n\n', id="body")
        yield Footer()

    def on_mount(self):
        pais: Tree[dict] = self.query_one(Tree)
        pais.root.expand()
        for regiao in self.app_game.lists(loc.Region):
            regiao_corrente = pais.root.add(regiao.name)
            for estado in self.app_game.lists(
                loc.State, lambda x: x.region.name == regiao.name
            ):
                estado_corrente = regiao_corrente.add(estado.name)
                for cidade in self.app_game.lists(
                    loc.City, lambda x: x.state().name == estado.name
                ):
                    estado_corrente.add_leaf(cidade.name, data=cidade)
        pais.focus()

    def refresh_teams(self, city: loc.City | None) -> None:
        if city is None:
            return
        teams = self.app_game.lists(spr.Team, lambda x: x.city == city)
        for team in teams:
            self.selected_team = []

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        node = event.node
        if node.data.__class__ is loc.City:
            body = self.query_one("#body")
            body.update(f'{self.print_city_data(node.data)}')
            self.refresh_teams(node.data)

    def print_city_data(self, city: loc.City) -> str:
        print = city.full_print()
        teams = self.app_game.lists(spr.Team, lambda x: x.city == city)
        print += f"\t\tTimes ({len(teams)}):\n"
        i = 0
        for team in teams:
            print += f"\t\t\t{team.name}"
            if i % 3 == 2:
                print += f"{i}\n"
            i += 1
        print += "\n"
        return print


if __name__ == "__main__":
    app = PreemptiveEventSimulatorApp()
    app.initialize_data()
    app.run()
