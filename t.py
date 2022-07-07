import csv
import sys

def csv2blob(filename: str):
    li = [] # type: list[list[str]]
    with open(filename,'r') as f:
        for line in f.readlines():
            n = line.strip('\r\n\r\n')
            r = n.split()
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
        print(line[])
    print('=======================[TARGETS]=======================')

ai = csv2blob('/home/netmin/Desktop/discovered_targets-01.csv')