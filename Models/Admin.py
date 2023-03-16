from User import User

class Admin(User):
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, etudiants:list = [], chargés:list = [], responsableAdmin:list = [], partenaires:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.etudiants = etudiants
        self.chargés = chargés
        self.responsableAdmins = responsableAdmin
        self.partenaires = partenaires
        
    # Setters
    def setEtudiant(self, newEtudiant:dict) -> None:
        self.etudiants.append(newEtudiant)
        
    def setChargé(self, newChargé) -> None:
        self.chargés.append(newChargé)
        
    def setResponsableAdmin(self, newResponsableAdmin) -> None:
        self.responsableAdmins.append(newResponsableAdmin)
        
    def setPartenaire(self, newPartenaire) -> None:
        self.partenaires.append(newPartenaire)
        
    # Getters
    def getEtudiant(self) -> list:
        return self.etudiants
        
    def getChargé(self) -> list:
        return self.chargés
        
    def getResponsableAdmin(self) -> list:
        return self.responsableAdmins
        
    