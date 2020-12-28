import argparse
from classes.interactive import Interactive
from classes.message import message


class Arguments:
    def __init__(self):
        ap = argparse.ArgumentParser()
        ap.add_argument('-m', '--min', type=str, help="Minimum length of wordlist word")
        ap.add_argument('-x', '--max', type=str, help="Maximum length of wordlist word")
        ap.add_argument('-c', '--chars', type=str, help="Characters for generating words")
        ap.add_argument('-o', '--output', type=str, help="Output file (if needed)")
        ap.add_argument('-i', '--interactive', action="store_true", help="Interactive mode of this script")
        self.args = vars(ap.parse_args())
        self.interactive = self.args['interactive']
        if self.interactive:
            # Open interactive mode
            self.args = Interactive().getargs()
        self.checkargs()

    def getargs(self):
        return self.args

    def checkargs(self):
        doexit = False
        if self.args['min'] in [None, ""]:
            message("Please specify minimum length!", "error")
            doexit = True
        if self.args['max'] in [None, ""]:
            message("Please specify maximum length!", "error")
            doexit = True
        if self.args['chars'] in [None, ""]:
            message("Please specify characters!", "error")
            doexit = True
        if doexit:
            exit()
        if int(self.args['min']) > int(self.args['max']):
            message("Min length cannot be bigger than max length, you idiot...", "error")
            exit()
        if self.args['output'] in [None, ""]:
            self.args['notsaving'] = True
        else:
            self.args['notsaving'] = False
