from assets.terminal import TermColors as Term_Colors
from assets.commandhandler import CommandHandler
from colorama import Fore
from os import execv
from time import sleep
from subprocess import check_call
from sys import executable, argv

class Terminal:
    """
    A class for DeAuthy's colors in the terminal and formatting, such as ``bold`` and ``end``

    Attributes
    -------
    • ``
    """

    def __init__(self) -> Term_Colors:
        self.white       = Fore.WHITE
        self.light_white = Fore.LIGHTBLACK_EX
        self.red         = Fore.RED
        self.yellow      = Fore.LIGHTYELLOW_EX
        self.light_green = Fore.LIGHTGREEN_EX
        self.magenta     = Fore.MAGENTA
        self.cyan        = Fore.CYAN
        self.blue        = Fore.BLUE
        self.light_blue  = Fore.LIGHTBLUE_EX
        self.bold        = '\033[1m'
        self.underline   = '\033[4m'
        self.end         = '\033[0m'
        self.deAuThY = self.white + "[" + self.red + "D" + self.yellow + "E" + self.light_green + "A" + self.magenta + "U" + self.cyan + "T" + self.blue + "H" + self.red + "Y" + self.white + "]"

    def tell_issue(self, msg: str):
        d_wut = self.white + f"{self.bold}[" + self.red + "!" + self.white + f"]{self.end}{self.light_white} "
        print(self.deAuThY + d_wut + msg)

    def inform(self, msg: str, entire_color=Fore.LIGHTBLACK_EX):
        d_hey = self.white + f"{self.bold}[" + self.light_green + "+" + self.white + f"]{self.end}{self.light_white} "
        print(self.deAuThY + d_hey + entire_color + msg)

    def prompt(self, question: str, allowed_replies: list[str], ending_color=Fore.WHITE) -> str:
        d_huh = self.white + f"{self.bold}[" + self.light_blue + "?" + self.white + f"]{self.end}{self.light_white} "
        reply = input(self.deAuThY + d_huh + f"{self.light_white}{question}{self.bold}>{self.end} {ending_color}")
        if reply.lower() in CommandHandler.supported_commands_debian_based_distros:
            print(self.end)
            check_call(reply)
            reply = self.prompt(question, allowed_replies, ending_color)
            return reply
        elif reply in CommandHandler.own_commands:
            CommandHandler.Own_Cmds.handle_own_cmd[reply]()
            reply = self.prompt(question, allowed_replies, ending_color)
            return reply
        elif reply.lower() in allowed_replies:
            return reply
        else:
            if allowed_replies[0].lower() == "any":
                return reply
            else:
                self.tell_issue(f"{self.red}That's not a valid {self.bold}{self.red}reply{self.end}{self.red} :/")
                reply = self.prompt(question=question, allowed_replies=allowed_replies)
                return reply

    @property
    def End(self):
        return self.end

    @property
    def Bold(self):
        return self.bold

    @property
    def White(self):
        return self.white

    @property
    def Light_green(self):
        return self.light_green

    @property
    def Red(self):
        return self.red

    @property
    def Light_white(self):
        return self.light_white

    @property
    def Yellow(self):
        return self.yellow

    @property
    def Light_blue(self):
        return self.light_blue

    @property
    def Magenta(self):
        return self.magenta

    @property
    def Cyan(self):
        return self.cyan

    @property
    def Blue(self):
        return self.blue

    @property
    def Underline(self):
        return self.underline

    @property
    def DeAuThY(self):
        deauthy = self.deAuThY
        return deauthy