from ast import Index
from deauthy.commandhandler import CommandHandler
from colorama import Fore
from subprocess import CalledProcessError, check_call

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
    y_n         = f"({Fore.LIGHTGREEN_EX}Y{Fore.WHITE}/{Fore.RED}N{Fore.WHITE})"
    Warning     = f"{Yellow}{Bold}[{Fore.YELLOW}{Bold}warning{Yellow}{Bold}]{End}"
    deAuThY = Fore.WHITE + "[" + Fore.RED + "D" + Fore.LIGHTYELLOW_EX + "E" + Fore.LIGHTGREEN_EX + "A" + Fore.MAGENTA + "U" + Fore.CYAN + "T" + Fore.BLUE + "H" + Fore.RED + "Y" + Fore.WHITE + "]"
    deauthy_non_tag = Fore.RED + "D" + Fore.LIGHTYELLOW_EX + "E" + Fore.LIGHTGREEN_EX + "A" + Fore.MAGENTA + "U" + Fore.CYAN + "T" + Fore.BLUE + "H" + Fore.RED + "Y"

    def tell_issue(msg: str):
        d_wut = Terminal.White + f"{Terminal.Bold}[" + Terminal.Red + "!" + Terminal.White + f"]{Terminal.End}{Terminal.Light_white} "
        print(Terminal.deAuThY + d_wut + msg)

    def inform(msg: str, entire_color=Fore.LIGHTBLACK_EX):
        d_hey = Terminal.White + f"{Terminal.Bold}[" + Terminal.Light_green + "+" + Terminal.White + f"]{Terminal.End}{Terminal.Light_white} "
        print(Terminal.deAuThY + d_hey + entire_color + msg)

    def prompt(question: str, allowed_replies: list[str], ending_color=End) -> str:
        d_huh = Terminal.White + f"{Terminal.Bold}[" + Terminal.Light_blue + "?" + Terminal.White + f"]{Terminal.End}{Terminal.Light_white} "
        try:
            reply = input(Terminal.deAuThY + d_huh + f"{Terminal.Light_white}{question}{Terminal.Bold}>{Terminal.End} {ending_color}")
            if reply.split()[0].lower() in CommandHandler.Debian.supported_commands_debian_based_distros:
                try:
                    if len(reply.split()) >= 2:
                        cmd = CommandHandler.stage_args(reply)
                        exitcode = check_call(args=cmd)
                        reply = Terminal.prompt(question, allowed_replies, ending_color)
                        return reply
                    else:
                        executable = CommandHandler.stage_args(reply)[0]
                        exitcode = check_call([executable])
                        reply = Terminal.prompt(question, allowed_replies, ending_color)
                except CalledProcessError:
                    reply = Terminal.prompt(question, allowed_replies, ending_color)
                    return reply
            elif reply in CommandHandler.own_commands:
                CommandHandler.Own_Cmds.handle_own_cmd[reply]()
                reply = Terminal.prompt(question, allowed_replies, ending_color)
                return reply
            elif reply.lower() in allowed_replies:
                return reply
            else:
                if allowed_replies[0].lower() == "any":
                    return reply
                if allowed_replies[0].lower() == "deauthy | sh" and reply.split()[0] not in CommandHandler.own_commands:

                    Terminal.tell_issue(msg=f"{Terminal.Red}That's not a valid {Terminal.Bold}{Terminal.White}DeAuthy command{Terminal.End}{Terminal.Red} :/")
                    reply = Terminal.prompt(question=question, allowed_replies=allowed_replies)
                    return reply
                else:
                    Terminal.tell_issue(msg=f"{Terminal.Red}That's not a valid {Terminal.Bold}{Terminal.Red}reply{Terminal.End}{Terminal.Red} :/")
                    reply = Terminal.prompt(question=question, allowed_replies=allowed_replies)
                    return reply
        except KeyboardInterrupt:
            quit(0)
        except IndexError:
            Terminal.tell_issue(f"{Terminal.Red}{Terminal.Bold}HEY!{Terminal.End}{Terminal.White} Come on! Fill something in!{Terminal.Red}{Terminal.Bold} >:({Terminal.End}")
            reply = Terminal.prompt(question=question, allowed_replies=allowed_replies)
            return reply