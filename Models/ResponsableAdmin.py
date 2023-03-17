from User import User
from Classe import Classe
from Chargé import Chargé

class ResponsableAdmin(User):
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, classes:list = [], chargés:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.classes = classes
        self.chargés = chargés
        
    #Fonctionnalité de la responsable
    def ajouterComponent(self, libelle:str, componentData:list):
        for component in componentData:
            if component.get('Libelle') == libelle:
                return (len(componentData)+1, libelle)
        return False

    def ajouterProf(self, nom:str, prénom:str, mail:str, téléphone: int, modules:list, classes:list, data:list):
        for prof in data:
            if prof.get("Téléphone") == téléphone:
                return (f"PROF-{len(data)+1}", nom, prénom, mail, téléphone, modules, classes)
        return False
    
    def listerComponent(self):pass
    
    def listerProf(self):pass
    
    def listerChargés(self):pass
    
    def listerClasses(self):pass
    
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
        
    