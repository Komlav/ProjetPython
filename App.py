l = "['dfsgdfgdf','kjkhjjj','jghjghjfhjfvh',13,13.5,17.5]"
lp = list()
m = l[1:-2].split(',')
print(m[0][1:-2])

t="cvbn"
def strToList(chaine:str):
    # type(chaine)
    ch=chaine[1:-1].split(",")
    # type(ch)
    ch.append(f"'{t}'")
    # print(ch)
    for i in ch:
        i[2:-2]
        print(i)
    
strToList(l)

def listTrans(liste: str = ...) -> list:
    return [float(i) if i.isdigit() or i.count('.') == 1 else i for i in liste[1:-2].replace("'",'').split(',')]

print(listTrans(l))

def testSaisie(message:str, catégorie: str = 'str', min: int = 0, max: int = 100, nbreChar: int = 3):
    push="\t"*4 
    
    while True:
        element = input(f"{push}{message}")
        print(f"{push}{'='*len(message + element)}")
        match catégorie:
            case 'int':
                ver = element.replace("-","")
                if ver.isdigit() and (int(element) >= min and int(element) <= max):
                    return int(element)
                else:
                    print("Ressaisissez")
            case 'str':
                if(len(element) >= nbreChar):
                    return element
                else:
                    print("ressaisissez")
testSaisie("Enter un entier","int",1,10)