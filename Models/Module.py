from Classe import *
from Professeur import *

class Module:
    def __init__(self, idN:int, libelle:str, professeurs:list = [], classes:list = []) -> None:
        self.id = idN
        self.libelle = libelle
        self.classes = classes
        self.professeurs = professeurs
    
    #Setters
    def setId(self, newId:int) -> None:
        self.id = newId
    
    def setLibelle(self, newLibelle:str) -> None:
        self.libelle = newLibelle
        
    def setClasse(self, newClasse: Classe) -> None:
        self.classes.append(newClasse)
    
    def setProfesseur(self, newProfesseur: Professeur) -> None:
        self.professeurs.append(newProfesseur)
        
    #Getters
    def getId(self) -> int:
        return self.id
    
    def getLibelle(self) -> str:
        return self.libelle
    
    def getClasse(self) -> list:
        return self.classes

    def getProfesseurs(self) -> list:
        return self.professeurs