from deauthy.terminal import Terminal
from deauthy.auto_installer import Dependencies
from os import geteuid

class Checks:
    """
    Deauthy's check methods, containing numerous checks to make sure everything goes at it should
    """

    def __init__(self):
        Dependencies.installed()
    
    def has_root() -> bool:
        "Are we launched with root privileges?\n## returns\n- `True` - DeAuthy is ran as root.\n- `False` - Deauthy is NOT ran as root."
        return geteuid() == 0