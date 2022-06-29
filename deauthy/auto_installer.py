from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError

class Dependencies:
    from deauthy.terminal import Terminal
    """
    DeAuthy's Dependencies class, full of code ensuring dependencies are all installed.
    The idea is give 0 errors: DeAuthy MUST run properly.
    """
    deps = ["pyroute2", "colorama", "halo"]

    def install(self):
        """Installs every non-standard lib dependency DeAuthy needs."""
        for dep in self.deps:
            out = check_output(f"pip install {dep} --upgrade --no-warn-conflicts --no-warn-script-location", shell=True)

    def installed(self):
        """Ensures the installation of DeAuthy's dependencies.\n
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
                self.install(self)
                return False
            except ImportError:
                self.Terminal.tell_issue(f"HEY! We're missing some dependencies here...")
                self.Terminal.inform(f"Attempting to install them!")
                self.install(self)
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
        self.Terminal.inform(msg=f"{self.Terminal.White}Uninstalling {len(self.deps)} packages")
        def pkgs():
            current_pkg = 1
            failed_pkgs = 0
            successful  = 0
            for dep in self.deps:
                with Halo(text=f"Uninstalling {dep} {self.Terminal.Light_green}{current_pkg}{self.Terminal.White}/{len(self.deps)}") as spinner:
                    try:
                        out = check_output(f"pip uninstall {dep} --yes", shell=True)
                        if "PermissionError: [Errno 13]" in out.decode():
                            spinner.fail(text=f"{self.Terminal.Red}{self.Terminal.Bold}Failed deinstallation of {self.Terminal.White}{dep}\n{self.Terminal.Bold}Error: {self.Terminal.Red}PermissionError: [Errno 13]{self.Terminal.End}...\n{self.Terminal.White}Skipping!")
                            failed_pkgs += 1
                        elif f"Successfully uninstalled {dep}" in out.decode():
                            spinner.succeed(text=f"{self.Terminal.Light_green}Successfully uninstalled {self.Terminal.White}{dep}{self.Terminal.End}")
                            current_pkg += 1
                            successful += 1
                        else:
                            spinner.fail(f"""{self.Terminal.Warning} {self.Terminal.White}Something went wrong whilst uninstalling "{dep}"\nI suggest you try to uninstall it manually: {self.Terminal.White}"{self.Terminal.Bold}{self.Terminal.Light_white}pip3 uninstall {dep}{self.Terminal.End}{self.Terminal.White}"{self.Terminal.End}""")
                            failed_pkgs += 1
                    except CalledProcessError as e:
                        e.returncode
            return {
                "success":successful, "failed":failed_pkgs, "total":len(self.deps)}
        results = pkgs()
        self.Terminal.inform(msg=f"""{self.Terminal.Light_green}{self.Terminal.Bold}{results["success"]}{self.Terminal.End}{self.Terminal.White} dependencies were {self.Terminal.Light_green}{self.Terminal.Bold}successfully {self.Terminal.White}removed!""", entire_color=self.Terminal.White)
        self.Terminal.inform(msg=f"""{self.Terminal.Red}{self.Terminal.Bold}{results["failed"]}{self.Terminal.End}{self.Terminal.White} dependencies failed to be removed""", entire_color=self.Terminal.White)
        self.Terminal.inform(msg=f"""{self.Terminal.White}{self.Terminal.Bold}{results["total"]}{self.Terminal.End}{self.Terminal.White} total dependencies were in use by DeAuthy""", entire_color=self.Terminal.White)
        self.Terminal.inform(msg=f"{self.Terminal.White}Exiting!{self.Terminal.End}")
        exit(0)
