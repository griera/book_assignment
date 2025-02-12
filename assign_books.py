import numpy as np
import pandas as pd
import argparse
import pyfiglet
import time
import re
import os
import random
import shutil
import subprocess
from unidecode import unidecode
from termcolor import colored
from scipy.optimize import linear_sum_assignment

def main():
    args = get_arguments()
    df = load_data(args)
    books, people, preferences = process_data(df, args)
    assignments = assign_books(books, people, preferences, args)
    display_results(assignments, books, people, preferences, args)

def get_arguments():
    parser = argparse.ArgumentParser(
        description="Assign books to people based on preferences.",
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=40)
    )
    parser.add_argument("--csv_file", type=str, help="Path to local CSV file")
    parser.add_argument("--drive_id", type=str, help="Google Drive file ID")
    parser.add_argument("--ascii", action='store_true', help="Enable ASCII art for assignments display")
    parser.add_argument(
        "--ascii_banner", type=str, 
        help="Custom message to display as ASCII art when --ascii is enabled", 
        default=None
    )
    parser.add_argument(
        "--ascii_image", type=str, 
        help=("Path to local JPG image to display as ASCII art when --ascii is enabled. "
              "It requires to install jp2a (https://github.com/cslarsen/jp2a)"), 
        default=None
    )
    parser.add_argument("--evil_mode", action='store_true', help="Enable evil mode (what could possibly go wrong?)")
    parser.add_argument(
        "--evil_name", type=str, 
        help="Name of evil mode's author to display as ASCII art when --ascii and --evil_mode are enabled", 
        default="Evil Mode Demon"
    )
    parser.add_argument(
        "--evil_banner", type=str, 
        help="Custom message to display as ASCII art when --ascii and --evil_mode are enabled", 
        default=None
    )
    parser.add_argument(
        "--evil_image", type=str, 
        help=("Path to local JPG image to display as ASCII art when --ascii and --evil_mode are enabled. "
              "It requires to install jp2a (https://github.com/cslarsen/jp2a)"), 
        default=None
    )
    parser.add_argument("--debug", action='store_true', help="Enable debug mode")
    args = parser.parse_args()

    # Ensure at least one of --csv_file or --drive_id is provided
    if not args.csv_file and not args.drive_id:
        parser.error("You must provide either --csv_file or --drive_id.")
    
    return args

def load_data(args):
    if args.csv_file:
        return pd.read_csv(args.csv_file, index_col=0).iloc[:-2, 2:-1].fillna(0)
    elif args.drive_id:
        csv_url = f"https://docs.google.com/spreadsheets/d/{args.drive_id}/export?format=csv"
        return pd.read_csv(csv_url, index_col=0).iloc[:-2, 2:-1].fillna(0)
    else:
        raise ValueError("Provide a local CSV or Google Drive file ID.")

def process_data(df, args):
    books = df.index.tolist()
    people = df.columns.tolist()
    if len(books) < len(people):
        print("Warning: Not enough unique books to assign to all people.\n")

    # If evil mode is enabled, randomize preference scores
    preferences = np.random.randint(0, 11, size=df.shape) if args.evil_mode else df.to_numpy()
    return books, people, preferences

def print_debug_info(books, people, preferences, args):
    print("Books List (%s items):" %len(books))
    for book in books:
        print(book)
    
    print("\nPeople List (%s items):" %len(people))
    for person in people:
        print(person)
    
    print("\nPreferences Matrix:")
    if args.evil_mode:
        print("Warning! Evil mode enabled:\n- Randomize preference scores\n- Don't convert scores into costs")
    print(preferences, "\n")

def assign_books(books, people, preferences, args):
    # Convert preference scores to cost (Hungarian algorithm minimizes cost)
    # If evil mode is enabled, don't convert preference scores to cost
    cost_matrix = preferences if args.evil_mode else preferences.max() - preferences

    # Solve the assignment problem using the Hungarian algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    return {people[col]: (books[row], preferences[row, col]) for row, col in zip(row_ind, col_ind)}

def display_results(assignments, books, people, preferences, args):
    if args.ascii:
        print_pretty_ascii_assignments(assignments, args)
        os.system('cls' if os.name == 'nt' else 'clear')

    if args.debug:
        print_debug_info(books, people, preferences, args)

    print("Assignments:")
    for person, (book, score) in assignments.items():
        print(f"{person} receives the book: {book} with a score of {score}")

def print_pretty_ascii_assignments(assignments, args):
    width = shutil.get_terminal_size().columns
    font = "future"
    justify = "center"
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    for person, (book, score) in assignments.items():
        os.system('cls' if os.name == 'nt' else 'clear')
        color = random.choice(colors)
        text = unidecode(re.sub(" ", "  ", f"{person} receives the book:\n{book}\nwith a score of {score}"))
        print_colored_ascii_msg(text, color, font, width, justify)
        time.sleep(5)

    if args.ascii_banner:
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(1)
        print_pretty_ascii_banner(args.ascii_banner, colors, width)

    if os.name != "nt" and args.ascii_image and os.path.isfile(args.ascii_image):
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(1)
        print_image_to_ascii(args.ascii_image)

    if args.evil_mode:
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(1)
        print_evil_ascii(args.evil_name, args.evil_banner, width)
        time.sleep(5)
        if os.name != "nt" and args.evil_image and os.path.isfile(args.evil_image):
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(1)
            print_image_to_ascii(args.evil_image)

def print_image_to_ascii(image):
    if shutil.which("jp2a"):
        subprocess.run(["jp2a", "--colors", image])
    else:
        print("Warning: jp2a is not installed. Please install it to use this feature.")

    time.sleep(10)
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored_ascii_msg(text, color, font, width, justify):
    ascii_text = pyfiglet.figlet_format(text, width=width, font=font, justify=justify)
    colored_ascii = colored(ascii_text, color)
    print(colored_ascii)

def print_pretty_ascii_banner(banner, colors, width):
    font = "small"
    text = unidecode(re.sub(" ", "  ", banner))
    ascii_text = pyfiglet.figlet_format(text, width=width, font=font, justify="center")
    for i in range(0,15):
        for c in colors:
            colored_ascii = colored(ascii_text, c)
            print(colored_ascii)
            time.sleep(0.1)
            os.system('cls' if os.name == 'nt' else 'clear')

    time.sleep(1)

def print_evil_ascii(name, banner, width):
    font = "slant"
    color = "red"
    justify = "left"
    if banner:
        text = unidecode(re.sub(" ", "  ", banner))
        print_colored_ascii_msg(text, color, font, width, justify)

    print_demon_face(color)
    if name:
        text = unidecode(re.sub(" ", "  ", name))
        print_colored_ascii_msg(text, color, font, width, justify)

def print_demon_face(color):
    print(colored("      (                      )", color))
    print(colored("      |\    _,--------._    / |", color))
    print(colored("      | `.,'            `. /  |", color))
    print(colored("      `  '              ,-'   '", color))
    print(colored("       \/_         _   (     /", color))
    print(colored("      (,-.`.    ,',-.`. `__,'", color))
    print(colored("       |/#\ ),-','#\`= ,'.` |", color))
    print(colored("       `._/)  -'.\_,'   ) ))|", color))
    print(colored("       /  (_.)\     .   -'//", color))
    print(colored("      (  /\____/\    ) )`'\\", color))
    print(colored("       \ |V----V||  ' ,    \\", color))
    print(colored("        |`- -- -'   ,'   \  \\      _____", color))
    print(colored(" ___    |         .'    \ \  `._,-'     `-", color))
    print(colored("    `.__,`---^---'       \ ` -'", color))
    print(colored("       -.______  \ . /  ______,-", color))
    print(colored("               `.     ,'            ", color))

if __name__ == "__main__":
    main()

