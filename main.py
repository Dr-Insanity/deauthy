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
target_mac     = f""

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

def main():
    Terminal.inform(msg=f"{bold}{light_green}Hey! {end}{light_white}Tip of the day: Parrot Security or Kali Linux is recommended! Although, real control freaks use ArchLinux")
    Terminal.inform(msg=f"""{white}Type {light_white}"{white}!help{light_white}"{white} for a list of commands!""")
    if Checks.has_root():
        Terminal.inform(msg=f"{white}Running as {light_green}{bold}Root{end}")
    Terminal.prompt(question=f"{white}deauthy | sh", allowed_replies=["deauthy | sh"], ending_color=yellow)


try:
    if not Checks.has_root():
        Terminal.tell_issue(msg=f"{bold}{red}Run it as root...{end}")
        exit(1)
    Appearance.printBanner()
    main()
except KeyboardInterrupt:
    quit(0)