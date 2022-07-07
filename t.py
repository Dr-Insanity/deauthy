import csv

def csv2blob(filename):

    with open(filename,'r') as f:
        z = f.read()

    parts = z.split('\r\n\r\n')
    p_parts = [part for part in parts]
    print(p_parts)
    stations = parts[0]
    p_stats = [stat for stat in stations]
    print(p_stats)

ai = csv2blob('/home/netmin/Desktop/discovered_targets-01.csv')