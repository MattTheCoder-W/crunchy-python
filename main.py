import itertools
import os
import sys
import math
from random import choice
import argparse
os.system("cls")

in_args = []
try:
    if sys.argv[1] != "-i":
        ap = argparse.ArgumentParser()
        ap.add_argument('minimum-length', type=str, help="Minimum length of wordlist word")
        ap.add_argument('maximum-length', type=str, help="Maximum length of wordlist word")
        ap.add_argument('chars', type=str, help="Characters for generating words")

        ap.add_argument('-o', '--output', type=str, help="Output file (if needed)")
        ap.add_argument('-i', '--interactive', action="store_true", help="Interactive mode of this script")
        in_args = vars(ap.parse_args())
except IndexError:
    print("Usage: python crunchy.py <min-length> <max-length> <chars> [-o] [-i]")
    exit()


class Color:
    BLUE = u'\033[94m'
    GREEN = u'\033[92m'
    YELLOW = u'\033[93m'
    RED = u'\033[91m'
    END = u'\033[0m'


def colored(text, color="yellow"):
    if color.lower() == "yellow":
        color = Color.YELLOW
    elif color.lower() == "blue":
        color = Color.BLUE
    elif color.lower() == "red":
        color = Color.RED
    elif color.lower() == "green":
        color = Color.GREEN
    else:
        return "COLORING ERROR"
    return str(color + text + Color.END)


def print_banner():
    banner_width = 97
    center = int((WIDTH - banner_width) / 2)
    with open('banner.txt', 'rb') as infile:
        for line in infile.readlines():
            print(" " * center + line.decode().replace("\n", ''))
    for j in range(3):
        if j % 2 == 0:
            print(" " * center + "=" * banner_width)
        else:
            quote = choice(QUOTES)
            center_quote = int((banner_width - len(quote)) / 2) - 2
            print(" " * center + ">" * center_quote + " " + quote + " " + ">" * (center_quote + 2))


def get_data():
    try:
        print(colored(">>> ", "blue") + "Minimum word length: ", end="")
        in_min = int(input())
        print(colored(">>> ", "blue") + "Maximum word length: ", end="")
        in_max = int(input())
        if in_min > in_max:
            print(colored(">>> ", "red") + "Min length cannot be bigger than max length, you idiot...")
            exit()
        while True:
            print(colored(">>> ", "blue") + "Characters in words ('<h>' for help): ", end="")
            in_chars = str(input())
            if in_chars == "<h>":
                prefix = "\t"
                print(prefix + colored(">>> ", "yellow") + "Custom commands for characters choice!" + colored(" <<<",
                                                                                                              "yellow"))
                print(prefix + colored(">>> ", "yellow") + "<A> for big alphabet")
                print(prefix + colored(">>> ", "yellow") + "<a> for small alphabet")
                print(prefix + colored(">>> ", "yellow") + "<0> for digits")
                print(
                    prefix + colored(">>> ", "yellow") + "You can mix them! ex: <a><0><A> --> 'abcd....0123...ABCD...'")
                continue
            else:
                in_chars = in_chars.replace('<a>', SMALL).replace("<A>", BIG).replace("<0>", DIGITS)
                break
        return [in_min, in_max, in_chars]
    except KeyboardInterrupt:
        print('\n' + colored(">>> ", "red") + "Stopping")
        exit()


def estimate(lens, chars):
    # Get estimated size and length of wordlist (might not be 100% accurate)
    all_len = 0
    all_size = 0
    for k in lens:
        cur_len = int((math.factorial(len(chars) + k - 1) / (math.factorial(k) * math.factorial(len(chars) - 1))) * 2)
        all_len += cur_len
        all_size += cur_len * (k + 2)

    print(colored(">>> ",
                  "yellow") + f"Wordlist will have {all_len} words, which is about {all_size} bytes ({round(all_size / 1000000, 4)} MB)!")
    return all_len


def dosave():
    # Ask for saving file
    print(colored(">>>", "green") + " File to save wordlist in(Empty for not saving): ", end="")
    do_filenm = str(input())
    if do_filenm == "":
        notsaving = True
        print(colored(">>> ", "yellow") + "Not saving mode ON!")
    else:
        notsaving = False
    return [notsaving, do_filenm]


def generate(gen_lens, all_lens, gen_chars):
    gen_wordlist = []
    for i in gen_lens:
        try:
            print(colored(">>> ", "green") + "Generating started!")
            for index, combination in enumerate(list(itertools.combinations_with_replacement(gen_chars, i))):
                combination = list(combination)
                gen_wordlist.append(''.join(combination))
                if combination[::-1] != combination:
                    gen_wordlist.append(''.join(combination[::-1]))
                if index % 1000000 == 0:
                    print(f"{round(index / all_lens * 200, 2)}%              ", end="\r")
                if len(gen_wordlist) > 500000000:
                    print("\n" + colored(">>> ", "red") + "Reached memory limit!!! Stopping!")
                    gen_wordlist = []
                    exit()
        except MemoryError:
            print("\n" + colored(">>> ", "red") + "Reached memory limit!!! Stopping!")
            gen_wordlist = []
            exit()
    return gen_wordlist


def save(savingmode, filename, save_wordlist):
    if not savingmode:
        with open(filename, 'w') as f:
            for cur_word in save_wordlist[:-1]:
                f.write(cur_word + "\n")
            f.write(save_wordlist[-1])
            f.close()
        print(colored(">>> ", "green") + f"Wordlist saved to file: {filename}")


def calculate_size(wrdlist):
    all_size = 0
    for word in wrdlist:
        all_size += len(word) + 2
    all_size -= 2
    return all_size


def interactive():
    # Main Interactive Program Script
    try:
        print_banner()
        min, max, chars = get_data()

        lens = list(range(min, max + 1))
        all_len = estimate(lens, chars)
        notSaving, filenm = dosave()
        wordlist = generate(lens, all_len, chars)

        size = calculate_size(wordlist)
        print(colored(">>> ", "yellow") + f"(Actual) wordlist has {len(wordlist)} words!")
        print(colored(">>> ", "yellow") +
              f"(Actual) File will have {size} " + colored("bytes", "green") +
              f" -> {round(size / 1000, 2)} " + colored("KB", "yellow") +
              f" -> {int(size / 1000000)} " + colored("MB", "red") + "!")
        save(notSaving, filenm, wordlist)
    except KeyboardInterrupt:
        print('\n' + colored(">>> ", "red") + "Stopping")
        exit()


def standard():
    # Main Program Script
    try:
        min, max, chars = [int(in_args['minimum-length']), int(in_args['maximum-length']), in_args['chars']]

        lens = list(range(min, max + 1))
        all_len = estimate(lens, chars)
        if in_args['output'] is not None:
            notSaving = False
            filenm = in_args['output']
        else:
            notSaving = True
            filenm = ""
        wordlist = generate(lens, all_len, chars)

        size = calculate_size(wordlist)
        print(colored(">>> ", "yellow") + f"(Actual) wordlist has {len(wordlist)} words!")
        print(colored(">>> ", "yellow") +
              f"(Actual) File will have {size} " + colored("bytes", "green") +
              f" -> {round(size / 1000, 2)} " + colored("KB", "yellow") +
              f" -> {int(size / 1000000)} " + colored("MB", "red") + "!")
        save(notSaving, filenm, wordlist)
    except KeyboardInterrupt:
        print('\n' + colored(">>> ", "red") + "Stopping")
        exit()


QUOTES = ['Why are you beating me so hard?', "i don't have infinite memory...", "Please, nothing longer that 500*10^6",
          "Hi, friend!", "Hello?", "Matt had created me!", "I see you (눈_눈)"]
SPECIAL_CHARS = ['<a>', '<A>', '<0>']
SMALL = "abcdefghijklmnopqrstuvwxyz"
BIG = SMALL.upper()
DIGITS = "0123456789"
WIDTH = list(os.get_terminal_size())[0]

if in_args['interactive']:
    interactive()
else:
    standard()
