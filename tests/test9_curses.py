from tests.base_test import BaseTest
import curses
import os


class MainTest(BaseTest):
    test_description = "Test curses printing colors."
    file_name = os.path.basename(__file__)

    def run(self):
        try:
            os.environ['TERM'] = 'xterm-256color'

            def main(stdscr):
                curses.start_color()
                curses.use_default_colors()
                for i in range(0, curses.COLORS):
                    curses.init_pair(i + 1, i, -1)
                try:
                    for i in range(0, 255):
                        stdscr.addstr(str(i), curses.color_pair(i))
                except curses.ERR:
                    # End of screen reached
                    pass
                stdscr.getch()

            curses.wrapper(main)
        except Exception as e:
            self.error(e)


def test():
    MainTest()
