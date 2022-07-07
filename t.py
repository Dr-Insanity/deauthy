import csv

def csv2blob(filename):

    with open(filename,'r') as f:
        z = f.readlines()

    print(z)

ai = csv2blob('/home/netmin/Desktop/discovered_targets-01.csv')