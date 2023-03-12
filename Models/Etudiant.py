from User import User
from Note import Note
from TypeP import TypeP
from Classe import Classe

class Etudiant(User):
    def __init__(self, matricule: str, nom: str, prénom: str, dateNaissance:str, nationnalité:str, mail: str, téléphone: int, login: str, password: str, typeP:str, classe:Classe, notes:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.dateNaissance = dateNaissance
        self.nationnalité = nationnalité
        self.notes = notes 
        self.classe = classe
        
    #Setters
    def setDateNaissance(self, newDateNaissance: str) -> None:
        self.dateNaissance = newDateNaissance
        
    def setNationnalité(self, newNationnalité: str) -> None:
        self.nationnalité = newNationnalité
        
    def setNote(self, newNote:Note) -> None:
        self.notes.append(newNote)
        
    def setClasse(self, newClasse:Classe) -> None:
        self.classe = newClasse
        
    #Getters
    def getDateNaissance(self) -> str:
        return self.dateNaissance
        
    def getNationnalité(self) -> str:
        return self.nationnalité
        
    def getNote(self) -> list:
        return self.notes

    def getClasse(self) -> Classe:
        return self.classe