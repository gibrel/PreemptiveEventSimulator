from __future__ import annotations
from os import name
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Footer, Header, Static, Tree, Label, RadioButton, RadioSet, ListItem, ListView
import helpers.creators as cre
from entities.game import Game
import entities.locations as loc
import entities.sports as spr


GAME = Game()

class ListModule(Static):

    def compose(self) -> ComposeResult:
        yield Label("TIMES", id="listLabel")
        yield ListView(id="listView")

class BodyModule(Static):
    MUSSUM_IPSUM = "\n\tMussum Ipsum, cacilds vidis litro abertis.  Pra lá, depois divoltis porris, paradis. Mé faiz elementum girarzis, nisi eros vermeio. Delegadis gente finis, bibendum egestas augue arcu ut est. Em pé sem cair, deitado sem dormir, sentado sem cochilar e fazendo pose."

    def compose(self) -> ComposeResult:
        yield Label("CIDADE", id="bodyLabel")
        yield Static(self.MUSSUM_IPSUM, id="content")
        yield Label("TEAM", id="teamLabel")
        yield Static(self.MUSSUM_IPSUM, id="teamContent")

class TreeModule(Static):

    def compose(self) -> ComposeResult:
        yield Label("LOCALIZAÇÃO", id="treeLabel")
        yield Tree(GAME.get_first(loc.Country).name, id="locations")

class ScreenModule(Static):

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield TreeModule(id="tree")
            yield BodyModule(id="body")
            yield ListModule(id="list")

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
            self.selectedCity = node.data
            body = self.query_one("#content")
            body.update(f'{self.print_city_data(node.data)}')
            self.refresh_teams(node.data)

    def print_city_data(self, city: loc.City) -> str:
        print = city.full_print()
        return print

    def refresh_teams(self, city: loc.City | None) -> None:
        if city is not None:
            teams = GAME.lists(spr.Team, lambda x: x.city == city)
            listView = self.query_one(ListView)
            listView.remove_children()
            for team in teams:
                listView.mount(ListItem(Label(team.name), name=team.name))

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        teamName = event.item.name
        teamContent = self.query_one("#teamContent")
        if self.selectedCity is None:
            teamContent.update(f"{teamName}")
        else:
            team = GAME.get_first(spr.Team, lambda x: x.city == self.selectedCity and x.name == teamName )
            teamContent.update(f"\n{self.selectedCity.name}\n{team.name}\n{teamName}")


if __name__ == "__main__":
    app = PreemptiveEventSimulatorApp()
    app.initialize_data()
    app.run()
