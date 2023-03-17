from Admin import Admin
# from DataBase.sql import MySql


DEFAULT_PASSWORD = "passer@123"
TAILLE_SCREEN = 100

class DefaultUseCases:
    def __init__(self) -> None:
        self.all_User_Data = {} #Données des utilisateurs.
        self.all_Other_Data = {} #Données des filières et autres infos
        

    def connect(self, login:str, password:str)-> dict:
        for liste_user in self.all_User_Data.values():
            for user in liste_user:
                if (login == user.get("Login") and password == user.get("Password")):
                    return user
        return {}
    
    def ligne(self, motif:str = "-", nombre:int = TAILLE_SCREEN):
        print(motif*nombre)
        pass
    
    def showComponents(self, attributs:list, data:list):
        self.ligne("=")
        for attribut in attributs: print(f"{attribut}", end=" ")
        self.ligne("=")
        
        for user in data:
            for i in range(len(attributs)): print(f"{user.get(attributs[i])}", end=" ")
            self.ligne()
            
class AdminUseCases(Admin):
    #Use case d'ajout
    # - Etudiant
    # - Chargé
    # - Responsable Adminstratif
    # - Partenaires
    
    def __init__(self, admin_data:dict) -> None:
        super().__init__(admin_data.get("Matricule"),admin_data.get("Nom"),admin_data.get("Prénom"),admin_data.get("Mail"),admin_data.get("Téléphone"),admin_data.get("Login"),admin_data.get("Password"),admin_data.get("TypeP"),admin_data.get("Etudiants"),admin_data.get("Chargés"),admin_data.get("ResponsableAdmin"), admin_data.get("Partenaires")) # type: ignore
        self.all_etudiants = self.getEtudiant()
        self.all_chargés = self.getChargé()
        self.all_responsables = self.getResponsableAdmin()
        self.all_partenaires = self.getPartenaire()
        
    def setUserMail(self, user:dict, domaine:str = "ism.edu",):
        return  f"{user.get('Prénom').replace(' ', '-').lower()}.{user.get('Nom').lower()}@{domaine}.sn" # type: ignore
        
    def user(self, newEtu:dict):
        self.setEtudiant(newEtu)
        self.mail = self.setUserMail(newEtu)
        return (
            newEtu.get("Matricule"),
            newEtu.get("Nom"),
            newEtu.get("Prénom"),
            newEtu.get("DateNaissance"),
            newEtu.get("Nationnalité"),
            self.mail, #Mail etudiant
            newEtu.get("Telephone"),
            self.mail, #Login etudiant
            DEFAULT_PASSWORD,
            "Etudiant",
            newEtu.get("Classes"),
            newEtu.get("Notes")
        )
        
    def addNewChargé(self, newChargé:dict):
        self.setChargé(newChargé)
        self.mail = self.setUserMail(newChargé, "groupeism")
        return (
            newChargé.get("Matricule"),
            newChargé.get("Nom"),
            newChargé.get("Prénom"),
            self.mail, #Mail chargé
            newChargé.get("Telephone"),
            self.mail, #Login chargé
            DEFAULT_PASSWORD,
            "Chargé",
            newChargé.get("Classe")
            )
        
    def addNewResponsableAdmin(self, newResponsableAdmin:dict):
        self.setResponsableAdmin(newResponsableAdmin)
        self.mail = self.setUserMail(newResponsableAdmin, "groupeism")
        return (
            newResponsableAdmin.get("Matricule"),
            newResponsableAdmin.get("Nom"),
            newResponsableAdmin.get("Prénom"),
            self.mail, #Mail ResponsableAdmin
            newResponsableAdmin.get("Telephone"),
            self.mail, #Login ResponsableAdmin
            DEFAULT_PASSWORD,
            "ResponsableAdmin",
            newResponsableAdmin.get("Classes"),
            newResponsableAdmin.get("Chargés")
        )
        
    def addNewPartenaire(self, newPartenaire:dict):
        self.setPartenaire(newPartenaire)
        return (
            newPartenaire.get("Matricule"),
            newPartenaire.get("Libelle"),
            newPartenaire.get("Mail"), #Mail Partenaire
            newPartenaire.get("Telephone"),
            newPartenaire.get("Mail"), #Login Partenaire
            DEFAULT_PASSWORD,
            "Partenaire",
            newPartenaire.get("Etudiants")
        )
        
    
        
         