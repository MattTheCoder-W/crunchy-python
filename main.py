from classes.args import Arguments
from classes.generate import Generator
import os

if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

if __name__ == "__main__":
    args = Arguments().getargs()
    Generator(args)
