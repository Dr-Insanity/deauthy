import csv
import sys

def csv2blob(filename: str):
    li = [] # type: list[list[str]]
    with open(filename,'r') as f:
        for line in f.readlines():
            n = line.strip("\r\n\r\n\t ',.")
            if "time seen" in line:
                r = n.split(sep=',')
                li.append(r)
            else:
                r = n.split(sep=',')
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
    for line in li:
        if len(line) != 1:
            print(line)
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
    print('===================================[AVAILABLE DATA]===================================')
    if not index_names is None:
        for name in index_names:
            packed_data[name] = None
        print(f"==========================[MADE DATA MODEL DICT for ESSIDs!]==========================")

    [
        'BSSID', 
        ' First time seen', 
        ' Last time seen', 
        ' channel', 
        ' Speed', 
        ' Privacy', 
        ' Cipher', 
        ' Authentication', 
        ' Power', 
        ' # beacons', 
        ' # IV', 
        ' LAN IP', 
        ' ID-length', 
        ' ESSID', 
        ' Key'
    ]
    names = {}
    networks = 2
    for field in li:
        if ['Station MAC', ' First time seen', ' Last time seen', ' Power', ' # packets', ' BSSID', ' Probed ESSIDs'] == field:
            break
        try:
            if len(field) != 1 and ['BSSID', ' First time seen', ' Last time seen', ' channel', ' Speed', ' Privacy', ' Cipher', ' Authentication', ' Power', ' # beacons', ' # IV', ' LAN IP', ' ID-length', ' ESSID', ' Key'] != field:
                print(f"ESSIDs: {field[13]}\nLength of CSV line: {len(field)}\nLength of ESSID: {len(field[13])}\n")
                networks += 1
        except IndexError:
            pass
    #for field in li:
    #    f1 = field[1] # field containing names to index data for wireless networks
    #    if f1 == "BSSID":
    #        names["BSSID"] = {:}
    #data = {}
    #for field in li:
    #    f1 = field[1] # field containing names to index data for wireless networks
    #    if f1 == " ESSID":
    #        data["ESSID"] = {"":}

ai = csv2blob('discovered_targets-01.csv')