from os import geteuid
from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
import re

class Checks:
    """
    Deauthy's check methods, containing numerous checks to make sure everything goes at it should
    """

    def __init__(self):
        from deauthy.auto_installer import Dependencies
        Dependencies.installed()
    
    def has_root() -> bool:
        "Are we launched with root privileges?\n## returns\n- `True` - DeAuthy is ran as root.\n- `False` - Deauthy is NOT ran as root."
        return geteuid() == 0

    def Chipset_Support_Check():
        from deauthy.terminal import Terminal
        white = Terminal.White
        red = Terminal.Red
        bold = Terminal.Bold
        end = Terminal.End
        Terminal.inform(msg=f"Checking if any of your devices (Built-in & External) support MONITOR mode...")
        for chipset_name in ["AR92", "RT3070", "RT3572", "8187L", "RTL8812AU", "AR93", "82371AB"]:
            try:
                out = check_output(f"lspci | grep {chipset_name}", shell=True)
                out = check_output(f"lsusb | grep {chipset_name}", shell=True)
                if chipset_name in out.decode():
                    put = out.decode('utf8', 'strict')
                    return True
            except CalledProcessError as e:
                continue
        Terminal.tell_issue(msg=f"{red}{bold}I'm so sorry!")
        Terminal.tell_issue(msg=f"{red}{bold}It seems your chipset is NOT SUPPORTED :/")
        Terminal.tell_issue(msg=f"{red}{bold}If you are very certain your chipset supports monitor mode and packet injection")
        Terminal.tell_issue(msg=f"{red}{bold}Please contribute to the project here by making an issue")
        Terminal.tell_issue(msg=f"{red}{bold}Go to: {white}https://github.com/Dr-Insanity/deauthy/issues/new")
        Terminal.inform(msg=f"{red}{bold}Goodbye!\n{end}Exiting...")
        exit(1)

    def is_valid_MAC(mac: str):
        """MAC address validator\n\nParameters\n----------\n- `str` - A MAC-address\n\nReturns\n-------\n- `True` - The given MAC address is valid\n- `False` - The given MAC address is invalid\n"""
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
            return True
        return False