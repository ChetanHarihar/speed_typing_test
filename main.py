import curses
from curses import wrapper
import random
import time

# Function to load a random line from a file
def load_text(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    return random.choice(lines).strip()

# Function to display the typing test
def wpm_test(stdscr, string, key_list, wrong_keys, wpm=0):
    for i in range(len(key_list)):
        if i in wrong_keys:
            stdscr.addstr(string[i], curses.color_pair(3))  # Display wrong keys in red
        else:
            stdscr.addstr(string[i], curses.color_pair(2))  # Display correct keys in green
    stdscr.addstr(0, len(key_list), string[len(key_list)], curses.color_pair(4))  # Display current character in black on white
    stdscr.addstr(0, len(key_list) + 1, string[len(key_list) + 1:], curses.color_pair(1))  # Display the remaining text in white on black
    stdscr.addstr(f'\n\nWPM:{wpm}', curses.color_pair(5))  # Display WPM in cyan

# Function to initialize the curses screen
def initialize_screen(stdscr):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Color pair 1: White on Black
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Color pair 2: Green on Black
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # Color pair 3: Red on Black
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Color pair 4: Black on White
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Color pair 5: Cyan on Black

    stdscr.clear()

    stdscr.addstr(0, 0, "Welcome to the Speed Typing Test!", curses.color_pair(1))
    stdscr.addstr("\nPress any key to begin!", curses.color_pair(1))
    stdscr.refresh()
    stdscr.getkey()

# Main function to run the typing test
def main(stdscr):
    while True:
        initialize_screen(stdscr)
        file_name = "lines.txt"
        string = load_text(file_name)

        typing = True
        stdscr.nodelay(True)
        key_list = []
        wrong_keys = set()
        start_time = time.time()
        for index, character in enumerate(string):
            while typing:
                stdscr.clear()
                elapsed_time = max(time.time() - start_time, 1)
                wpm = round(((60 * len(key_list))/elapsed_time)/5)
                wpm_test(stdscr, string, key_list, wrong_keys, wpm)

                try:
                    key = stdscr.getkey()
                except:
                    continue
                
                # If Esc key is pressed, exit typing
                if key == '\x1b':
                    typing = False
                else:
                    # Special case for single inverted comma
                    if key == 'SHF_PADENTER':
                        key = "'"
                        
                    if key == character:
                        key_list.append(key)
                        break
                    else:
                        wrong_keys.add(index)
                        continue
            else:
                break

        stdscr.nodelay(False)

        if typing:
            stdscr.clear()
            stdscr.addstr("Congratulations..! You Completed the test!", curses.color_pair(1))
            stdscr.addstr(f"\nYour Score: {wpm}", curses.color_pair(1))
            stdscr.addstr("\nPress `Esc` to Exit | Press any key to continue typing", curses.color_pair(1))
            key = stdscr.getkey()
            if key == '\x1b':
                break
            else:
                continue
        else:
            return

# Wrapper to run the main function with curses
wrapper(main)