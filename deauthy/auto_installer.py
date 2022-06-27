from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
from deauthy.terminal import Terminal

class Dependencies:
    """
    DeAuthy's Dependencies class, full of code ensuring dependencies are all installed.
    The idea is give 0 errors: DeAuthy MUST run properly.
    """
    deps = ["pyroute2", "colorama", "halo"]

    def install(self):
        """Installs every non-standard lib dependency DeAuthy needs."""
        for dep in self.deps:
            out = check_output(f"pip install {dep} --upgrade --user", shell=True)

    def installed(self):
        """Ensures the installation of DeAuthy's dependencies.

        Returns
        -------
        - `True` - All required dependencies are installed.
        - `False` - Some of the required dependencies were not installed/uninstalled. It was attempted to install all dependencies.
        """
        try:
            import colorama
            import halo
            import pyroute2
            return True
        except ImportError:
            try:
                from colorama import Fore
                White       = Fore.WHITE
                Light_white = Fore.LIGHTBLACK_EX
                Red         = Fore.RED
                Yellow      = Fore.LIGHTYELLOW_EX
                Light_green = Fore.LIGHTGREEN_EX
                Magenta     = Fore.MAGENTA
                Cyan        = Fore.CYAN
                Blue        = Fore.BLUE
                Light_blue  = Fore.LIGHTBLUE_EX
                Bold        = '\033[1m'
                Underline   = '\033[4m'
                End         = '\033[0m'
                deAuThY = White + "[" + Red + "D" + Yellow + "E" + Light_green + "A" + Magenta + "U" + Cyan + "T" + Blue + "H" + Red + "Y" + White + "]"
                d_wut = White + f"{Bold}[" + Red + "!" + White + f"]{End}{Light_white} "
                d_hey = White + f"{Bold}[" + Light_green + "+" + White + f"]{End}{Light_white} "
                print(f"{deAuThY}{d_wut} {Red}{Bold}HEY! {End} We're missing some dependencies here...")
                print(f"{deAuThY}{d_hey} {Light_green}{Bold}Attempting to install them!")
                self.install()
                return False
            except ImportError:
                Terminal.tell_issue(f"HEY! We're missing some dependencies here...")
                Terminal.inform(f"Attempting to install them!")
                self.install()
                return False

    def remove(self):
        """A class method for removing all DeAuthy's dependencies, if that is really wanted. 
        These dependencies may also be used by other python applications. 
        Deinstallation of DeAuthy's dependencies may result in 
        those applications not working as intended.

        Returns
        -------
        - ``True`` - Deinstallation of DeAuthy's dependencies was successful.
        - ``False`` - Failed to uninstall DeAuthy's dependencies.
        """
        from halo import Halo
        current_pkg = 1
        for dep in self.deps:
            Terminal.inform(self=Terminal, msg=f"{Terminal.White}Uninstalling {len(self.deps)} packages")
            with Halo(text=f"Uninstalling {dep} {Terminal.Light_green}{current_pkg}{Terminal.White}/{len(self.deps)}") as spinner:
                out = check_output(f"pip uninstall {dep}", shell=True)
                spinner.succeed(text=f"{Terminal.Light_green}Successfully uninstalled {Terminal.White}{dep}{Terminal.End}")
        Terminal.inform(self=Terminal, msg=f"All dependencies were removed!")
        Terminal.inform(self=Terminal, msg=f"Exiting!")
        exit(0)
