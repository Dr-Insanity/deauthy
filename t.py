import csv
import sys

def csv2blob(filename: str, pos: int):
    li = []
    with open(filename,'r') as f:
        for line in f.readlines():
            n = line.strip('\r\n\r\n\t')
            li.append(n)

    print(li[int(pos)])

    print('=======================[TARGETS]=======================')
    print(li[2::])

ai = csv2blob('/home/netmin/Desktop/discovered_targets-01.csv', sys.argv[1])