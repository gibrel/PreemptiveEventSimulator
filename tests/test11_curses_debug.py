from tests.base_test import BaseTest
import os
from curses import wrapper


class MainTest(BaseTest):
    test_description = "Test curses debug."
    file_name = os.path.basename(__file__)

    def run(self):
        try:
            os.environ['TERM'] = 'xterm-256color'

            def main(stdscr):
                # Clear screen
                stdscr.clear()

                # This raises ZeroDivisionError when i == 10.
                for i in range(0, 11):
                    v = i - 10
                    stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10 / v))

                stdscr.refresh()
                stdscr.getkey()

            wrapper(main)
        except Exception as e:
            self.error(e)


def test():
    MainTest()
