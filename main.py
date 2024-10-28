from __future__ import annotations
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Footer, Header, Static, Tree, Label, RadioButton, RadioSet
import helpers.creators as cre
from entities.game import Game
import entities.locations as loc
import entities.sports as spr


GAME = Game()

class RadioModule(Static):

    def compose(self) -> ComposeResult:
        yield Label("TIMES", id="radio_label")
        yield RadioSet(id="radioSet")

class BodyModule(Static):

    def compose(self) -> ComposeResult:
        yield Label("CIDADE", id="body_label")
        yield Static("\n\tMussum Ipsum, cacilds vidis litro abertis.  Pra lá, depois divoltis porris, paradis. Mé faiz elementum girarzis, nisi eros vermeio. Delegadis gente finis, bibendum egestas augue arcu ut est. Em pé sem cair, deitado sem dormir, sentado sem cochilar e fazendo pose.", id="content")

class TreeModule(Static):

    def compose(self) -> ComposeResult:
        yield Label("LOCALIZAÇÃO", id="tree_label")
        yield Tree(GAME.get_first(loc.Country).name, id="locations")

class ScreenModule(Static):

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield TreeModule(id="tree")
            yield BodyModule(id="body")
            yield RadioModule(id="radio")

class PreemptiveEventSimulatorApp(App):
    BINDINGS = [
        # (key, action_name, description)
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    TITLE = "Preemptive Event Simulator v0.0.002"
    CSS_PATH = "main.tcss"

    def initialize_data(self):
        cre.populate_game(GAME)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield ScreenModule(id="screen")
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def on_mount(self):
        pais: Tree[dict] = self.query_one(Tree)
        pais.root.expand()
        for regiao in GAME.lists(loc.Region):
            regiao_corrente = pais.root.add(regiao.name)
            for estado in GAME.lists(
                loc.State, lambda x: x.region.name == regiao.name
            ):
                estado_corrente = regiao_corrente.add(estado.name)
                for cidade in GAME.lists(
                    loc.City, lambda x: x.state().name == estado.name
                ):
                    estado_corrente.add_leaf(cidade.name, data=cidade)
        pais.focus()

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        node = event.node
        if node.data.__class__ is loc.City:
            body = self.query_one("#content")
            body.update(f'{self.print_city_data(node.data)}')
            self.refresh_teams(node.data)

    def print_city_data(self, city: loc.City) -> str:
        print = city.full_print()
        return print

    def refresh_teams(self, city: loc.City | None) -> None:
        if city is not None:
            teams = GAME.lists(spr.Team, lambda x: x.city == city)
            radioSet = self.query_one(RadioSet)
            radioSet.remove_children()
            for team in teams:
                radioSet.mount(RadioButton(team.name))

    def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
        event.pressed.focus()


if __name__ == "__main__":
    app = PreemptiveEventSimulatorApp()
    app.initialize_data()
    app.run()
