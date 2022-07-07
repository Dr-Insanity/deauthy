import pandas

df = pandas.read_csv('/home/netmin/Desktop/discovered_targets-01.csv')

print(df.to_json(indent=2))