from Classe import Classe

class Filiere:
    def __init__(self, idN:int, libelle:str, classes:list = []) -> None:
        self.id = idN
        self.libelle = libelle
        self.classes = classes
    
    #Setters
    def setId(self, newId:int) -> None:
        self.id = newId
    
    def setLibelle(self, newLibelle:str) -> None:
        self.libelle = newLibelle
    
    def setClasse(self, newClasse:Classe) -> None:
        self.classes.append(newClasse)
        
    #Getters
    def getId(self) -> int:
        return self.id
    
    def getLibelle(self) -> str:
        return self.libelle
    
    def getClasse(self) -> list:
        return self.classes
    