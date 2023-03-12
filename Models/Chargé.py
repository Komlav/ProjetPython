from User import User
from Classe import Classe

class Chargé(User):
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, classes:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.classes = classes
        
    #Setters
    def setClasse(self, newClasse:Classe) -> None:
        self.classes.append(newClasse)
        
    # Getters
    def getClasse(self) -> list:
        return self.classes