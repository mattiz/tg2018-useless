import os
import curses
from time import sleep
import threading
import hashlib
import timeit
from math import ceil



def mineOneUnit():
    hashlib.sha256(hashlib.sha256(os.urandom(10)).digest())


class MinerThread (threading.Thread):
    num = 0
    speed = 0

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        i = 1

        while self.stopped() == False:
            # Time execution of 10.000 units of work
            t = timeit.timeit( 'mineOneUnit()', setup="from __main__ import mineOneUnit", number=10000)

            # Refersh speed
            if i % 100 == 0:
                self.speed = ceil( ((1 / t) * 10000) / 1000 )

            # Refresh number of uBOC
            if i % 1000 == 0:
                self.num = self.num + 1
                i = 0

            i += 1


def start_x(width, text):
    return int((width // 2) - (len(text) // 2) - len(text) % 2)


def draw(stdscr):
    key = 0

    # Setup
    stdscr.nodelay(True)
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    minerThread = MinerThread("Thread-1")
    minerThread.start()

    # Loop until 'q' is pressed
    while (key != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Centering calculations
        start_y = int((height // 2) - 2) - 4

        # Declaration of strings
        title = "BogoCoin miner"[:width-1]
        speed = "{} KH/s".format( minerThread.speed )[:width-1]
        mined = "{} µBOC mined".format( minerThread.num )[:width-1]
        statusbar = "Press 'q' to exit | Useless contribution by MooG"

        # Status bar
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

        stdscr.refresh()
        key = stdscr.getch()

        sleep(0.05)


    minerThread.stop()


def main():
    curses.wrapper(draw)

if __name__ == "__main__":
    main()