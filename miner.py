import sys,os
import curses
from time import sleep


def start_x(width, text):
    return int((width // 2) - (len(text) // 2) - len(text) % 2)





def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0
    i = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()


        # Declaration of strings
        title = "BogoCoin miner"[:width-1]
        speed = "10.6 KH/s"[:width-1]
        mined = "{} uBTC mined".format(i)[:width-1]
        statusbar = "Press 'q' to exit"

        i = i + 1

        # Centering calculations
        start_y = int((height // 2) - 2) - 4



        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbar)
        stdscr.addstr(height-1, len(statusbar), " " * (width - len(statusbar) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Print title in red and bold
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(start_y, start_x(width, title), title)
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 2, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 4, start_x(width, speed), speed)
        stdscr.addstr(start_y + 6, start_x(width, mined), mined)
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        sleep(0.05)

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()