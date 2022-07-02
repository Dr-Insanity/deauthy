from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
from sys import stdout

class Dependencies:
    """
    DeAuthy's Dependencies class, full of code ensuring dependencies are all installed.
    The idea is give 0 errors: DeAuthy MUST run properly.
    """
    deps = ["pyroute2", "colorama", "halo"]

    def install():
        """Installs every non-standard lib dependency DeAuthy needs."""
        for dep in Dependencies.deps:
            out = check_output(f"pip install {dep} --upgrade --no-warn-conflicts --no-warn-script-location", shell=True)

    def installed():
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
                Dependencies.install()
                return False
            except ImportError:
                from deauthy.terminal import Terminal
                Terminal.tell_issue(f"HEY! We're missing some dependencies here...")
                Terminal.inform(f"Attempting to install them!")
                Dependencies.install()
                return False

    def remove():
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
        from deauthy.terminal import Terminal
        Terminal.inform(msg=f"{Terminal.White}Uninstalling {len(Dependencies.deps)} packages")
        def pkgs():
            current_pkg = 1
            failed_pkgs = 0
            successful  = 0
            for dep in Dependencies.deps:
                with Halo(text=f"Uninstalling {dep} {Terminal.Light_green}{current_pkg}{Terminal.White}/{len(Dependencies.deps)}") as spinner:
                    try:
                        out = check_output(["python3", "-m", "pip", "uninstall", dep, "--yes"])
                        if "PermissionError: [Errno 13]" in out.decode():
                            spinner.fail(text=f"{Terminal.Red}{Terminal.Bold}Failed deinstallation of {Terminal.White}{dep}\n{Terminal.Bold}Error: {Terminal.Red}PermissionError: [Errno 13]{Terminal.End}...\n{Terminal.White}Skipping!")
                            failed_pkgs += 1
                        elif f"Successfully uninstalled {dep}" in out.decode():
                            spinner.succeed(text=f"{Terminal.Light_green}Successfully uninstalled {Terminal.White}{dep}{Terminal.End}")
                            current_pkg += 1
                            successful += 1
                        else:
                            spinner.fail(f"""{Terminal.Warning} {Terminal.White}Something went wrong whilst uninstalling "{dep}"\nI suggest you try to uninstall it manually: {Terminal.White}"{Terminal.Bold}{Terminal.Light_white}pip3 uninstall {dep}{Terminal.End}{Terminal.White}"{Terminal.End}""")
                            failed_pkgs += 1
                    except CalledProcessError as e:
                        e.returncode
            return {
                "success":successful, "failed":failed_pkgs, "total":len(Dependencies.deps)}
        results = pkgs()
        Terminal.inform(msg=f"""{Terminal.Light_green}{Terminal.Bold}{results["success"]}{Terminal.End}{Terminal.White} dependencies were {Terminal.Light_green}{Terminal.Bold}successfully {Terminal.White}removed!""", entire_color=Terminal.White)
        Terminal.inform(msg=f"""{Terminal.Red}{Terminal.Bold}{results["failed"]}{Terminal.End}{Terminal.White} dependencies failed to be removed""", entire_color=Terminal.White)
        Terminal.inform(msg=f"""{Terminal.White}{Terminal.Bold}{results["total"]}{Terminal.End}{Terminal.White} total dependencies were in use by DeAuthy""", entire_color=Terminal.White)
        Terminal.inform(msg=f"{Terminal.White}Exiting!{Terminal.End}")
        exit(0)
