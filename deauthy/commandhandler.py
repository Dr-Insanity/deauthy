import shutil
import time
import urllib.request
from colorama import Fore
import os
from subprocess import check_call, check_output, DEVNULL, STDOUT
from deauthy.auto_installer import DeAuthy
from deauthy.checks import Checks
from deauthy.deauthy_types import Interface
from deauthy.functs import Functs
import requests, zipfile, io
from halo import Halo
import sys
import json
from socket import if_nameindex

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
    if reply.lower() in CommandHandler.Debian.supported_commands_debian_based_distros:
        print(end)
        args = CommandHandler.stage_args(reply)[1:]
        executable = CommandHandler.stage_args(reply)[0]
        exitcode = check_call(args=args, executable=executable)
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

    def stage_args(entire_cmd: str):
        """Get an entire command, with or without arguments, as parts into a list, to make it work with subprocess\n\nParameters\n----------\n- `entire_cmd` [str] - An entire command, with/without args.\n\nReturns\n-------\n- `fragmented_cmd` [list[str]] - The command you gave in, just in parts in a LIST"""
        fragmented_cmd = entire_cmd.split()
        return fragmented_cmd

    class Debian:
        supported_commands_debian_based_distros = [
            "ifconfig",
            "apt",
            "ls",
            "airmon-ng",
            "cat",
            "nano",
            "vim"
        ]


    own_commands = [
        f"{prefix}help",
        f"{prefix}reinstall",
        f"{prefix}disclaimer",
        f"{prefix}about",
        f"{prefix}repo",
        f"{prefix}announcements",
        f"{prefix}remove",
        f"{prefix}interface",
        f"{prefix}interfacemode",
        f"{prefix}settarget",
        f"{prefix}start",
        f"{prefix}discover",
        f"{prefix}update",
    ]

    class Own_Cmds:
        def d_announcements():
            """Displays important note(s) that are very recommended to read."""
            print(f"""{end}As of right now, saving configuration is not possible.
this due to me getting a better understanding of JSON. 
It's something I still have to take under the loop, but saving will be possible in the future.
You can keep an eye on the Testing branch, but I don't recommend cloning it, since it may contain code that renders the application useless.""")

        def d_help():
            """Views this message."""
            help_page = f"{white}{bold}[{end}DeAuthy commands{white}{bold}]{end} {white}Page {light_green}{bold}1{end}{white}/1"
            commands = [method for method in dir(CommandHandler.Own_Cmds) if method.startswith('__') is False]
            for func in commands:
                if func == f"handle_own_cmd":
                    continue
                a = getattr(CommandHandler.Own_Cmds, func)
                print(f"""{light_white}- {light_green}{func[2:]} {light_white}-- {white}{a.__doc__}""")

        def d_about():
            """Displays information about the project."""
            print(f"""{white}{bold}
DeAuthy{end} {white}version: {light_white}Private Repository Version
{white}
Note: {light_white}Version numbers are gonna be set once this project is released.
{white}{bold}
Author:{end} {light_green}Dr-Insanity {white}(On Github)""")

        def d_disclaimer():
            """Displays the disclaimer for DeAuthy."""
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
            """Displays the link to deauthy's Github repository."""
            print(f"{white}{bold}DeAuthy{end} {white}repository: {light_green}https://github.com/Dr-Insanity/deauthy{end}")

        def d_remove():
            """Attempts to remove DeAuthy's dependencies that are not from the standard python library."""
            res = prompt(f"{white}Are you very sure you want to do this? ({light_green}Y{white}/{red}N{white})", ["y", "n"], ending_color=red)
            if res.lower() == "y":
                from deauthy.auto_installer import Dependencies
                Dependencies.remove()
            if res.lower() == "n":
                print(f"{white}Cancelled.")
        
        def d_interface():
            """Sets the wireless network interface for DeAuthy to use."""
            from deauthy.terminal import Terminal
            from deauthy.checks import Checks
            from deauthy.functs import mod_config, Functs
            Checks.Chipset_Support_Check()
            Terminal.inform(msg=f"{cyan}======================================{white}\nSometimes, when a wireless interface is brought into monitor mode, it gets 'mon' right after the interface name\nSo, for example:\n\nInterface in managed mode:\nwlx12345\n\nInterface in monitor mode:\nwlx12345mon\n\nIt's also possible there's simply a 1 added after the interface name\n{cyan}======================================")
            Terminal.inform(msg=f"{white}Found a {light_green}{bold}supported {white}Chipset!{end}")
            monsuffix = Terminal.prompt(question=f"What's added when your interface goes into monitor mode?{end}", allowed_replies=["any"])
            mod_config('monitor_suffix', monsuffix)
            Terminal.inform(msg=f"{cyan}Choose a {bold}{cyan}wireless{end}{cyan} interface {white}({light_white}{bold}step {light_green}1{end}{light_white}/{white}3)")
            cardname = Functs.prompt_for_ifaces()
            if not Interface.is_wireless(cardname):
                Terminal.tell_issue(f"{red}{bold}HEY!{end}{white} That's {red}{bold}not{end}{white} a wireless interface!{red}{bold} >:({end}")
                return

            mod_config("interface", cardname)
            if not Functs.is_in_monitor_mode(Interface(cardname)):
                mon_or_not = Terminal.prompt(f"""{white}Do you want to put "{cardname}" into monitor mode now? {Terminal.y_n}""", ["y", "n"], light_green)
                if mon_or_not.lower() == "y":
                    Functs.switch(Interface(cardname), "monitor")
                    return
                if mon_or_not.lower() == "n":
                    Terminal.inform(f"""{white}Leaving {cardname}'s mode unchanged.""")
                    return

        def d_interfacemode():
            """Set the mode for a wireless network interface card."""
            from deauthy.terminal import Terminal
            from deauthy.functs import Functs, get_var
            if get_var('interface') is None:
                Terminal.tell_issue(f"{red}{bold}Nuh-uh!{end}{white}How about you first set a wireless interface card, hmm?{end}")
                return
            cardname = get_var('interface')
            mode = Terminal.prompt(f"""{white}Preferred mode for network interface "{cardname}"? ({light_white}managed{white}/{light_white}monitor{white})""", ["managed", "monitor"], yellow)
            state = Functs.is_in_monitor_mode(Interface(cardname))
            if state and mode.lower() == "monitor":
                Terminal.tell_issue(f"{white}Nuh-uh, can't do. That card is already in {mode} mode :/{end}")
                return
            if not state and mode.lower() == f"managed":
                Terminal.tell_issue(f"{white}Nuh-uh, can't do. That card is already in {mode} mode :/{end}")
                return
            Functs.switch(Interface(cardname), mode.lower())

        def d_settarget():
            """Set the target."""
            from deauthy.terminal import Terminal
            from deauthy.functs import Functs, mod_config, get_var
            from deauthy.checks import Checks
            from deauthy.deauthy_types import BSSID
            target_mac_addr = Terminal.prompt(question="Which client mac address are we going to send deauth packets to?", allowed_replies=["any"])
            if Checks.is_valid_MAC(target_mac_addr):
                pass
            elif not Checks.is_valid_MAC(target_mac_addr):
                Terminal.tell_issue(f"{red}{bold}HEY!{end}{white} That's {red}{bold}not{end}{white} a valid MAC address!{red}{bold} >:({end}")
                return

            mod_config('target_mac', target_mac_addr)
            Terminal.inform(f"{white}Now we need to specify which network(s) are forbidden for our target to connect to{end}")
            method = Terminal.prompt(question="Use ESSID or BSSIDs (BSSID / ESSID)", allowed_replies=["bssid", "essid"])
            if method == "BSSID":
                bssids_list = {}
                try:
                    amt_of_bssids   = Terminal.prompt(question=f"How many BSSIDs?", allowed_replies=["any"])
                    numb_of_bssids  = int(amt_of_bssids)
                    bssids_added = 0
                    while bssids_added < numb_of_bssids:
                        bss     = Terminal.prompt(question=f"{white}Enter BSSID {light_green}{bold}{bssids_added+1}{end}{white}/{amt_of_bssids}", allowed_replies=["any"])
                        channel = Terminal.prompt(f"{white}It's channel", allowed_replies=["any"])
                        bssids_added += 1
                        bssids_list[bss] = channel
                    with Halo(f"{white}{bold}Saving") as spinner:
                        mod_config('target_BSSIDs', bssids_list)
                        mod_config('use_bssids', True)
                        mod_config('use_essid', False)
                        mod_config('target_ESSID', None)
                    spinner.succeed(f"{white}Configuration was {light_green}{bold}saved {end}{white}to:\n{yellow}{bold}'deauthy/conf.json' {end}{light_white}(Current Working Directory){end}")
                    return
                except KeyboardInterrupt:
                    current_wiface = get_var('interface')
                    Functs.switch(Interface(current_wiface), "managed")
                    return
            elif method == "ESSID":
                Terminal.inform(f"{Terminal.Yellow}{Terminal.Bold}Use this approach only if you're 100% SURE if the {Terminal.End}{Terminal.Red}{Terminal.Bold}target network has ONLY 1 BSSID!!!{Terminal.End}")
                answ = Terminal.prompt(f"{Terminal.White}Are you {Terminal.Light_green}{Terminal.Bold}100% SURE{Terminal.End}{Terminal.White}? {Terminal.y_n}", ["y", "n"])
                if answ.lower() == "y":
                    pass
                elif answ.lower() == "n":
                    Terminal.inform(f"""{white}Cancelling. Set up BSSID approach with the same command. Then choose BSSID.""")
                    return
                
                ess = Terminal.prompt(f"{white}Now, enter the ESSID of the target network", ["any"])
                chn = Terminal.prompt(f"{white}It's channel?", ["any"])
                try:
                    int(ess)
                except ValueError:
                    Terminal.tell_issue(f"{red}{bold}That's not a number! >:(")

                with Halo(f"{white}{bold}Saving") as spinner:
                    mod_config('target_BSSIDs', None)
                    mod_config('use_bssids', False)
                    mod_config('use_essid', True)
                    mod_config('target_ESSID', {ess:int(chn)})
                
                spinner.succeed(f"{white}Configuration was {light_green}{bold}saved {end}{white}to:\n{yellow}{bold}'deauthy/conf.json' {end}{light_white}(Current Working Directory){end}")
                return

        def d_discover():
            """Discover targets in your area."""
            from deauthy.terminal import Terminal
            from deauthy.functs import get_var
            iface = get_var('interface')
            if iface is None or iface not in [ifc[1] for ifc in if_nameindex()]:
                Terminal.tell_issue(f"{red}{bold}You know what I'm thinking? What kind of retarded user is using me?")
                Terminal.inform(f"{red}{bold}Tell me what interface I should be using with the '!interface' command")
                Terminal.inform(f"{red}{bold}Also, put it into monitor mode, while you're at it.")
                return
            answ = Terminal.prompt(question=f"{white}We're going to do discovery for targets {underline}that can be seen within your interface's range{end}. {light_green}{bold}OK{end}{white}?", allowed_replies=["any"])
            Terminal.inform(f"{white}Press CTRL + C to stop doing discovery. It is recommended to wait at least 2 minutes so that you will have all the access points of a network. Quitting too early can result in the target device to be able to hop over to that one access point we don't know of. So please lay back, take a breather, take some coffee, and let it run for at least 2 minutes.")
            try:
                out = check_output(["airodump-ng", iface, "-w", "discovered_targets", "-o", "pcap"])
            except KeyboardInterrupt:
                Terminal.inform(f"{white}CTRL + C pressed! Stopping monitoring.")
            out = check_output(["tshark", "–r" "discovered_targets.pcap", "–T", "json", ">", "discovered_targets.json"])

        def d_update():
            """Check for updates. Will also update if there's a newer version."""
            DeAuthy.update()

        def d_reinstall():
            """Reinstalls DeAuthy straight from the github repository."""
            DeAuthy.reinstall()

        def d_start():
            """Initiate the attack"""
            from deauthy.terminal import Terminal
            from deauthy.deauthy_types import ESSID, BSSID
            from deauthy.functs import get_var
            iface = get_var('interface')
            if iface is None or iface not in [ifc[1] for ifc in if_nameindex()]:
                Terminal.tell_issue(f"{red}{bold}You know what I'm thinking? What kind of retarded user is using me?")
                Terminal.inform(f"{red}{bold}Tell me what interface I should be using with the '!interface' command")
                Terminal.inform(f"{red}{bold}Also, put it into monitor mode, while you're at it.")
                return
            do_bssid = get_var('target_BSSIDs')
            do_essid = get_var('target_ESSID')
            if do_bssid is None and do_essid is None:
                Terminal.tell_issue(f"{red}{bold}Wouldn't it be so much better if you actually set up targets?")
                Terminal.tell_issue(f"{red}{bold}So you know, that I actually know who to target, maybe?")
                return
            elif do_bssid is None and do_essid is not None:
                # do ESSID approach
                do_essid: dict[str, int]
                essiD, channeL = list(do_essid.items())[0]
                Functs.ESSID_METHOD.deauth(ESSID(essiD, channeL))
                return
 
            elif do_essid is None and do_bssid is not None:
                # do BSSID approach
                bssids = BSSID(do_bssid)
                Functs.BSSID_METHOD.deauth(bssids)

        def d_config():
            """View the current configuration (RAW JSON)"""
            with open("deauthy/conf.json", "r") as f:
                print(json.dumps(f.read(), indent=2))

        handle_own_cmd = {
            f"{prefix}help":d_help,
            f"{prefix}reinstall":d_reinstall,
            f"{prefix}disclaimer":d_disclaimer,
            f"{prefix}repo":d_repo,
            f"{prefix}about":d_about,
            f"{prefix}announcements":d_announcements,
            f"{prefix}remove":d_remove,
            f"{prefix}interface":d_interface,
            f"{prefix}interfacemode":d_interfacemode,
            f"{prefix}settarget":d_settarget,
            f"{prefix}start":d_start,
            f"{prefix}discover":d_discover,
            f"{prefix}update":d_update,
        }