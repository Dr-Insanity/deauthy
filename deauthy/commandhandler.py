import subprocess
import shutil
import time
import urllib.request
from colorama import Fore
import os
from subprocess import check_call, check_output, DEVNULL, STDOUT, run
from deauthy.auto_installer import DeAuthy
from deauthy.checks import Checks
from deauthy.deauthy_types import Interface
import requests, zipfile, io
from halo import Halo
import sys
import json
from socket import if_nameindex

prefix = f"!"

red         = Fore.RED
mag         = Fore.MAGENTA
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

class CommandHandler:
    """A class made to handle Deauthy's own commands as well as SOME linux commands."""

    def stage_args(entire_cmd: str):
        """Get an entire command, with or without arguments, as parts into a list, to make it work with subprocess\n\nParameters\n----------\n- `entire_cmd` [str] - An entire command, with/without args.\n\nReturns\n-------\n- `fragmented_cmd` [list[str]] - The command you gave in, just in parts in a LIST"""
        fragmented_cmd = entire_cmd.split()
        return fragmented_cmd

    class Debian:
        supported_commands = [
            "ifconfig",
            "lspci",
            "lsusb",
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
        f"{prefix}config",
    ]

    class Own_Cmds:
        def d_announcements():
            """Displays important note(s) that are very recommended to read."""
            print(f"""{end}As of right now, the core function is not working.""")

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
            from deauthy.terminal import Terminal
            res = Terminal.prompt(f"{white}Are you very sure you want to do this? ({light_green}Y{white}/{red}N{white})", ["y", "n"], ending_color=red)
            if res is None: return
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
            Terminal.inform(msg=f"{cyan}======================================{white}\nSometimes, when a wireless interface is brought into monitor mode, it gets 'mon' right after the interface name\nSo, for example:\n\nInterface in managed mode:\nwlx12345\n\nInterface in monitor mode:\nwlx12345mon\n\nIt's also possible there's simply a 1 added after the interface name\n{cyan}======================================")
            monsuffix = Terminal.prompt(question=f"What's added when your interface goes into monitor mode?{end}", allowed_replies=["any"])
            if monsuffix is None: return
            Checks.Chipset_Support_Check()
            Terminal.inform(msg=f"{white}Found a {light_green}{bold}supported {white}Chipset!{end}")
            mod_config('monitor_suffix', monsuffix)
            Terminal.inform(msg=f"{cyan}Choose a {bold}{cyan}wireless{end}{cyan} interface {white}({light_white}{bold}step {light_green}1{end}{light_white}/{white}3)")
            cardname = Functs.prompt_for_ifaces()
            if not Interface.is_wireless(cardname):
                Terminal.tell_issue(f"{red}{bold}HEY!{end}{white} That's {red}{bold}not{end}{white} a wireless interface!{red}{bold} >:({end}")
                return

            mod_config("interface", cardname)
            if not Functs.is_in_monitor_mode(Interface(cardname)):
                mon_or_not = Terminal.prompt(f"""{white}Do you want to put "{cardname}" into monitor mode now? {Terminal.y_n}""", ["y", "n"], light_green)
                if mon_or_not is None: return
                if mon_or_not.lower() == "y":
                    Functs.switch(Interface(cardname), "monitor")
                    return
                if mon_or_not.lower() == "n":
                    Terminal.inform(f"""{white}Leaving {cardname}'s mode unchanged.""")
                    return

        def d_interfacemode():
            """Set the mode for a wireless network interface card."""
            from deauthy.terminal import Terminal
            from deauthy.functs import Functs, get_var, mod_config
            if get_var('interface') is None:
                Terminal.tell_issue(f"{red}{bold}Nuh-uh!{end}{white}How about you first set a wireless interface card, hmm?{end}")
                return
            cardname = get_var('interface')
            Terminal.inform(msg=f"""{cyan}======================================{white}\nVarious ways are available to put a wireless interface into monitor mode.\nSome drivers have may have specified how it should be done for that driver. Personally, I know airmon-ng is a way. But it's {Terminal.Underline}possible{end+white} yours should be put into monitor mode by "iw" and "ip link"\n{cyan}======================================""")
            monmethod = Terminal.prompt(question=f"Please specify what the method for your card is{end} (IW / AIRMON)", allowed_replies=["iw", "airmon"])
            if monmethod is None: return
            mod_config('mon_method', {"iw":"iw", "airmon":"airmon"}[monmethod.lower()])
            mode = Terminal.prompt(f"""{white}Preferred mode for network interface "{cardname}"? ({light_white}managed{white}/{light_white}monitor{white})""", ["managed", "monitor"], yellow)
            if mode is None: return
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
            if target_mac_addr is None: return
            if Checks.is_valid_MAC(target_mac_addr):
                pass
            elif not Checks.is_valid_MAC(target_mac_addr):
                Terminal.tell_issue(f"{red}{bold}HEY!{end}{white} That's {red}{bold}not{end}{white} a valid MAC address!{red}{bold} >:({end}")
                return

            mod_config('target_mac', target_mac_addr)
            Terminal.inform(f"{white}Now we need to specify which network(s) are forbidden for our target to connect to{end}")
            method = Terminal.prompt(question="Use ESSID or BSSIDs (BSSID / ESSID)", allowed_replies=["bssid", "essid"])
            if method is None: return
            if method == "BSSID":
                bssids_list = {}
                try:
                    amt_of_bssids   = Terminal.prompt(question=f"How many BSSIDs?", allowed_replies=["any"])
                    if amt_of_bssids is None: return
                    numb_of_bssids  = int(amt_of_bssids)
                    bssids_added = 0
                    while bssids_added < numb_of_bssids:
                        bss     = Terminal.prompt(question=f"{white}Enter BSSID {light_green}{bold}{bssids_added+1}{end}{white}/{amt_of_bssids}", allowed_replies=["any"])
                        if bss is None: return
                        channel = Terminal.prompt(f"{white}It's channel", allowed_replies=["any"])
                        if channel is None: return
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
                if answ is None: return
                if answ.lower() == "y":
                    pass
                elif answ.lower() == "n":
                    Terminal.inform(f"""{white}Cancelling. Set up BSSID approach with the same command. Then choose BSSID.""")
                    return
                
                ess = Terminal.prompt(f"{white}Now, enter the ESSID of the target network", ["any"])
                if ess is None: return
                chn = Terminal.prompt(f"{white}It's channel?", ["any"])
                if chn is None: return
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

        def d_clientdiscover():
            """Discover client targets in your area."""
            from deauthy.terminal import Terminal
            from deauthy.functs import get_var, mod_config
            iface = get_var('interface')
            if iface is None or iface not in [ifc[1] for ifc in if_nameindex()]:
                Terminal.inform(f"{red}{bold}Tell me what interface I should be using with the '!interface' command")
                return
            print(f"{cyan}{bold}INTERFACE{white}: {end}{iface}")
            answ = Terminal.prompt(question=f"{white}We're going to do discovery for targets {underline}that can be seen within your interface's range{end}. {light_green}{bold}OK{end}{white}?", allowed_replies=["any"])
            if answ is None: return
            Terminal.inform(f"{yellow+bold}1{white+bold}.) {light_green+bold}lay back")
            Terminal.inform(f"{yellow+bold}2{white+bold}.) {light_blue+bold}take a breather")
            Terminal.inform(f"{yellow+bold}3{white+bold}.) {red+bold}take some coffee")
            Terminal.inform(f"{white}Press CTRL + C to stop doing discovery. It is recommended to wait at least 2 minutes so that you will have all the clients (devices) listed. Quitting too early can result in not having all the devices. So please lay back, take a breather, take some coffee, and let it run for at least 2 minutes.")
            with Halo(f"{light_blue+bold+underline}Monitoring networks nearby...") as spinner:
                try:
                    out = check_output(["airodump-ng", iface, "-w", "discovered_targets", "-o", "pcap"])
                except KeyboardInterrupt:
                    spinner.succeed(f"{light_green+bold+underline}CTRL + C pressed! Stopping monitoring.")

            out = run('tshark -Y wlan.fc.type_subtype==0x04 -e wlan.ssid -e wlan.ds.current_channel -e wlan.addr -T json -r discovered_targets-01.cap > discovered_targets.json', shell=True)
        def d_discover():
            """Discover target networks (Access Points) in your area."""
            from deauthy.terminal import Terminal
            from deauthy.functs import get_var, mod_config
            iface = get_var('interface')
            if iface is None or iface not in [ifc[1] for ifc in if_nameindex()]:
                Terminal.inform(f"{red}{bold}Tell me what interface I should be using with the '!interface' command")
                return
            print(f"{cyan}{bold}INTERFACE{white}: {end}{iface}")
            answ = Terminal.prompt(question=f"{white}We're going to do discovery for targets {underline}that can be seen within your interface's range{end}. {light_green}{bold}OK{end}{white}?", allowed_replies=["any"])
            if answ is None: return
            Terminal.inform(f"{yellow+bold}1{white+bold}.) {light_green+bold}lay back")
            Terminal.inform(f"{yellow+bold}2{white+bold}.) {light_blue+bold}take a breather")
            Terminal.inform(f"{yellow+bold}3{white+bold}.) {red+bold}take some coffee")
            Terminal.inform(f"{white}Press CTRL + C to stop doing discovery. It is recommended to wait at least 2 minutes so that you will have all the access points of a network. Quitting too early can result in the target device to be able to hop over to that one access point we don't know of. So please lay back, take a breather, take some coffee, and let it run for at least 2 minutes.")
            with Halo(f"{cyan+bold+underline}Monitoring networks nearby...") as spinner:
                try:
                    check_call(["airodump-ng", iface, "-w", "discovered_targets", "-o", "pcap"], stdout=DEVNULL, stderr=STDOUT)
                except KeyboardInterrupt:
                    spinner.succeed(f"{light_green+bold+underline}CTRL + C pressed! Stopping monitoring.")

            # ['tshark', '-Y', 'wlan.fc.type_subtype==0x08', '-e', 'wlan.ssid', '-e', 'wlan.ds.current_channel', '-e', 'wlan.addr', '-T', 'json', '-r', 'discovered_targets-01.cap', '>', 'discovered_targets.json'], stdout=DEVNULL, stderr=STDOUT)
            subprocess.check_output("tshark -Y wlan.fc.type_subtype==0x08 -e wlan.ssid -e wlan.ds.current_channel -e wlan.addr -T json -r discovered_targets-01.cap > discovered_targets.json", shell=True)
            for file in os.listdir():
                if file.startswith("discovered_targets") and file.endswith(".cap"):
                    os.remove(file)
            if not os.path.isfile("discovered_targets.json"):
                Terminal.inform(f"{Terminal.Red}Could not load up the discovered targets json file\n{white}Reason: {red}Not Found")
                return
            with open("discovered_targets.json", "r") as jsonfile:
                data: list[dict] = json.load(jsonfile)
                if len(data) == 0:
                    Terminal.tell_issue(f"{red+bold+underline}No networks were found. {white}Please wait a little longer.")
                    return
                jsonfile.close()
                pos = 1
                cursor = 1
                ssids: set[str] = set()
                bssids: dict[str, dict[str, str]] = {}
                for network in data:
                    try:
                        ssids.add(network["_source"]["layers"]["wlan.ssid"][0])
                        bssids[str(cursor)] = {network["_source"]["layers"]["wlan.ssid"][0]: network["_source"]["layers"]["wlan.addr"][1], "channel":network["_source"]["layers"]["wlan.ds.current_channel"][0]}
                        cursor += 1
                    except KeyError as e:
                        bssids[str(cursor)] = {network["_source"]["layers"]["wlan.ssid"][0]: network["_source"]["layers"]["wlan.addr"][1]}
                charlength = 0
                for ssid in ssids:
                    if ssid.count(ssid) > charlength:
                        charlength = ssid.count(ssid)
                print(f"{mag+bold}===========================[{yellow+bold}AVAILABLE NETWORKS{mag+bold}]==========================={end}")
                for network in data:
                    if len(network["_source"]["layers"]["wlan.ssid"][0]) > 0:
                        print(f"""{mag}[{yellow}{bold}{pos}{end}{mag}] {light_blue}{bold}{network["_source"]["layers"]["wlan.ssid"][0]} {white}{bold}| {end}{light_white}{network["_source"]["layers"]["wlan.addr"][1]}""")
                        pos += 1
                    elif len(network["_source"]["layers"]["wlan.ssid"][0]) == 0:
                        print(f"""{mag}[{yellow}{bold}{pos}{end}{mag}] {light_blue}{bold}<Hidden Network> {white}{bold}| {end}{light_white}{network["_source"]["layers"]["wlan.addr"][1]}""")
                        pos += 1
                print(f"{white+bold}Usage:{end}{light_white} Choose e.g. 1, 3, 5, 8, 16")
                for file in os.listdir():
                    if file == "discovered_targets.json": os.remove(file)
                def select_nets():
                    from deauthy.terminal import Terminal
                    selected_nets = Terminal.prompt(f"{cyan+bold+underline}Select access points to blacklist for {red}1 {cyan}client", ["any"], light_green)
                    if selected_nets is None: return
                    selected_nets = selected_nets.split(", ")
                    selected_bssids = {}
                    nets = f""
                    for selected_net in selected_nets:
                        try:
                            nets += f"""{light_blue+bold+list(bssids[selected_net].keys())[0]} {white+bold}({end+light_white+list(bssids[selected_net].values())[0]}{white+bold}){end}\n"""
                            selected_bssids[str(list(bssids[selected_net].values())[0])] = list(bssids[selected_net].values())[1]
                        except KeyError as e:
                            if e not in list(bssids.keys())[0]:
                                print(f"{red}{bold}Please just select like {light_white}1, 2, 3\n{red}{underline}Include spaces in your selections{end}")
                                select_nets()
                            elif e in list(bssids.keys())[0]:
                                selected_bssids[str(list(bssids[selected_net].values())[0])] = None
                    mod_config("target_BSSIDs", selected_bssids)
                    return nets
                selected_networks = select_nets()
                if isinstance(selected_networks, str):
                    print(f"{mag+bold}===========================[{yellow+bold}SELECTED NETWORKS{mag+bold}]==========================={end}\n{selected_networks}")

        def d_update():
            """Check for updates. Will also update if there's a newer version."""
            DeAuthy.update()

        def d_reinstall():
            """Reinstalls DeAuthy straight from the github repository."""
            DeAuthy.reinstall()

        def d_start():
            """Initiate the attack"""
            from deauthy.terminal import Terminal
            from deauthy.functs import Functs
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
                print(do_bssid)
                bssids = BSSID(do_bssid)
                Functs.BSSID_METHOD.deauth(bssids)

        def d_config():
            """View the current configuration (RAW JSON)"""
            from deauthy.terminal import Terminal
            f = open("deauthy/conf.json", "r")
            try:
                print(json.dumps(json.load(f), indent=2))
            except json.decoder.JSONDecodeError:
                Terminal.inform(f"{Terminal.Red}Config file got corrupted.\nResetting it...")
                with open("deauthy/conf.json", "w") as f:
                    f.truncate()
                    f.write("""{ "not_setup_yet":true }""")
                    f.close()
                os.execv(sys.executable, ['python'] + [sys.argv[0]])

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
            f"{prefix}config":d_config,
        }