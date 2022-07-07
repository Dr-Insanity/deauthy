import csv
import sys

def csv2blob(filename: str):
    li = [] # type: list[list[str]]
    with open(filename,'r') as f:
        for line in f.readlines():
            n = line.strip("\r\n\r\n',.")
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
    for line in li:
        print(line)
    print('=======================[TARGETS]=======================')

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
        try:
            print("ESSIDs: " + field[networks])
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

ai = csv2blob('/home/netmin/Desktop/discovered_targets-01.csv')