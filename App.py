
# from tabulate import tabulate
# l=list()
# for i in range(10):
#     l.append((i,i))
# print(tabulate(headers=["1","2"],tabular_data=l))

def convertion(liste)->dict:
    it=iter(liste)
    dicoo=dict(zip(it, it))
    return dicoo
liste=["eyu",[1,2],1,"GHJ"]
dico=convertion(liste)
dico["dfg"]=list()
dico["dfg"].append(1)
dico["dfg"].append(12)
listee=dico.items()
print(list(listee))