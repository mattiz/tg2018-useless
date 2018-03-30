import sys,os
import curses
from time import sleep
import time
import threading
import hashlib
import timeit
from math import ceil



def mineOne():
    hashlib.sha256(os.urandom(10))


class myThread (threading.Thread):
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

    def getNum(self):
        return self.num

    def getSpeed(self):
        return self.speed

    def run(self):
        print ("Starting " + self.name)

        i = 1

        while self.stopped() == False:
            #print('Running..')

            #t = timeit.timeit( 'hashlib.sha256(os.urandom(10))', number=1000)
            t = timeit.timeit( 'mineOne()', setup="from __main__ import mineOne", number=10000)


            if i % 100 == 0:
                self.speed = ceil( ((1 / t) * 10000) / 1000 )

            if i % 1000 == 0:
                self.num = self.num + 1
                i = 0

            i += 1

            #print(t)


            #sleep(1)

        print ("Exiting " + self.name)




def start_x(width, text):
    return int((width // 2) - (len(text) // 2) - len(text) % 2)





def draw(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.nodelay(True)
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    thread1 = myThread("Thread-1")
    thread1.start()

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()


        # Declaration of strings
        title = "BogoCoin miner"[:width-1]
        speed = "{} KH/s".format( thread1.getSpeed() )[:width-1]
        mined = "{} uBOC mined".format( thread1.getNum() )[:width-1]
        statusbar = "Press 'q' to exit"


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


    thread1.stop()


def main():
    curses.wrapper(draw)

if __name__ == "__main__":
    main()