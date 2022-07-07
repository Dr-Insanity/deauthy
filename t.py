import csv
import sys

def csv2blob(filename: str):
    li = [] # type: list[str]
    with open(filename,'r') as f:
        for line in f.readlines():
            n = line.strip('\r\n\r\n\t')
            li.append(list(n))

    print('=======================[TARGETS]=======================')
    for line in li:
        print(line)
    print('=======================[TARGETS]=======================')

ai = csv2blob('/home/netmin/Desktop/discovered_targets-01.csv')