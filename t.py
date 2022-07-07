import pandas

df = pandas.read_csv('/home/netmin/Desktop/discovered_targets-01.csv', sep='\t')

print(df.to_dict())