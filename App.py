
from tabulate import tabulate
l=list()
for i in range(10):
    l.append((i,i))
print(tabulate(headers=["1","2"],tabular_data=l))