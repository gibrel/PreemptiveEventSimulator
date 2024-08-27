import os
import curses
from curses import wrapper

os.environ['TERM'] = 'xterm-256color'


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    OLD_TERMINAL_BLACK_GREEN = curses.color_pair(1)

    stdscr.clear()
    num_rows, num_cols = stdscr.getmaxyx()
    stdscr.bkgd(' ', OLD_TERMINAL_BLACK_GREEN)
    stdscr.addstr("hello normal\n")
    stdscr.addstr("hello in bold\n", curses.A_BOLD)
    stdscr.addstr("hello in italic\n", curses.A_ITALIC)
    stdscr.addstr("hello reverse\n", curses.A_REVERSE)
    stdscr.addstr(f"\nHello World!\nThat is a(n): {type(stdscr)}\n")
    stdscr.addstr(f"\tA total of {num_rows} rows (y) and {num_cols} cols (x).\n")
    stdscr.refresh()
    stdscr.getch()

    stdscr.clear()
    new_num_rows, new_num_cols = stdscr.getmaxyx()
    stdscr.addstr(f"\tA total of {new_num_rows} rows (y) and {new_num_cols} cols (x).\n")
    stdscr.refresh()
    stdscr.getch()


if __name__ == '__main__':
    wrapper(main)
