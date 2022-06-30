from socket import if_nameindex
from deauthy.deauthy_types import Interface
from subprocess import DEVNULL, STDOUT, check_call, check_output, CalledProcessError
from halo import Halo

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

    def switch(card: Interface, mode: str):
        """
        Accepts either "monitor" or "managed"
        """
        from deauthy.terminal import Terminal
        end = Terminal.End
        def managed():
            with Halo(f"Putting {card.name} into {mode} mode...") as spinner:
                out = check_call(["airmon-ng", "stop", f"{card.name}mon"], stdout=DEVNULL, stderr=STDOUT)
                if out != 1:
                    spinner.succeed(f"{card.name} is now in {mode} mode")
                else:
                    spinner.fail(f"Could not put {card.name} in {mode} mode{end}")
        def monitor():
            with Halo(f"Putting {card.name} into {mode} mode...") as spinner:
                out = check_call(["airmon-ng", "start", f"{card.name}"], stdout=DEVNULL, stderr=STDOUT)
                if out != 1:
                    spinner.succeed(f"{card.name} is now in {mode} mode")
                else:
                    spinner.fail(f"Could not put {card.name} in {mode} mode{end}")
            
            
        modes = {
            "managed":managed,
            "monitor":monitor,
        }
        try:
            modes[mode]()
        except KeyError:
            raise RuntimeError("That's not a valid interface mode.")