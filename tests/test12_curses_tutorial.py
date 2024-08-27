from tests.base_test import BaseTest
import os
import curses
from curses import wrapper
from services.curses_service import print_center


class MainTest(BaseTest):
    test_description = "Test curses debug."
    file_name = os.path.basename(__file__)

    def run(self):
        try:
            os.environ['TERM'] = 'xterm-256color'

            def main(stdscr):
                curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
                OLD_TERMINAL_BLACK_GREEN = curses.color_pair(1)

                stdscr.clear()
                stdscr.bkgd(' ', OLD_TERMINAL_BLACK_GREEN)

                stdscr.addstr("hello repeat\n")
                stdscr.addstr("hello repeat\n", curses.A_BOLD)
                stdscr.addstr("hello repeat\n", curses.A_ITALIC)
                stdscr.addstr("hello repeat\n", curses.A_REVERSE)

                print_center(stdscr, f"Hello World!\nThat is a(n): {type(stdscr)}", OLD_TERMINAL_BLACK_GREEN)

                stdscr.refresh()
                stdscr.getch()

            wrapper(main)

            pass
        except Exception as e:
            self.error(e)


def test():
    MainTest()
