from classes.message import message
import itertools
from classes.progress import Progress
from os import get_terminal_size


class Generator:
    def __init__(self, args):
        self.args = args
        self.lens = list(range(int(self.args['min']), int(self.args['max']) + 1))
        self.data = self.getsize()
        self.wordlist = self.generate()
        self.getactualsize()
        if not self.args['notsaving']:
            self.save()

    def getsize(self):
        data = {"len": 0, "size": 0}
        for k in self.lens:
            cur_len = len(self.args['chars']) ** k
            data['len'] += cur_len
            data['size'] += cur_len * (k + 2)
        data['size'] -= 2
        return data

    def getactualsize(self):
        size = 0
        for word in self.wordlist:
            size += len(word) + 2
        size -= 2
        if size < 1000:
            message(f"Actual size of file is {size} bytes with {len(self.wordlist)} words!", "info")
        elif size < 1000000:
            message(f"Actual size of file is {round(size/1000, 2)} KB with {len(self.wordlist)} words!", "info")
        elif size < 1000000000:
            message(f"Actual size of file is {round(size/1000000, 1)} MB with {len(self.wordlist)} words!", "info")

    def generate(self):
        wordlist = []
        message("Generating started!", "info")
        index = 0
        prg = Progress(tabs=int(get_terminal_size()[0]/2), spc="-")
        for i in self.lens:
            try:
                for combination in list(map("".join, itertools.product(self.args['chars'], repeat=i))):
                    wordlist.append(combination)
                    index += 1
                    if self.data['len'] > 10000 and index % 1500000 == 0:
                        prg.next(cur_perc=round(index / self.data['len'], 2))
            except MemoryError:
                message("Reached memory limit!!! Stopping!", "error", prefix="\n")
                wordlist = []
                exit()
        prg.next(cur_perc=1)
        print()
        message("Wordlist generated!", "success")
        return wordlist

    def save(self):
        with open(self.args['output'], 'w') as f:
            for cur_word in self.wordlist[:-1]:
                f.write(cur_word + "\n")
            f.write(self.wordlist[-1])
            f.close()
        message(f"Wordlist saved to file: {self.args['output']}", "success")
