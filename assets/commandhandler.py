from main import white, bold, end, light_green, light_white, red
prefix = f"!"
class CommandHandler:
    """A class made to handle Deauthy's own commands as well as SOME linux commands."""
    supported_commands_debian_based_distros = [
        "ifconfig",
        "ls",
    ]
    own_commands = [
        f"{prefix}help",
        f"{prefix}about",
        f"{prefix}repo",
        f"{prefix}announcement",
    ]

    class Own_Cmds:
        def d_announcements():
            print(f"""{end}As of right now, saving configuration is not possible.
this due to me getting a better understanding of JSON. 
It's something I still have to take under the loop, but saving will be possible in the future.
You can keep an eye on the Testing branch, but I don't recommend cloning it, since it may contain code that renders the application useless.""")

        def d_help():
            print(f"""{white}{bold}[{end}DeAuthy commands{white}{bold}]{end} {white}Page {light_green}{bold}1{end}{white}/1
{light_white}- {light_green}help {light_white}-- {white}Views this message.
{light_white}- {light_green}disclaimer {light_white}-- {white}Displays a disclaiemr for DeAuthy.
{light_white}- {light_green}repo {light_white}-- {white}Displays the link to deauthy's Github repository.
{light_white}- {light_green}about {light_white}-- {white}Displays information about the project.
{light_white}- {light_green}announcements {light_white}-- {white}Displays important note(s) that are very recommended to read.""")

        def d_about():
            print(f"""{white}{bold}
DeAuthy{end} {white}version: {light_white}Private Repository Version
{white}
Note: {light_white}Version numbers are gonna be set once this project is released.
{white}{bold}
Author:{end} {light_green}Dr-Insanity {white}(On Github)""")

        def d_disclaimer():
            print(f"""{bold}{red}Disclaimer{end}{white}:{red}
I do not condone illegal activities.
I discourage non-ethical use of my application.
I only developed this program.
Anything that you do with this application is not done by 
me and therefore you're the only one responsible for any 
damage you cause.
By using this application, you fully understood and agreed 
with what I just said and you understand you're on your
own when you're charged or in a lawsuit, unless you got others rooting for you. 
It won't be me.{end}""")

        def d_repo():
            print(f"{white}{bold}DeAuthy{end} {white}repository: {light_green}https://github.com/Dr-Insanity/deauthy{end}")

        handle_own_cmd = {
            f"{prefix}help":d_help,
            f"{prefix}about":d_about,
            f"{prefix}repo":d_repo,
            f"{prefix}announcements":d_announcements,
            f"{prefix}disclaimer":d_disclaimer,
        }