import pandas as pd
import math
import csv

result = []
df = pd.read_csv('01.csv')
# print(df.dtypes)
for i in range(len(df)):
    v = df.iloc[i,1]
    h = df.iloc[i,3]
    # print(v , h)
    if v > h:
        result.append([df.iloc[i,0], df.iloc[i,2], 'V'])
    else:
        result.append([df.iloc[i,2], df.iloc[i,0], 'H'])

print(result)


with open('18-19Result.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['win', 'lose', 'probability'])
    writer.writerows(result)
    print('done.')