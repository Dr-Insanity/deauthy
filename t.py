import json
import re

def is_valid_MAC(mac: str):
    """MAC address validator\n\nParameters\n----------\n- `str` - A MAC-address\n\nReturns\n-------\n- `True` - The given MAC address is valid\n- `False` - The given MAC address is invalid\n"""
    if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
        return True
    return False

def csv2json(filename: str):
    li = [] # type: list[list[str]]
    with open(filename,'r') as f:
        for line in f.readlines():
            if "Station MAC" in line:
                break
            n = line.strip("\r\n\r\n',.")
            if "time seen" in line:
                r = n.split(sep=',')
                li.append(r)
            else:
                r = n.split(sep=',')
                if not ' (not associated) ' in line:
                    if (len(r) != 1):
                        if is_valid_MAC(r[0]):
                            if len(r[13]) == 1:
                                _bssid = r[0].strip()
                                _first_time_seen = r[1].strip()
                                _last_time_seen = r[2].strip()
                                _channel = r[3].strip()
                                _speed = r[4].strip()
                                _privacy = r[5].strip()
                                _cipher = r[6].strip()
                                _authentication = r[7].strip()
                                _power = r[8].strip()
                                _beacons = r[9].strip()
                                _iv = r[10].strip()
                                _lan_ip = r[11].strip()
                                _id_length = r[12].strip()
                                _essid = r[13].strip()
                                _key = r[14].strip()
                                li.append([_bssid,_first_time_seen,_last_time_seen,_channel,_speed,_privacy,_cipher,_authentication,_power,_beacons,_iv,_lan_ip,_id_length,f" <Hidden Network>", _key])
                                continue
                li.append(r)

    # li[0] = station
    # li[1] = mac
    # li[2] = mac
    # li[3] = mac
    # li[4] = mac
    # li[5] = mac
    # li[6] = mac
    # li[7] = mac
    # li[8] = mac
    # li[9] = mac
    # li[10] = mac
    print('=======================[TARGETS]=======================')
    packed_data = {}
    index_names = None
    bssids = []
    total_networks_their_details = 0
    for line in li:
        if (len(line) != 1):
            if is_valid_MAC(line[0]):
                if ' (not associated) ' in line:
                    break
                _bssid = line[0].strip()
                _first_time_seen = line[1].strip()
                _last_time_seen = line[2].strip()
                _channel = line[3].strip()
                _speed = line[4].strip()
                _privacy = line[5].strip()
                _cipher = line[6].strip()
                _authentication = line[7].strip()
                _power = line[8].strip()
                _beacons = line[9].strip()
                _iv = line[10].strip()
                _lan_ip = line[11].strip()
                _id_length = line[12].strip()
                _essid = line[13].strip()
                _key = line[14].strip()
                total_networks_their_details += 1

        if ('BSSID' in line and
            ' First time seen' in line and
            ' Last time seen' in line and
            ' channel' in line and
            ' Speed' in line and
            ' Privacy' in line and
            ' Cipher' in line and
            ' Authentication' in line and
            ' Power' in line and
            ' # beacons' in line and
            ' # IV' in line and
            ' LAN IP' in line and
            ' ID-length' in line and
            ' ESSID' in line and
            ' Key' in line):
            index_names = line
            print(f"GOT INDEX NAMES. Creating Dict with these names as it's keys.")
    print(f"==============================[GOT {total_networks_their_details} BSSIDs]===================================")
    print('===================================[AVAILABLE DATA]===================================')

    if not index_names is None:
        for name in index_names:
            if name == 'BSSID':
                packed_data[name.lower()] = None
            elif name != 'BSSID':
                packed_data[name[1::].lower()] = None
        print(f"==========================[MADE DATA MODEL DICT for ESSIDs!]==========================")

    def get_specs(name: str):
        data = []
        for line in li:
            if (len(line) != 1): # If it's not the line we're looking for
                if is_valid_MAC(line[0].strip().lower()): # If it IS the line we ARE looking for
                    if not f" {name}" in line: # if it's not the specific network we asked for
                        continue
                    data.append([line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip(), line[4].strip(), line[5].strip(), line[6].strip(), line[7].strip(), line[8].strip(), line[9].strip(), line[10].strip(), line[11].strip(), line[12].strip(), line[13].strip(), line[14].strip()])
        cp_packed_data = packed_data.copy()
        try:
            cp_packed_data["bssid"] = data[0][0]
            cp_packed_data["first time seen"] = data[0][1]
            cp_packed_data["last time seen"] = data[0][2]
            cp_packed_data["channel"] = data[0][3]
            cp_packed_data["speed"] = data[0][4]
            cp_packed_data["privacy"] = data[0][5]
            cp_packed_data["cipher"] = data[0][6]
            cp_packed_data["authentication"] = data[0][7]
            cp_packed_data["power"] = data[0][8]
            cp_packed_data["beacons"] = data[0][9]
            cp_packed_data["iv"] = data[0][10]
            cp_packed_data["lan ip"] = data[0][11]
            cp_packed_data["id-length"] = data[0][12]
            cp_packed_data["essid"] = data[0][13]
            cp_packed_data["key"] = data[0][14]
            return cp_packed_data
        except IndexError:
            return cp_packed_data

    names = []
    same_names = 1
    for field in li:
        if ['Station MAC', ' First time seen', ' Last time seen', ' Power', ' # packets', ' BSSID', ' Probed ESSIDs'] == field:
            break

        if len(field) != 1 and [' Privacy', ' Cipher', ' Authentication', ' Power', ' # beacons', ' # IV', ' LAN IP', ' ID-length', ' ESSID', ' Key'] != field:
            # print(f"ESSID: {field[13][1::]}\nLength of CSV line: {len(field)}\nLength of ESSID: {len(field[13][1::])}\n")
            if is_valid_MAC(field[0].strip().lower()):
                print(field[13][1::])
                names.append(field[13][1::])

    nets = {} # type: dict[str, None]
    for name in names:
        nets[name] = None

    print(nets)

    numb_of_bssids = {} # type: dict[str, int]
    for key, value in nets.items():
        if len(key) == 0:
            print(f"# of APs for <Hidden Network>: {names.count(key)}")
            numb_of_bssids["<Hidden Network>"] = names.count(key)
        elif len(key) != 0:
            print(f"# of APs for {key}: {names.count(key)}")
            numb_of_bssids[key] = names.count(key)

    print(numb_of_bssids)

    def xxxx():
        __dicts = []
        cp_packed_data = packed_data.copy()
        for line in li:
            if (len(line) == 1): # If it's not the line we're looking for
                continue
            if is_valid_MAC(line[0].strip().lower()): # If it IS the line we ARE looking for
                cp_packed_data["bssid"] = line[0].strip()
                cp_packed_data["first time seen"] = line[1].strip()
                cp_packed_data["last time seen"] = line[2].strip()
                cp_packed_data["channel"] = line[3].strip()
                cp_packed_data["speed"] = line[4].strip()
                cp_packed_data["privacy"] = line[5].strip()
                cp_packed_data["cipher"] = line[6].strip()
                cp_packed_data["authentication"] = line[7].strip()
                cp_packed_data["power"] = line[8].strip()
                cp_packed_data["beacons"] = line[9].strip()
                cp_packed_data["iv"] = line[10].strip()
                cp_packed_data["lan ip"] = line[11].strip()
                cp_packed_data["id-length"] = line[12].strip()
                cp_packed_data["essid"] = line[13].strip()
                cp_packed_data["key"] = line[14].strip()
                __dicts.append(cp_packed_data)
        return __dicts

    __dicts = xxxx()

    numb_of_bssids_cp = {}
    numb_of_bssids_cp["AccessPoints"] = __dicts

    print(json.dumps(numb_of_bssids_cp, indent=2))

ai = csv2json('discovered_targets-01.csv')