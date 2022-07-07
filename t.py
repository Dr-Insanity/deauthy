import csv
import sys

def csv2blob(filename: str):
    li = []
    with open(filename,'r') as f:
        for line in f.readlines():
            n = line.strip('\r\n\r\n\t')
            li.append(n)

    lo = []
    for line in li:
        rr = f"""'{line}'"""
        lo.append(rr)

    print('=======================[TARGETS]=======================')
    print(lo[2::])
    print('=======================[TARGETS]=======================')

ai = csv2blob('/home/netmin/Desktop/discovered_targets-01.csv')