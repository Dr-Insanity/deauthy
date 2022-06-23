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
        self.name = name
        self.channel = channel

    @property
    def channel(self):
        """The wireless network's channel"""
        channel = self.channel
        return channel

    @property
    def value(self):
        """The value for this ESSID"""
        name = self.name
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
        self.bssids = bssids
        self.essid = essid
    
    @property
    def bssids(self) -> dict[str, int]:
        """A set of BSSIDs and their channels, in a dict."""
        bssids_data = self.bssids
        return bssids_data

    @property
    def essid(self) -> ESSID:
        """The ESSID of a wireless network, can be None"""
        essid = self.essid
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
        self.Name = name

    @property
    def name(self):
        """The name of this wireless interface (i.e. wlan0 or wlo0)"""
        name = self.Name
        return name