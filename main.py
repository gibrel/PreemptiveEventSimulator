from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header, Static, Tree
# import helpers.creators as cre
from entities.game import Game
import entities.locations as loc


class PreemptiveEventSimulatorApp(App):
    BINDINGS = [
        # (key, action_name, description)
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    TITLE = "Preemptive Event Simulator v0.0.001"
    CSS_PATH = "main.tcss"
    app_game: Game
    locations_tree = None
    main_body = None

    def initialize_data(self):
        self.app_game = Game()
        # cre.populate_game(self.app_game)

    def compose(self) -> ComposeResult:
        self.locations_tree = Tree(self.app_game.get_first(loc.Country).name)
        self.main_body = Static('\n' + (self.TITLE + " ")* 10 + '\n\n', id="body")
        yield Header(show_clock=True)
        with Container(id="sidebar"):
            yield self.locations_tree
        with Container(id="main"):
            yield self.main_body
        yield Footer()

    def on_mount(self):
        pais: Tree[dict] = self.locations_tree
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
        self.query_one(Tree).focus()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        node = event.node
        print_message = f"Node highlighted: {node.label}"
        print(print_message)
        if node.data.__class__ is loc.City:
            self.main_body.update(f'{node.data.full_print()}')

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        node = event.node
        print_message = f"Node selected: {node.label}"
        print(print_message)

    def on_tree_node_collapsed(self, event: Tree.NodeCollapsed) -> None:
        node = event.node
        print_message = f"Node collapsed: {node.label}"
        print(print_message)

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node = event.node
        print_message = f"Node expanded: {node.label}"
        print(print_message)


if __name__ == "__main__":
    app = PreemptiveEventSimulatorApp()
    app.initialize_data()
    app.run()
