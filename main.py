#!/usr/bin/python
import curses
import time
from curses import wrapper

TREE = """
..........................★.
........................./.\\
......................./.....\\
...................../.1.......\\
.................../..4.4....2...\\
................./__....4..2.....__\\
................../......1....4.4.\\
................/2.....2.......1.3..\\
............../....2.......3..3.......\\
............/..........2........1.....1.\\
........../__......3.......2...2.1..1...__\\
.........../....3........1...1....2......\\
........./.3..3.......1......3......2.2..44\\
......./.......1..1..............3....4.2....\\
...../......1.......................3......2...\\
.../............1...............4......3..3......\\
./_________________________________________________\\
....................|...........|
....................|...........|
....................|...........|
....................|___________|
"""

class Pattern(object):
    def __init__(self, pat):
        self.char = pat[0]
        self.pattern = pat[1:]
        self.pos = -1

    def next(self):
        self.pos = (self.pos + 1) % len(self.pattern)
        return self.pattern[self.pos] 

    def chr(self):
        return self.char

def main(w):
    pattern_specs = (
            ('*', 2, 3, 4),
            ('o', 3, 4, 5), 
            ('+', 4, 5, 2), 
            ('/', 5, 2, 3)
    )
    patterns = [Pattern(pat) for pat in pattern_specs]
    
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    w.clear()

    while True:
        next_colors = [pat.next() for pat in patterns]
        for (i, line) in enumerate(TREE.split('\n')):
            line = line.replace('.', ' ')
            if i == 1:
                # Start lights yellow
                line_color = 3
            else: 
                line_color = 1

            w.addstr(i, 0, line, curses.color_pair(line_color))

            for (pat, color) in enumerate(next_colors):
                c = str(pat + 1)
                pos = 0
                while True:
                    pos = line.find(c, pos + 1)
                    if pos < 0:
                        break
                    w.addstr(i, pos, patterns[pat].chr(), curses.color_pair(color))
        w.refresh()
        time.sleep(1)

if __name__ == '__main__':
    try: 
        wrapper(main)
    except KeyboardInterrupt:
        # ignore KeyboardInterrupt error because it is ugly
        pass
    # main(curses.initscr())
