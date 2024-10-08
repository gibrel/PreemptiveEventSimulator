from time import monotonic
from textual import on
from textual.app import App
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Static


class TimeDisplay(Static):
    accumulated_time = 0
    time_elapsed = reactive(0)
    start_time = monotonic()

    def on_mount(self):
        self.update_timer = self.set_interval(
            1 / 60, self.update_time_elapsed, pause=True
        )

    def update_time_elapsed(self):
        self.time_elapsed = self.accumulated_time + monotonic() - self.start_time

    def watch_time_elapsed(self):
        time = self.time_elapsed
        time, seconds = divmod(time, 60)
        hours, minutes = divmod(time, 60)
        time_string = f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}"
        self.update(time_string)

    def start(self):
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self):
        self.accumulated_time = self.time_elapsed
        self.update_timer.pause()

    def reset(self):
        self.accumulated_time = 0
        self.time_elapsed = 0


class Stopwatch(Static):

    @on(Button.Pressed, "#start")
    def start_stopwatch(self):
        self.add_class("started")
        self.query_one(TimeDisplay).start()
        reset_button = self.query_one("#reset")
        reset_button.add_class("hidden")

    @on(Button.Pressed, "#stop")
    def stop_stopwatch(self):
        self.remove_class("started")
        self.query_one(TimeDisplay).stop()
        reset_button = self.query_one("#reset")
        reset_button.remove_class("hidden")

    @on(Button.Pressed, "#reset")
    def reset_stopwatch(self):
        self.query_one(TimeDisplay).reset()

    def compose(self):
        yield Button("Start", variant="success", id="start")
        yield Button("Stop", variant="error", id="stop", classes="hidden")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00.000")


class TextualTimerApp(App):
    BINDINGS = [
        # (key, action_name, description)
        ("d", "toggle_dark_mode", "Toggle dark mode"),
        ("a", "add_stopwatch", "Add stopwatch"),
        ("r", "remove_stopwatch", "Remove last stopwatch"),
        ("q", "exit_app", "Exit Textual Timer App"),
    ]

    CSS_PATH = "textual_timer.tcss"

    def compose(self):
        yield Header(show_clock=True)
        yield Footer()
        with ScrollableContainer(id="stopwatches"):
            yield Stopwatch()
            yield Stopwatch()
            yield Stopwatch()

    def action_toggle_dark_mode(self):
        self.dark = not self.dark

    def action_add_stopwatch(self):
        stopwatch = Stopwatch()
        container = self.query_one("#stopwatches")
        container.mount(stopwatch)
        stopwatch.scroll_visible()

    def action_remove_stopwatch(self):
        stopwatches = self.query(Stopwatch)
        if stopwatches:
            stopwatches.last().remove()

    def action_exit_app(self):
        self.app.exit()


if __name__ == "__main__":
    TextualTimerApp().run()
