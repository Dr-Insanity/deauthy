from deauthy.auto_installer import Dependencies
Dependencies.installed()
from socket import if_nameindex
from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
from sys import exit
from halo import Halo
from deauthy.deauthy_types import BSSID, ESSID, Interface
from deauthy.terminal import Terminal
from deauthy.checks import Checks
from deauthy.functs import Functs

def version():
    with open('deauthy/VERSION', 'r') as f:
        v = f.readline()
        f.close()
        return v

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

def clear():
    check_call(["clear"])

def printBanner():
    clear()
    print(red + """

██████╗ ███████╗     █████╗ ██╗   ██╗████████╗██╗  ██╗██╗   ██╗
██╔══██╗██╔════╝    ██╔══██╗██║   ██║╚══██╔══╝██║  ██║╚██╗ ██╔╝
██║  ██║█████╗█████╗███████║██║   ██║   ██║   ███████║ ╚████╔╝ 
██║  ██║██╔══╝╚════╝██╔══██║██║   ██║   ██║   ██╔══██║  ╚██╔╝  
██████╔╝███████╗    ██║  ██║╚██████╔╝   ██║   ██║  ██║   ██║   
╚═════╝ ╚══════╝    ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝   ╚═╝                             
        """ + light_green + "Time to kick off some assholes from yer net" + f"DeAuthy{end} {white}version: {light_white}{version()}")
    return True

def main():
    Terminal.inform(msg=f"{bold}{light_green}Hey! {end}{light_white}Tip of the day: Parrot Security or Kali Linux is recommended! Although, real control freaks use ArchLinux")
    Terminal.inform(msg=f"""{white}Type {light_white}"{white}!help{light_white}"{white} for a list of commands!""")
    if Checks.has_root():
        Terminal.inform(msg=f"{white}Running as {light_green}{bold}Root{end}")
    Terminal.prompt(question=f"{white}deauthy | sh", allowed_replies=["deauthy | sh"])

try:
    if not Checks.has_root():
        Terminal.tell_issue(msg=f"{bold}{red}Run it as root...{end}")
        exit(1)
    printBanner()
    main()
except KeyboardInterrupt:
    quit(0)