from Controller import DefaultUseCases, TAILLE_SCREEN
from User import User

# from Note import Note
# from TypeP import TypeP
# from Classe import Classe

class Etudiant(User):
    def __init__(self, matricule: str, nom: str, prénom: str, dateNaissance:str, nationnalité:str, mail: str, téléphone: int, login: str, password: str, typeP:str, classe, notes:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.dateNaissance = dateNaissance
        self.nationnalité = nationnalité
        self.notes = notes 
        self.classe = classe #id de la classe
        self.commentaires = []
        
    #Fonctionnalités de l'étudiant
    def setCommentaire(self, newCommentaire):
        self.commentaires.append(newCommentaire)
        self.classe.getChargé().setCommentaires({"idClasse": self.classe, "idEtu":self.getMatricule(), "Commentaire":newCommentaire})
        
    def listeCommentaire(self):
        print("="*TAILLE_SCREEN)
        print("Commentaire")
        print("="*TAILLE_SCREEN)
        for commentaire in self.commentaires:
            print(commentaire)
            print('-'*TAILLE_SCREEN)
    
    
    #Setters
    def setDateNaissance(self, newDateNaissance: str) -> None:
        self.dateNaissance = newDateNaissance
        
    def setNationnalité(self, newNationnalité: str) -> None:
        self.nationnalité = newNationnalité
        
    def setNote(self, newNote) -> None:
        self.notes.append(newNote)
        
    def setClasse(self, newClasse) -> None:
        self.classe = newClasse
        
    #Getters
    def getDateNaissance(self) -> str:
        return self.dateNaissance
        
    def getNationnalité(self) -> str:
        return self.nationnalité
        
    def getNote(self) -> list:
        return self.notes

    def getClasse(self):
        return self.classe