from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
import requests, zipfile, shutil, io, os, sys, time

class Dependencies:
    """
    DeAuthy's Dependencies class, full of code ensuring dependencies are all installed.
    The idea is give 0 errors: DeAuthy MUST run properly.
    """
    deps = ["pyroute2", "colorama", "halo", "pyperclip"]

    def install():
        """Installs every non-standard lib dependency DeAuthy needs."""
        print(f"Installing/updating {len(Dependencies.deps)} packages")
        def pkgs():
            current_pkg = 1
            failed_pkgs = 0
            successful  = 0
            for dep in Dependencies.deps:
                print(f"Installing {dep} {current_pkg}/{len(Dependencies.deps)}")
                try:
                    out = check_output(["python3", "-m", "pip", "install", dep, "--upgrade", "--no-warn-conflicts", "--no-warn-script-location"])
                    if "PermissionError: [Errno 13]" in out.decode():
                        print(f"Failed installation of {dep}\nError: PermissionError: [Errno 13]...\nSkipping!")
                        failed_pkgs += 1
                    elif f"Successfully installed {dep}" in out.decode():
                        print(f"Successfully installed {dep}")
                        current_pkg += 1
                        successful += 1
                    elif f"Requirement already satisfied: {dep}" in out.decode():
                        print(f"Was already installed {dep}")
                        current_pkg += 1
                        successful += 1
                    else:
                        print(f"""Something went wrong whilst installing "{dep}"\nI suggest you try to install it manually: "pip3 install {dep}" """)
                        failed_pkgs += 1
                except CalledProcessError as e:
                    e.returncode
            return {
                "success":successful, "failed":failed_pkgs, "total":len(Dependencies.deps)}
        results = pkgs()
        print(f"""{results["success"]} dependencies were successfully installed!""")
        print(f"""{results["failed"]} dependencies failed to be installed""")
        input("Press enter / enter something")
        if results["failed"] > 0:
            print(f"Some package failed to install. As a result, DeAuthy is lacking required dependencies.")
            print(f"You should try to install the following dependencies by yourself:\n--> colorama\n--> pyroute2\n--> halo\nQUITTING!")
            quit(1)

    def installed():
        """Ensures the installation of DeAuthy's dependencies.\n
        Returns
        -------
        - `True` - All required dependencies are installed.
        - `False` - Some of the required dependencies were not installed/uninstalled. It was attempted to install all dependencies.
        """
        print(f"Enforcing the installation of all required dependencies...")
        for dep in Dependencies.deps:
            try:
                check_output(["python3", "-m", "pip", "show", dep])
            except CalledProcessError:
                print(f"[deauthy][!] HEY! We're missing the {dep} library")
                print(f"[deauthy][+] Attempting to install it...")
                Dependencies.install()
                return False
        return True

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

class DeAuthy():
    """Class representing the application itself. Contains code for managing it's installation/configuration."""

    def reinstall():
        """Reinstalls DeAuthy from the github repository (Force update, without version check)

        Returns
        -------
        - `True` - Reinstallation succeeded.
        - `False` - Reinstallation failed.
        """
        from deauthy.terminal import Terminal
        from halo import Halo
        keep_config = False
        answ = Terminal.prompt(question=f"Keep config file? {Terminal.Light_green}Y{Terminal.White}/{Terminal.Red}N{Terminal.White})", allowed_replies=["y", "n"])
        if answ.lower() == "y":
            keep_config = True
        if answ.lower() == "n":
            pass
        with Halo('Reinstalling...') as spinner:
            response = requests.get("https://github.com/Dr-Insanity/deauthy/archive/refs/heads/Testing.zip")
            with zipfile.ZipFile(io.BytesIO(response.content)) as update_zip:
                update_zip.extractall()
            for file in os.listdir(f"deauthy-Testing"):
                if file in [".git", ".vscode", ".gitignore", "t.py"]:
                    continue
                if os.path.isdir(f"deauthy-Testing/{file}"):
                    shutil.rmtree(file)
                    shutil.move(f"deauthy-Testing/{file}", "./")
                if os.path.isfile(f"deauthy-Testing/{file}"):
                    if file in ["conf.json"] and str(keep_config) == "True":
                        spinner.stop_and_persist()
                        print("We need to keep config!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        continue
                    else:
                        os.remove(file)
                        shutil.move(f"deauthy-Testing/{file}", "./")
                if file in ["conf.json"]:
                    if not keep_config:
                        Terminal.tell_issue("Config file is reset.")
                    else:
                        Terminal.tell_issue("Config file is kept as-is.")
                        continue
            time.sleep(5)
            shutil.rmtree(f"deauthy-Testing/")
        if not keep_config:
            Terminal.inform(f"{Terminal.Red}Config file is reset.")
        else:
            Terminal.inform(f"{Terminal.Light_green}Config file is kept as-is.")
        spinner.succeed(f"{Terminal.Light_green} Success! Restarting...")
        time.sleep(5) # give the time to the user to read that we're restarting
        os.execv(sys.executable, ['python'] + [sys.argv[0]])

    def update():
        """Updates DeAuthy straight from the github repository

        Returns
        -------
        - `True` - Update succeeded.
        - `False` - Update failed.
        """
        from deauthy.terminal import Terminal
        from halo import Halo
        with Halo('Checking for updates...') as updatechecker_spinner:
            response = requests.get("https://raw.githubusercontent.com/Dr-Insanity/deauthy/Testing/deauthy/VERSION")
            version = open('deauthy/VERSION', 'r').readline()
            if response.content.decode() == version:
                updatechecker_spinner.fail(f"There are no updates available right now.")
                return
            updatechecker_spinner.succeed(f"Update Available! How nice!")
        with Halo('Updating...') as spinner:
            response = requests.get("https://github.com/Dr-Insanity/deauthy/archive/refs/heads/Testing.zip")
            with zipfile.ZipFile(io.BytesIO(response.content)) as update_zip:
                update_zip.extractall()
            for file in os.listdir(f"deauthy-Testing"):
                if file in [".git", ".vscode", ".gitignore", "t.py", "conf.json"]:
                    continue
                if os.path.isdir(f"deauthy-Testing/{file}"):
                    shutil.rmtree(file)
                    shutil.move(f"deauthy-Testing/{file}", "./")
                if os.path.isfile(f"deauthy-Testing/{file}"):
                    if file == "conf.json":
                        continue
                    os.remove(file)
                    shutil.move(f"deauthy-Testing/{file}", "./")
            time.sleep(5)
            shutil.rmtree(f"deauthy-Testing/")
        spinner.succeed(f"{Terminal.Light_green} Success! Restarting...")
        time.sleep(2) # give the time to the user to read that we're restarting
        os.execv(sys.executable, ['python'] + [sys.argv[0]])
