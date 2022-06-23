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
    ----------
    - `tell_issue()`
    - `inform()`
    - `prompt()`
    - `End`
    - `Bold`
    - `White`
    - `Light_green`
    - `Red`
    - `Light_white`
    - `Yellow`
    - `Light_Blue`
    - `Magenta`
    - `Cyan`
    - `Blue`
    - `Underline`
    - `DeAuThY`
    """

    White       = Fore.WHITE
    Light_white = Fore.LIGHTBLACK_EX
    Red         = Fore.RED
    Yellow      = Fore.LIGHTYELLOW_EX
    Light_green = Fore.LIGHTGREEN_EX
    Magenta     = Fore.MAGENTA
    Cyan        = Fore.CYAN
    Blue        = Fore.BLUE
    Light_blue  = Fore.LIGHTBLUE_EX
    Bold        = '\033[1m'
    Underline   = '\033[4m'
    End         = '\033[0m'
    deAuThY = Fore.WHITE + "[" + Fore.RED + "D" + Fore.LIGHTYELLOW_EX + "E" + Fore.LIGHTGREEN_EX + "A" + Fore.MAGENTA + "U" + Fore.CYAN + "T" + Fore.BLUE + "H" + Fore.RED + "Y" + Fore.WHITE + "]"

    def tell_issue(self, msg: str):
        d_wut = self.White + f"{self.Bold}[" + self.Red + "!" + self.White + f"]{self.End}{self.Light_white} "
        print(self.deAuThY + d_wut + msg)

    def inform(self, msg: str, entire_color=Fore.LIGHTBLACK_EX):
        d_hey = self.White + f"{self.Bold}[" + self.Light_green + "+" + self.White + f"]{self.End}{self.Light_white} "
        print(self.deAuThY + d_hey + entire_color + msg)

    def prompt(self, question: str, allowed_replies: list[str], ending_color=Fore.WHITE) -> str:
        d_huh = self.White + f"{self.Bold}[" + self.Light_blue + "?" + self.white + f"]{self.End}{self.Light_white} "
        reply = input(self.deAuThY + d_huh + f"{self.Light_white}{question}{self.Bold}>{self.End} {ending_color}")
        if reply.lower() in CommandHandler.supported_commands_debian_based_distros:
            print(self.End)
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
                self.tell_issue(f"{self.Red}That's not a valid {self.Bold}{self.Red}reply{self.End}{self.Red} :/")
                reply = self.prompt(question=question, allowed_replies=allowed_replies)
                return reply