l = "['dfsgdfgdf','kjkhjjj','jghjghjfhjfvh',13,13.5,17.5]"
# lp = list()
# m = l[1:-2].split(',')
# print(m[0][1:-2])

# t="cvbn"
# def strToList(chaine:str):
#     # type(chaine)
#     ch=chaine[1:-1].split(",")
#     # type(ch)
#     ch.append(f"'{t}'")
#     # print(ch)
#     for i in ch:
#         i[2:-2]
#         print(i)
    
# strToList(l)

def listTrans(liste: str = ...) -> list:
    return [float(i) if i.isdigit() or i.count('.') == 1 else i for i in liste[1:-2].replace("'",'').split(',')]

print(listTrans(l))