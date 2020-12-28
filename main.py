from classes.args import Arguments
from classes.generate import Generator

if __name__ == "__main__":
    args = Arguments().getargs()
    Generator(args)