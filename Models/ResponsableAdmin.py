from User import User
from Classe import Classe
from Chargé import Chargé

class ResponsableAdmin(User):
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, classes:list = [], chargés:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.classes = classes
        self.chargés = chargés
        
    # Setters
    def setClasse(self, newClasse: Classe) -> None:
        self.classes.append(newClasse)
        
    def setChargé(self, newChargé: Chargé) -> None:
        self.chargés.append(newChargé)
        
    # Getters     
    def getClasse(self) -> list:
        return self.classes
        
    def getChargé(self) -> list:
        return self.chargés
        
    