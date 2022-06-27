from colorama import Fore
from subprocess import check_call

prefix = f"!"

red         = Fore.RED
blue        = Fore.BLUE
white       = Fore.WHITE
bold        = '\033[1m'
yellow      = Fore.LIGHTYELLOW_EX
light_green = Fore.LIGHTGREEN_EX
light_white = Fore.LIGHTBLACK_EX
end         = '\033[0m'
light_blue  = Fore.LIGHTBLUE_EX
underline   = '\033[4m'
deAuThY = Fore.WHITE + "[" + Fore.RED + "D" + Fore.LIGHTYELLOW_EX + "E" + Fore.LIGHTGREEN_EX + "A" + Fore.MAGENTA + "U" + Fore.CYAN + "T" + Fore.BLUE + "H" + Fore.RED + "Y" + Fore.WHITE + "]"

def tell_issue(msg: str):
    d_wut = Fore.White + f"{bold}[" + red + "!" + white + f"]{end}{light_white} "
    print(deAuThY + d_wut + msg)

def inform(msg: str, entire_color=Fore.LIGHTBLACK_EX):
    d_hey = Fore.White + f"{Fore.Bold}[" + Fore.Light_green + "+" + Fore.White + f"]{Fore.End}{Fore.Light_white} "
    print(Fore.deAuThY + d_hey + entire_color + msg)

def prompt(question: str, allowed_replies: list[str], ending_color=Fore.WHITE) -> str:
    d_huh = Fore.WHITE + f"{Fore.Bold}[" + Fore.LIGHTBLUE_EX + "?" + Fore.WHITE + f"]{Fore.End}{Fore.Light_white} "
    reply = input(Fore.deAuThY + d_huh + f"{Fore.Light_white}{question}{Fore.Bold}>{Fore.End} {ending_color}")
    if reply.lower() in CommandHandler.supported_commands_debian_based_distros:
        print(Fore.End)
        check_call(reply)
        reply = Fore.prompt(question, allowed_replies, ending_color)
        return reply
    elif reply in CommandHandler.own_commands:
        CommandHandler.Own_Cmds.handle_own_cmd[reply]()
        reply = Fore.prompt(question, allowed_replies, ending_color)
        return reply
    elif reply.lower() in allowed_replies:
        return reply
    else:
        if allowed_replies[0].lower() == "any":
            return reply
        else:
            tell_issue(msg=f"{Fore.Red}That's not a valid {Fore.Bold}{Fore.Red}reply{Fore.End}{Fore.Red} :/")
            reply = prompt(question=question, allowed_replies=allowed_replies)
            return reply

class CommandHandler:
    """A class made to handle Deauthy's own commands as well as SOME linux commands."""
    supported_commands_debian_based_distros = [
        "ifconfig",
        "ls",
    ]
    own_commands = [
        f"{prefix}help",
        f"{prefix}about",
        f"{prefix}repo",
        f"{prefix}announcement",
        f"{prefix}remove",
    ]

    class Own_Cmds:
        def d_announcements():
            print(f"""{end}As of right now, saving configuration is not possible.
this due to me getting a better understanding of JSON. 
It's something I still have to take under the loop, but saving will be possible in the future.
You can keep an eye on the Testing branch, but I don't recommend cloning it, since it may contain code that renders the application useless.""")

        def d_help():
            print(f"""{white}{bold}[{end}DeAuthy commands{white}{bold}]{end} {white}Page {light_green}{bold}1{end}{white}/1
{light_white}- {light_green}help {light_white}-- {white}Views this message.
{light_white}- {light_green}disclaimer {light_white}-- {white}Displays a disclaiemr for DeAuthy.
{light_white}- {light_green}repo {light_white}-- {white}Displays the link to deauthy's Github repository.
{light_white}- {light_green}about {light_white}-- {white}Displays information about the project.
{light_white}- {light_green}announcements {light_white}-- {white}Displays important note(s) that are very recommended to read.
{light_white}- {light_green}remove {light_white}-- {white}Attempts to remove DeAuthy's dependencies that are not from the standard python library.""")

        def d_about():
            print(f"""{white}{bold}
DeAuthy{end} {white}version: {light_white}Private Repository Version
{white}
Note: {light_white}Version numbers are gonna be set once this project is released.
{white}{bold}
Author:{end} {light_green}Dr-Insanity {white}(On Github)""")

        def d_disclaimer():
            print(f"""{bold}{red}Disclaimer{end}{white}:{red}
I do not condone illegal activities.
I discourage non-ethical use of my application.
I only developed this program.
Anything that you do with this application is not done by 
me and therefore you're the only one responsible for any 
damage you cause.
By using this application, you fully understood and agreed 
with what I just said and you understand you're on your
own when you're charged or in a lawsuit, unless you got others rooting for you. 
It won't be me.{end}""")

        def d_repo():
            print(f"{white}{bold}DeAuthy{end} {white}repository: {light_green}https://github.com/Dr-Insanity/deauthy{end}")

        def d_remove():
            res = Fore.prompt(f"{Fore.WHITE}Are you very sure you want to do this? ({Fore.LIGHTGREEN_EX}Y{Fore.WHITE}/{Fore.RED}N{Fore.White})", ["y", "n"], ending_color=Fore.RED)
            if res.lower() == "y":
                from deauthy.auto_installer import Dependencies
                Dependencies.remove(Dependencies)
            if res.lower() == "n":
                print(f"{Fore.WHITE}Cancelled.")

        handle_own_cmd = {
            f"{prefix}help":d_help,
            f"{prefix}about":d_about,
            f"{prefix}repo":d_repo,
            f"{prefix}announcements":d_announcements,
            f"{prefix}disclaimer":d_disclaimer,
            f"{prefix}remove":d_remove,
        }