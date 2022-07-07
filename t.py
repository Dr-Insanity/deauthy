import csv

def csv2blob(filename):
    li = []
    with open(filename,'r') as f:
        for line in f.readlines():
            n = line.strip('\r\n\r\n')
            li.append(n)

    print(li[2])

ai = csv2blob('/home/netmin/Desktop/discovered_targets-01.csv')