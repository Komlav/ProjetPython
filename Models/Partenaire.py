from User import User


class Partenaire(User):
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, fichierEtudiant:str) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.etudiants = fichierEtudiant
    
    # Setters
    def setEtudiant(self, newfichierEtudiant:str) -> None:
        self.etudiants = newfichierEtudiant
        
    # Getters
    def getEtudiants(self) -> str:
        return self.etudiants
        