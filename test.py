import json
from colorama import Fore
from subprocess import check_call

red         = Fore.RED
mag         = Fore.MAGENTA
blue        = Fore.BLUE
white       = Fore.WHITE
bold        = '\033[1m'
yellow      = Fore.LIGHTYELLOW_EX
light_green = Fore.LIGHTGREEN_EX
light_white = Fore.LIGHTBLACK_EX
end         = '\033[0m'
light_blue  = Fore.LIGHTBLUE_EX
underline   = '\033[4m'
cyan        = Fore.CYAN
deAuThY = Fore.WHITE + "[" + Fore.RED + "D" + Fore.LIGHTYELLOW_EX + "E" + Fore.LIGHTGREEN_EX + "A" + Fore.MAGENTA + "U" + Fore.CYAN + "T" + Fore.BLUE + "H" + Fore.RED + "Y" + Fore.WHITE + "]"

def mod_config(key: str, value):
    with open("deauthy/conf.json", "r") as jsonfile:
        data = json.load(jsonfile)
        jsonfile.close()
        
    data[key] = value
    with open("deauthy/conf.json", "w+") as jsonfile:
        myJSON = json.dump(data, jsonfile, indent=2)
        jsonfile.close()

with open("C:/Users/cicho/Downloads/discovered_targets.json", "r") as jsonfile:
    data: list[dict] = json.load(jsonfile)
    jsonfile.close()
    numb = 1
    pos = 1
    cursor = 1
    longest_ssid = None
    ssids: set[str] = set()
    bssids: dict[str, dict[str, str]] = {}
    print(f"{mag+bold}===========================[{yellow+bold}AVAILABLE NETWORKS{mag+bold}]==========================={end}")
    for network in data:
        ssids.add(network["_source"]["layers"]["wlan.ssid"][0])
        bssids[str(cursor)] = {network["_source"]["layers"]["wlan.ssid"][0]: network["_source"]["layers"]["wlan.addr"][1]}
        cursor += 1
    
    charlength = 0
    for ssid in ssids:
        if ssid.count(ssid) > charlength:
            charlength = ssid.count(ssid)
    
    for network in data:
        print(f"""{mag}[{yellow}{bold}{pos}{end}{mag}] {light_blue}{bold}{network["_source"]["layers"]["wlan.ssid"][0]} {white}{bold}| {end}{light_white}{network["_source"]["layers"]["wlan.addr"][1]}""")
        pos += 1

    print(f"{white+bold}Usage:{end}{light_white} Choose e.g. 1, 3, 5, 8, 16")
    def select_nets():
        selected_nets = prompt(f"{cyan+bold+underline}Select access points to blacklist for {red}1 {cyan}client", ["any"], light_green)
        selected_nets = selected_nets.split(", ")
        selected_bssids: list[str] = []
        nets = f""
        for selected_net in selected_nets:
            try:
                nets += f"""{light_blue+bold+list(bssids[selected_net].keys())[0]} {white+bold}({end+light_white+list(bssids[selected_net].values())[0]}{white+bold}){end}\n"""
                selected_bssids.append(list(bssids[selected_net].values())[0])
            except KeyError:
                print(f"{red}{bold}Please just select like {light_white}1, 2, 3\n{red}{underline}Include spaces in your selections{end}")
                select_nets()
        mod_config("target_BSSIDs", selected_bssids)
        return nets
    selected_networks = select_nets()
    if isinstance(selected_networks, str):
        print(f"{mag+bold}===========================[{yellow+bold}SELECTED NETWORKS{mag+bold}]==========================={end}\n{selected_networks}")