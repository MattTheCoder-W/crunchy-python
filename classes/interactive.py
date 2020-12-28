from os import get_terminal_size
from random import choice
from classes.message import message

QUOTES = ['Why are you beating me so hard?', "i don't have infinite memory...",
          "Please, nothing longer that 500*10^6",
          "Hi, friend!", "Hello?", "Matt had created me!", "I see you (눈_눈)"]
WIDTH = get_terminal_size()[0]
SMALL = "abcdefghijklmnopqrstuvwxyz"
BIG = SMALL.upper()
DIGITS = "0123456789"


class Interactive:
    def __init__(self):
        self.showbanner()
        self.args = self.getdata()

    def getargs(self):
        return self.args

    @staticmethod
    def dosave():
        message("File to save wordlist in(Empty for not saving): ", "question", end="")
        filenm = str(input())
        if filenm == "":
            notsaving = True
            message("Not saving mode ON!", "info")
        else:
            notsaving = False
        return {"output": filenm, "notsaving": notsaving}

    @staticmethod
    def getdata():
        try:
            message("Minimum word length: ", "question", end="")
            in_min = str(input())
            message("Maximum word length: ", "question", end="")
            in_max = str(input())
            while True:
                message("Characters in words ('<h>' for help): ", "question", end="")
                in_chars = str(input())
                if in_chars == "<h>":
                    message("Custom commands for characters choice!", "info", prefix="\t")
                    message("<A> for big alphabet", "info", prefix="\t")
                    message("<a> for small alphabet", "info", prefix="\t")
                    message("<0> for digits", "info", prefix="\t")
                    message("You can mix them! ex: <a><0><A> --> 'abcd....0123...ABCD...'", "info", prefix="\t")
                    continue
                else:
                    in_chars = in_chars.replace('<a>', SMALL).replace("<A>", BIG).replace("<0>", DIGITS)
                    break
            return {"min": in_min, "max": in_max, "chars": in_chars}
        except KeyboardInterrupt:
            message("Stopping", "warning", prefix="\n")
            exit()

    @staticmethod
    def showbanner(quiet=False):
        banner_width = 97
        center = int((WIDTH - banner_width) / 2)
        if not quiet:
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
