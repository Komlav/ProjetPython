# from Niveau import Niveau
# from Filiere import Filiere
# from Etudiant import Etudiant
# from Chargé import Chargé
# from Module import Module
# from Professeur import Professeur

class Classe:
    def __init__(self, idC:int, libelle:str, filière, niveau, effectif:int, chargéClasse, professeurs:list = [], étudiants:list = [], modules:list = []) -> None:
        self.idC = idC
        self.libelle = libelle
        self.filière = filière
        self.niveau = niveau
        self.effectif = effectif
        self.étudiants = étudiants
        self.modules = modules
        self.professeurs = professeurs
        self.chargé = chargéClasse
        
    #Setters
    def setId(self, newId) -> None:
        self.idC = newId
        
    def setLibelle(self, newlibelle) -> None:
        self.libelle = newlibelle
        
    def setNiveau(self, newNiveau) -> None:
        self.niveau = newNiveau
        
    def setEffectif(self, newEffectif) -> None:
        self.effectif = newEffectif
        
    def setModule(self, newModule) -> None:
        self.modules.append(newModule)
        
    def setProfesseur(self, newProfesseur) -> None:
        self.professeurs.append(newProfesseur)
        
    def setChargé(self, newChargé) -> None:
        self.chargé = newChargé
        
    def setEtudiant(self, newEtudiant) -> None:
        self.étudiants.append(newEtudiant)
        
    #Getters
    def getId(self) -> int:
        return self.idC
        
    def getLibelle(self) -> str:
        return self.libelle
        
    def getNiveau(self):
        return self.niveau
        
    def getEffectif(self) -> int:
        return self.effectif
        
    def getModule(self) -> list:
        return self.modules
        
    def getProfesseur(self) -> list:
        return self.professeurs
        
    def getChargé(self):
        return self.chargé 
    
    def getEtudiant(self) -> list:
        return self.étudiants