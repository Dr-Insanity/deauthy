import csv
import sys

def csv2blob(filename: str, pos: int):
    li = []
    with open(filename,'r') as f:
        for line in f.readlines():
            n = line.strip('\r\n\r\n')
            li.append(n)

    print(li[pos])

ai = csv2blob('/home/netmin/Desktop/discovered_targets-01.csv', sys.argv[1])