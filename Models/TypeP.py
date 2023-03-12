from Etudiant import Etudiant
from ResponsableAdmin import ResponsableAdmin
from Chargé import Chargé
from Partenaire import Partenaire

class TypeP:
    def __init__(self, idN:int, libelle:str, etudiants:list = [], responsableAdmins: list = [], chargés:list = [], partenaires:list =  []) -> None:
        self.id = idN
        self.libelle = libelle
        self.etudiants = etudiants
        self.responsableAdmins = responsableAdmins
        self.chargés = chargés
        self.partenaires = partenaires
    
    #Setters
    def setId(self, newId:int) -> None:
        self.id = newId
    
    def setLibelle(self, newLibelle:str) -> None:
        self.libelle = newLibelle
        
    def setEtudiant(self, newEtudiant:Etudiant) -> None:
        self.etudiants.append(newEtudiant)
        
    def setResponsableAdmin(self, newResponsableAdmin:ResponsableAdmin) -> None:
        self.responsableAdmins.append(newResponsableAdmin)
        
    def setChargé(self, newChargé:Chargé) -> None:
        self.chargés.append(newChargé)
        
    def setPartenaire(self, newPartenaire:Partenaire) -> None:
        self.partenaires.append(newPartenaire)
        
    #Getters
    def getId(self) -> int:
        return self.id
    
    def getLibelle(self) -> str:
        return self.libelle
    
    def getEtudiant(self) -> list:
        return self.etudiants
        
    def getResponsableAdmin(self) -> list:
        return self.responsableAdmins
        
    def getChargé(self) -> list:
        return self.chargés
        
    def getPartenaire(self) -> list:
        return self.partenaires