#!/usr/bin/env python3
import curses
import random
import time

# Small terminal snake game using curses (stdlib only).

WIDTH = 40
HEIGHT = 20
TICK = 0.12  # seconds per frame


def center(msg, width):
    if len(msg) >= width:
        return msg
    pad = (width - len(msg)) // 2
    return " " * pad + msg


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)

    use_color = False
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)  # snake
        curses.init_pair(2, curses.COLOR_RED, -1)    # food
        curses.init_pair(3, curses.COLOR_CYAN, -1)   # border
        curses.init_pair(4, curses.COLOR_YELLOW, -1) # header
        use_color = True

    # Game window with a border
    win = curses.newwin(HEIGHT + 2, WIDTH + 2, 1, 2)
    win.nodelay(True)
    win.keypad(True)

    snake = [(HEIGHT // 2, WIDTH // 2), (HEIGHT // 2, WIDTH // 2 - 1)]
    direction = (0, 1)
    score = 0

    def spawn_food():
        while True:
            pos = (random.randint(1, HEIGHT), random.randint(1, WIDTH))
            if pos not in snake:
                return pos

    food = spawn_food()

    while True:
        stdscr.erase()
        if use_color:
            stdscr.attron(curses.color_pair(4))
        stdscr.addstr(0, 2, center("Snake  |  Arrows/WASD  |  Q to quit", 50))
        if use_color:
            stdscr.attroff(curses.color_pair(4))
        stdscr.addstr(0, 55, f"Score: {score}")
        stdscr.refresh()

        win.erase()
        if use_color:
            win.attron(curses.color_pair(3))
        win.border()
        if use_color:
            win.attroff(curses.color_pair(3))
        # Chessboard-style background inside the border.
        for y in range(1, HEIGHT + 1):
            for x in range(1, WIDTH + 1):
                win.addch(y, x, '.' if (x + y) % 2 == 0 else ':')

        # Input
        key = win.getch()
        if key in (ord('q'), ord('Q')):
            return
        elif key in (curses.KEY_UP, ord('w'), ord('W')) and direction != (1, 0):
            direction = (-1, 0)
        elif key in (curses.KEY_DOWN, ord('s'), ord('S')) and direction != (-1, 0):
            direction = (1, 0)
        elif key in (curses.KEY_LEFT, ord('a'), ord('A')) and direction != (0, 1):
            direction = (0, -1)
        elif key in (curses.KEY_RIGHT, ord('d'), ord('D')) and direction != (0, -1):
            direction = (0, 1)

        # Move
        head_y, head_x = snake[0]
        dy, dx = direction
        new_head = (head_y + dy, head_x + dx)

        # Collision with walls
        if new_head[0] == 0 or new_head[0] == HEIGHT + 1 or new_head[1] == 0 or new_head[1] == WIDTH + 1:
            break
        # Collision with self
        if new_head in snake:
            break

        snake.insert(0, new_head)

        # Food
        if new_head == food:
            score += 1
            food = spawn_food()
        else:
            snake.pop()

        # Draw
        if use_color:
            win.attron(curses.color_pair(2))
        win.addch(food[0], food[1], '*')
        if use_color:
            win.attroff(curses.color_pair(2))
        if use_color:
            win.attron(curses.color_pair(1))
        for i, (y, x) in enumerate(snake):
            win.addch(y, x, 'O' if i == 0 else 'o')
        if use_color:
            win.attroff(curses.color_pair(1))

        win.refresh()
        time.sleep(TICK)

    # Game over
    stdscr.nodelay(False)
    stdscr.addstr(HEIGHT + 4, 2, "Game Over. Press any key to exit.")
    stdscr.refresh()
    stdscr.getch()


def run():
    curses.wrapper(main)


if __name__ == "__main__":
    run()
