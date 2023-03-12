from Etudiant import Etudiant

class Note:
    def __init__(self, libelle:str, etudiant:Etudiant) -> None:
        self.libelle = libelle
        self.etudiant = etudiant
    
    #Setters
    def setLibelle(self, newLibelle:str) -> None:
        self.libelle = newLibelle
        
    def setEtudiant(self, newEtudiant:Etudiant) -> None:
        self.etudiant = newEtudiant
    
    #Getters
    def getLibelle(self) -> str:
        return self.libelle
        
    def getEtudiant(self) -> Etudiant:
        return self.etudiant