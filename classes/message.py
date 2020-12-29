import colorama
colorama.init()

BLUE = u'\033[94m'
GREEN = u'\033[92m'
YELLOW = u'\033[93m'
RED = u'\033[91m'
WHITE = u''
END = u'\033[0m'


def message(text, msgtype="MESSAGE", end="\n", prefix=""):
    msgtype = msgtype.lower()
    msgicon = "="
    if msgtype == "info":
        msgicon = f"{YELLOW}!{END}"
    elif msgtype == "success":
        msgicon = f"{GREEN}+{END}"
    elif msgtype == "error":
        msgicon = f"{RED}-{END}"
    elif msgtype == "warning":
        msgicon = f"{RED}#{END}"
    elif msgtype == "question":
        msgicon = f"{YELLOW}?{END}"
    print(f"{prefix}[{msgicon}] > {text}", end=end)