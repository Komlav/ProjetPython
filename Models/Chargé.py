from User import User
from Classe import Classe
from Controller import TAILLE_SCREEN

class Chargé(User):
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, classes:list = [], commentaires:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.classes = classes #les ids des classes
        self.commentaires = commentaires
        
    def makeCommentaire(self,matriculeEtu:int, newCommentaire:str, data:list):
        for etudiant in data:
            if etudiant.get("Matricule") == matriculeEtu:
                etudiant.get("Commentaires").append(newCommentaire)
                return True
        return False        
        
    #Fonctionnalités du chargé
    def setCommentaires(self, newCommentaire:dict):
        self.commentaires.append(newCommentaire)
        
    def listeCommentaire(self):
        print("="*TAILLE_SCREEN)
        print(f"{'IdClasse':<20}{'IdEtudiant':<20}{'Commentaire'}")
        print("="*TAILLE_SCREEN)
        for com in self.commentaires:
            print(f"{com.get('idClasse'):<20}{com.get('idEtu'):<20}{com.get('Commentaire')}")
            print('-'*TAILLE_SCREEN)
    
    #Setters
    def setClasse(self, newClasse:Classe) -> None:
        self.classes.append(newClasse)
        
    # Getters
    def getClasse(self) -> list:
        return self.classes
    
