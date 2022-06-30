from pyroute2 import IW
from pyroute2 import IPRoute
from pyroute2.netlink import NetlinkError
from sys import argv

class ESSID:
    """The ESSID of a wireless network.

    Parameters
    ----------
    Same as attributes

    Attributes
    ----------
    - `value` str - The name of the network.
    - `channel` int - The channel this One and ONLY AP is streaming on.
    """
    def __init__(self, name: str, channel: int):
        self._name = name
        self._channel = channel

    @property
    def channel(self):
        """The wireless network's channel"""
        channel = self._channel
        return channel

    @property
    def value(self):
        """The value for this ESSID"""
        name = self._name
        return name

class BSSID:
    """
    A (set of) BSSID(s) belonging to a wireless network

    Parameters
    ----------
    Same as attributes

    Attributes
    ----------
    - `bssids` dict - A set of BSSIDs and their channels, in a dict.
    - `essid` ESSID - The ESSID of a wireless network, can be None.
    """

    def __init__(self, bssids: dict[str, int], essid: ESSID=None):
        self._bssids = bssids
        self._essid = essid
    
    @property
    def bssids(self):
        """A set of BSSIDs and their channels, in a dict."""
        bssids_data = self._bssids
        return bssids_data

    @property
    def essid(self):
        """The ESSID of a wireless network, can be None"""
        essid = self._essid
        return essid

class Interface:
    """A wireless interface, better known as NIC (Network Interface Card)
    
    Parameters
    ----------
    same as Attributes

    Attributes
    ----------
    - `name` str - The name of this wireless interface (i.e. wlan0 or wlo0)
    """

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self):
        """The name of this wireless interface (i.e. wlan0 or wlo1)\n
        Returns
        -------
        - `str`
        """
        name = self._name
        return name

    def is_wireless(interface: str):
        """Determine whether given NIC is a wireless one or not.\n
        Returns
        -------
        - `True`[Bool] -The given NIC is a wireless NIC.
        - `False`[Bool] - The given NIC is NOT a wireless NIC.
        """
        ip = IPRoute()
        iw = IW()
        index = ip.link_lookup(ifname=interface)[0]
        try:
            iw.get_interface_by_ifindex(index)
            return True
        except NetlinkError as e:
            if e.code == 19:  # 19 'No such device'
                return False
        finally:
            iw.close()
            ip.close()