import argparse
from classes.interactive import Interactive
from classes.message import message


def getsize(chars, args):
    lens = list(range(int(args['min']), int(args['max']) + 1))
    data = {"len": 0, "size": 0}
    for k in lens:
        cur_len = len(chars) ** k
        data['len'] += cur_len
        data['size'] += cur_len * (k + 2)
    data['size'] -= 2
    if data['size'] < 1000000:
        message(f"Wordlist will have {data['len']} words, which is about {data['size']} bytes" +
                f"({round(data['size'] / 1000, 3)}KB)!", "info")
    elif data['size'] < 1000000000:
        message(f"Wordlist will have {data['len']} words, which is about {data['size']} bytes" +
                f"({round(data['size'] / 1000000, 3)}MB)!", "info")
    else:
        message(f"Wordlist will have {data['len']} words, which is about {data['size']} bytes" +
                f"({round(data['size'] / 1000000000, 3)}GB)!", "info")


def dosave():
    message("File to save wordlist in(Empty for not saving): ", "question", end="")
    filenm = str(input())
    if filenm == "":
        notsaving = True
        message("Not saving mode ON!", "info")
    else:
        notsaving = False
    return {"output": filenm, "notsaving": notsaving}


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
            try:
                # Open interactive mode
                self.args = Interactive().getargs()
                self.checkargs()
                getsize(self.args['chars'], self.args)
                temp = dosave()
                self.args['output'] = temp['output']
                self.args['notsaving'] = temp['notsaving']
                self.checkout()
            except KeyboardInterrupt:
                message("Stopping", "info")
                exit()
        else:
            self.checkargs()
            self.checkout()

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

    def checkout(self):
        if self.args['output'] in [None, ""]:
            self.args['notsaving'] = True
        else:
            self.args['notsaving'] = False
