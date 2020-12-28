class Progress:
    def __init__(self, start=0, tabs=20, prog_char="#", spc=" "):
        self.prog_char = prog_char
        self.tabs = tabs
        self.percentage = start
        self.spc = spc

    def next(self, suffix="", cur_perc=0):
        line = "{" + format(round(cur_perc*100, 0), '.0f') + "%} ["
        for i in range(self.tabs):
            val = i + 1
            cur = val / self.tabs
            if cur <= cur_perc:
                line += self.prog_char
            else:
                line += self.spc
        line += "]"
        line += suffix
        print(line, end="\r")
