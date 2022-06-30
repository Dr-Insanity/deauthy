from colorama import Fore
from subprocess import check_call
from deauthy.checks import Checks
from deauthy.deauthy_types import Interface
from deauthy.functs import Functs

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
cyan        = Fore.CYAN
deAuThY = Fore.WHITE + "[" + Fore.RED + "D" + Fore.LIGHTYELLOW_EX + "E" + Fore.LIGHTGREEN_EX + "A" + Fore.MAGENTA + "U" + Fore.CYAN + "T" + Fore.BLUE + "H" + Fore.RED + "Y" + Fore.WHITE + "]"

def tell_issue(msg: str):
    d_wut = white + f"{bold}[" + red + "!" + white + f"]{end}{light_white} "
    print(deAuThY + d_wut + msg)

def inform(msg: str, entire_color=white):
    d_hey = white + f"{bold}[" + light_green + "+" + white + f"]{end}{light_white} "
    print(deAuThY + d_hey + entire_color + msg)

def prompt(question: str, allowed_replies: list[str], ending_color=white) -> str:
    d_huh = white + f"{bold}[" + light_blue + "?" + white + f"]{end}{light_white} "
    reply = input(deAuThY + d_huh + f"{light_white}{question}{bold}>{end} {ending_color}")
    if reply.lower() in CommandHandler.supported_commands_debian_based_distros:
        print(end)
        check_call(reply)
        reply = prompt(question, allowed_replies, ending_color)
        return reply
    elif reply in CommandHandler.own_commands:
        CommandHandler.Own_Cmds.handle_own_cmd[reply]()
        reply = prompt(question, allowed_replies, ending_color)
        return reply
    elif reply.lower() in allowed_replies:
        return reply
    else:
        if allowed_replies[0].lower() == "any":
            return reply
        else:
            tell_issue(msg=f"{red}That's not a valid {bold}{red}reply{end}{red} :/")
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
        f"{prefix}interface",
        f"{prefix}interfacemode",
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
{light_white}- {light_green}remove {light_white}-- {white}Attempts to remove DeAuthy's dependencies that are not from the standard python library.
{light_white}- {light_green}interface {light_white}-- {white}Sets the wireless network interface for DeAuthy to use.
{light_white}- {light_green}interfacemode {light_white}-- {white}Set the mode for a wireless network interface card.""")
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
            res = prompt(f"{white}Are you very sure you want to do this? ({light_green}Y{white}/{red}N{white})", ["y", "n"], ending_color=red)
            if res.lower() == "y":
                from deauthy.auto_installer import Dependencies
                Dependencies.remove(Dependencies)
            if res.lower() == "n":
                print(f"{white}Cancelled.")
        
        def d_set_iface():
            from deauthy.terminal import Terminal
            Checks.Chipset_Support_Check()
            Terminal.inform(msg=f"{white}Found a {light_green}{bold}supported {white}Chipset!{end}")
            Terminal.inform(msg=f"{cyan}Choose a {bold}{cyan}wireless{end}{cyan} interface {white}({light_white}{bold}step {light_green}1{end}{light_white}/{white}3)")
            cardname = Functs.prompt_for_ifaces()
            if not Interface.is_wireless(cardname):
                Terminal.tell_issue(f"{red}{bold}HEY! {end}{white} That's {red}{bold}not{end}{white} a wireless interface!{red}{bold} >:({end}")
                return
            mon_or_not = Terminal.prompt(f"""{white}Do you want to put "{cardname}" into monitor mode now? ({light_green}Y{white}/{red}N{white})""", ["y", "n"], light_green)
            if mon_or_not.lower() == "y":
                Functs.switch(Interface(cardname), "monitor")
            if mon_or_not.lower() == "n":
                Terminal.inform(f"""{white}Leaving {cardname}'s mode unchanged.""")
            
            from main import current_wiface
            current_wiface.replace(current_wiface, cardname)

        def d_set_iface_mode():
            from deauthy.terminal import Terminal
            cardname = Functs.prompt_for_ifaces()
            if not Interface.is_wireless(cardname):
                Terminal.tell_issue(f"{red}{bold}HEY! {end}{white}That's {red}{bold}not{end}{white} a wireless interface!{red}{bold} >:({end}")
                return
            mode     = Terminal.prompt(f"""{white}Preferred mode for network interface "{cardname}"? ({light_white}managed{white}/{light_white}monitor{white})""", ["managed", "monitor"], yellow)
            Functs.switch(Interface(cardname), mode.lower())

        handle_own_cmd = {
            f"{prefix}help":d_help,
            f"{prefix}about":d_about,
            f"{prefix}repo":d_repo,
            f"{prefix}announcements":d_announcements,
            f"{prefix}disclaimer":d_disclaimer,
            f"{prefix}remove":d_remove,
            f"{prefix}interface":d_set_iface,
            f"{prefix}interfacemode":d_set_iface_mode,
        }