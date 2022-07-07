import pandas

df = pandas.read_csv('/home/netmin/Desktop/discovered_targets-01.csv', sep='\r')

print(df.to_dict())