import csv

def csv2blob(filename):

    with open(filename,'r') as f:
        z = f.read()

    parts = z.split('\r\n\r\n')
    print(parts)
    stations = parts[0]
    print(stations)

    import sys
    if sys.version_info[0] < 3:
        from StringIO import StringIO
    else:
        from io import StringIO

    stations_str = StringIO(stations)

    r = csv.reader(stations_str)
    i = list(r)
    z = [k for k in i if k != []]

    stations_list = z

    r = csv.reader(clients_str)
    i = list(r)
    z = [k for k in i if k != []]

    clients_list = z
    
    return stations_list, clients_list

csv2blob('/home/netmin/Desktop/discovered_targets-01.csv')