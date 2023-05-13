import os
import json
import sqlite3
from datetime import datetime
from random import randint
from string import ascii_uppercase
from time import sleep, time

import colorama as color
# pip install colorama : C'est un module qui permet de mettre la couleur
from colorama import init
from pyfiglet import figlet_format
from tabulate import tabulate  # # python -m pip install tabulate

init(autoreset=True)

#Couleur utilisées dans le code !

ERROR = color.Fore.RED
SUCCESS  = color.Fore.GREEN
WHITE  = color.Fore.WHITE
RED  = color.Fore.RED
YELLOW  = color.Fore.YELLOW
BLUE  = color.Fore.BLUE
CYAN  = color.Fore.CYAN
MAGENTA  = color.Fore.MAGENTA
WHITE  = color.Fore.WHITE

tab = '\t'
push = '\t'*4
DEFAULT_PASSWORD = "passer@123"
DEFAULT_EFFECTIF = 40
TAILLE_SCREEN = 150
BASE_FILE = "./DataBase/Database.sqlite3"
FOLDER_FILE = "DataBase/Students_Marks.json"
EGALE = "="

POLICES = ['avatar', 'banner', 'banner3-D', 'banner3', 'banner4', 'big', "isometric3", 'bulbhead']

RP_USECASES = {
    "main": ["Ajouter un nouveau", "Voir toutes les listes", "Modifier une information","Plus", "Se déconnecter"],
    "add": ["Ajouter un professeurs", "Ajouter un module", "Ajouter une filière"],
    "liste": ["Lister les professeurs", "Lister les modules", "Lister les filières", "Lister les chargés", "Lister les niveaux", "Lister les étudiants", "Menu général"],
    "more": ["Attribuer des classes aux chargés", "Voir la moyenne des etudiants d'une classe","Voir les statistiques", "Menu general"],
    "stat":["Les Statistiques d'une classe","Les Statistiques d'une Filiere"],
    "filtre": ["Tous","Filiere", "Classe", "Niveau", "Nationnalité"]
}

NIVEAUX = {
    "L1": "Licence 1",
    "L2": "Licence 2",
    "L3": "Licence 3",
    "M1": "Master 1",
    "M2": "Master 2"
}

ADMIN_USECASES = {
    "main": ["Ajouter un nouveau", "Voir toutes les listes", "Modifier une information", "Se déconnecter"],
    "add": ["Ajouter un étudiant","Ajouter un(e) chargé","Ajouter un(e) responsable","Ajouter un partenaire", "Retourner au menu général"],
    "liste" : ["Lister les étudiants", "Lister les chargé(e)s", "Lister les responsables","Lister les partenaires", "Retourner au menu général"],
    "edit": ["Profil", "Menu général"]
}

CHARGE_USECASE={
    "main":["Lister un profil","Voir les notes","Modifier une note","Initier Les notes d'un module","Commentaire", "Se deconnecter"],
    "Liste":["Lister les etudiants par Classe","Lister les professeurs", "Menu général"],
    "notes":["Notes d'une Classe","Notes d'un etudiant", "Menu général"],
    "edit":["Modifier les notes d'une classe","Modifier les notes d'un etudiant","Menu général"],
    "insert":["Pour une classe","Pour un etudiant","Menu général"],
    "commentaire":["Faire un commentaire","Voir les commentaires","Menu général"]
}
PARTENAIRE_USECASES = {
    "main":["Consulter le dossier d'un etudiant", "Se deconnecter"],
    "dossier":["Menu général"]
}

ETUDIANT_USECASE={
    "main":["Voir mes notes","Commentaire","Se deconnecter"],
    "commentaire":["Faire un commentaire","Voir mes commentaires"]
}


# s = sqlite3.connect(BASE_FILE)
# c = s.cursor()
# p = c.execute("ALTER TABLE Modules DROP notes ")
# s.commit()


class MySql: 
    def __init__(self) -> None:
        #Connexion à la base de donnée
        self.base = sqlite3.connect(BASE_FILE)
        #Initialisation du curseur de connexion
        self.curseur = self.base.cursor()
        
        self.TABLES_USER = {
            "Admin": ["Matricule", "Nom", "Prenom", "Mail", "Telephone", "Login","Password","TypeP"],
            "Chargé": ["Matricule", "Nom", "Prenom", "Mail", "Telephone", "Login", "Password", "TypeP",  "Classes"],
            "Etudiants": [ "Matricule", "Nom", "Prenom", "DateNaissance", "Nationnalité", "Mail", "Telephone", "Login", "Password", "TypeP","IdClasse", "Notes","Commentaires"],
            "partenaires": ["Id", "Libelle", "Mail", "Telephone", "Login", "Password", "TypeP"],
            "responsableAdmin": ["Matricule", "Nom", "Prenom", "Mail", "Telephone","Login", "Password", "TypeP"]
        }
        
        self.TABLES_OTHERS = {
            "filiere": ["idF","libelle","classes"], 
            "Modules": ["idM", "libelle", "classes", "professeurs","coefficient","credit"],
            "Niveau": ["idN","libelle","classes"],
            "professeurs": ["idP", "Nom", "Prenom", "mail", "Telephone", "modules", "Classes"], 
            "Classe": ["idC", 'libelle', 'effectif', 'chargé','filière', 'niveau', 'professeurs', 'modules', 'etudiants']
        }
        
        self.TABLES = {
            "Etudiants":"Matricule text, Nom text, Prenom text, DateNaissance text, Nationnalité text, Mail text, Telephone number, Login text, PassWord text, TypeP text, IdClasse number, Notes text", 
            "Chargé":"Matricule text, Nom text, Prenom text, mail text, Telephone number, Login text, Password text, TypeP text,  Classes text", 
            "Admin":"Matricule text, Nom text, Prenom text, mail text, Telephone number, Login text, Password text, TypeP text", 
            "Filiere":"idF number, libelle text, classes text", 
            "Modules":"idM number, libelle text, classes text, professeurs text, notes text", 
            "Niveau":"idN number, libelle text, classes text", 
            "partenaires":"id integer primary key autoincrement, libelle varchar(150), mail varchar(255), Telephone integer, Login varchar(255), Password varchar(150), TypeP varchar(150)", 
            "professeurs":"idP number, Nom text, Prenom text, mail text, Telephone number, Classes text, modules text", 
            "ResponsableAdmin":"Matricule text, Nom text, Prenom text, mail text, Telephone number, Login text, Password text, TypeP text",
            "Classe":"idC number, Libelle text, Filiere text, niveau number, effectif number, chargé text, professeurs text, modules text, etudiants text"
        }
        
        self.initTables(self.TABLES)
        
        self.datas = self.getUserData(self.TABLES_USER)
        self.component = self.getUserData(self.TABLES_OTHERS)
           
        #Mise à jour des changemements effectuer
        self.base.commit()
        
    def closeDB(self):
        self.base.close()

    def updateBase(self, table: str, changements: str, key: str, value):
        requete=f'UPDATE {table} SET {changements} WHERE {key}="{value}"' #L2 GRLS
        self.curseur.execute(requete)
        self.base.commit()
               
    def initTables(self,tables:dict):
        with self.base:
            for key, value in tables.items(): 
                requete = f"CREATE TABLE IF NOT EXISTS {key}({value})"
                self.curseur.execute(requete)
                self.base.commit()

    def getTables(self,requete:str):
        with self.base:
            self.curseur.execute(requete)
            return self.curseur.fetchall()

    def insert(self,table:str, value:tuple, colonne:list):
        with self.base:
            val = ', '.join(['?']*len(colonne))
            at = ", ".join(colonne)
            self.curseur.execute(f"INSERT INTO {table}({at}) VALUES ({val})",value)
            self.base.commit()
    
    def select(self, table:str):
        with self.base:
            self.curseur.execute(f"SELECT * FROM {table}")
            return self.curseur.fetchall()

        
    def delete(self,key:str,value,table:str):
        requete=f"DELETE FROM {table} WHERE {key}={value}"
        self.curseur.execute(requete)
        self.base.commit()
            
    def getUserData(self, tables:dict) -> dict:
        #Initialisation du dictionnaire qui va contenir les users
        data = dict()
        
        #Pourcourt de la table des users
        for key, value in tables.items():
            
            #Initialisation d'un liste de chaque table
            table_list = []
            
            #Exécution de la requette
            request = f"SELECT * FROM {key}"
            self.curseur.execute(request)
            
            #Parcourt de la liste de donnée de chaque table
            for user in self.curseur.fetchall():
                
                #Initialisation d'un nouveau utilisateur
                new_user = dict()
                valeur = 0
                
                #Parcourt de données d'un utilisateur et insertion dans le new_user
                for attribut in value:
                    new_user[attribut] = user[valeur]
                    valeur += 1
                
                #Insertion de l'utilisateur dans la liste de la table correspondant
                table_list.append(new_user)
            
            #Insertion de la liste de user de chaque table dans le dictionnaire de valeur selon la clé de la table
            data[key] = table_list
            
        #Retour du dictionnaire
        return data
    
###########################################################
############### Class de l'administrateur #################
###########################################################
class User:
    def __init__(self, matricule:str, nom:str, prénom:str, mail:str, téléphone:int, login:str, password:str, typeP: str) -> None:
        self.matricule = matricule
        self.nom = nom
        self.prénom = prénom
        self.mail = mail
        self.téléphone = téléphone
        self.login = login
        self.password = password
        self.typeP = typeP
    
    #Setters
    def setMatricule(self, newMatricule:str) -> None:
        self.matricule = newMatricule
    
    def setNom(self, newNom:str) -> None:
        self.nom = newNom
        
    def setPrénom(self, newPrénom:str) -> None:
        self.prénom = newPrénom
        
    def setMail(self, newMail:str) -> None:
        self.mail = newMail
        
    def setTéléphone(self, newTéléphone:int) -> None:
        self.téléphone = newTéléphone
        
    def setLogin(self, newLogin:str) -> None:
        self.login = newLogin
        
    def setPassword(self, newPassword:str) -> None:
        self.password = newPassword
        
    def setLibelle(self, newTypeP:str) -> None:
        self.typeP = newTypeP
        
    #Getters
    def getMatricule(self) -> str:
        return self.matricule 
    
    def getNom(self) -> str:
        return self.nom    
    
    def getPrénom(self) -> str:
        return self.prénom 
          
    def getMail(self) -> str:
        return self.mail    
     
    def getTéléphone(self) -> int:
        return self.téléphone 
        
    def getLogin(self) -> str:
        return self.login   
       
    def getPassword(self) -> str:
        return self.password 
            
    def getTypeP(self) -> str:
        return self.typeP      
    
###########################################################
############### Class de l'administrateur #################
###########################################################
class Admin(User):
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, etudiants:list = [], chargés:list = [], responsableAdmin:list = [], partenaires:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.etudiants = etudiants
        self.chargés = chargés
        self.responsableAdmins = responsableAdmin
        self.partenaires = partenaires
        self.usecase = DefaultUseCases()
        self.traitement()
        
    # def __init__(self) -> None:
    #     self.usecase = DefaultUseCases()
    #     self.traitement()
        
    def traitement(self):
        while True:
            match self.usecase.controlMenu("Menu général", ADMIN_USECASES["main"]):
                case 1:
                    while True:
                        match  self.usecase.controlMenu("Ajout d'un nouvel utilisateur", ADMIN_USECASES["add"]):
                            case 1:
                                self.usecase.showMsg("Liste des étudiants", clear=False)
                                self.ajoutEtudiant()
                                break
                            case 2:
                                self.usecase.showMsg("Liste des chargés")
                                self.ajoutChargé()
                                break
                            case 3:
                                self.usecase.showMsg("Liste des responsables administratifs")
                                self.ajoutRP()
                                break
                            case 4:
                                self.usecase.showMsg("Liste des partenaires")
                                self.ajoutPartenaire()
                                break
                            case 5:  break
                case 2:
                    while True:
                        match  self.usecase.controlMenu("Liste des utilisateurs", ADMIN_USECASES["liste"]):
                            case 1:
                                self.usecase.lister("Etudiants")
                                self.usecase.pause()
                                pass
                            case 2:
                                self.usecase.lister("Chargés")
                                self.usecase.pause()
                                pass
                            case 3:
                                self.usecase.lister("ResponsablesAdmin")
                                self.usecase.pause()
                                pass
                            case 4:
                                self.usecase.lister("Partenaires")
                                self.usecase.pause()
                                pass
                            case 5:
                                break
                    pass
                case 3:
                    while True:
                        match  self.usecase.controlMenu("Modifier une info", ADMIN_USECASES["edit"]):
                            case 1:
                                # self.ajoutEtudiant()
                                pass
                            case 2:
                                # self.ajoutChargé()
                                pass
                            case 3:
                                # self.ajoutRP()
                                pass
                            case 4:
                                break
                    pass
                case 4:
                    self.usecase.sql.closeDB()
                    break
        pass
        
    def ajoutPartenaire(self):
        date=self.usecase.CurrentDate()
        part = dict()
        part["Id"] = self.usecase.sql.getTables("SELECT count(Id) FROM partenaires;")[0][0] + 1
        part["Libelle"] = self.usecase.testSaisie("Entrez libelle de l'établissement : ").title() # type: ignore
        part["Mail"] = self.usecase.testSaisie("Entrez le mail de l'établissement : ").lower() # type: ignore
        part["Telephone"] = self.usecase.agree_number("Entrez le téléphone de l'établissement : ")
        while True:
            choix = self.usecase.question("Confirmer l'enregistrement")
            if choix == "oui":
                # self.usecase.sql.getTables(f"INSERT INTO partenaires(Libelle,Mail, Telephone, Login,PassWord,TypeP) VALUES({p[0]}, {p[1]}, {p[2]},{p[3]}, {p[4]}, {p[5]});")
                self.usecase.sql.insert("partenaires",self.addNewPartenaire(part), self.usecase.sql.TABLES_USER["partenaires"])
                self.usecase.sql = MySql()
                self.usecase.showMsg("Partenaire ajouté avec success")  
                break
            break
        
    def ajoutRP(self):
        date=self.usecase.CurrentDate()
        rp = dict()
        rp["Matricule"] = f"ISM{date[0]}/staff{len(self.usecase.sql.datas['responsableAdmin'])+1}-{date[1]}{date[2]}"
        rp["Nom"] = self.usecase.testSaisie("Entrez le nom du RP : ").upper() # type: ignore
        rp["Prénom"] = self.usecase.testSaisie("Entrez le prenom du RP : ").title() # type: ignore
        rp["Telephone"] = self.usecase.agree_number("Entrez le téléphone du RP : ")
        while True:
            choix = self.usecase.question("Confirmer l'enregistrement")
            if choix == "oui":
                self.usecase.sql.insert("responsableAdmin",self.addNewResponsableAdmin(rp), self.usecase.sql.TABLES_USER["responsableAdmin"])
                self.usecase.sql = MySql()
                self.usecase.showMsg("Reponsable ajouté avec success")  
                break
            break
    
    def ajoutChargé(self):
        date=self.usecase.CurrentDate()
        charge = dict()
        charge["Matricule"] = f"ISM{date[0]}/staff{len(self.usecase.sql.datas['Chargé'])+1}-{date[1]}{date[2]}"
        charge["Nom"] = self.usecase.testSaisie("Entrez le nom du chargé : ").upper() # type: ignore
        charge["Prénom"] = self.usecase.testSaisie("Entrez le prenom du chargé : ").title()# type: ignore
        charge["Telephone"] = self.usecase.agree_number("Entrez le téléphone du chargé : ")
        while True:
            choix = self.usecase.question("Confirmer l'enregistrement")
            if choix == "oui":
                self.usecase.sql.insert("Chargé",self.addNewChargé(charge), self.usecase.sql.TABLES_USER["Chargé"])
                self.usecase.sql = MySql()
                self.usecase.showMsg("Chargés ajouté avec succes")  
                break
            break
             
    def ajoutEtudiant(self):
        date=self.usecase.CurrentDate()
        etudiant = dict()
        matricule = f"ISM{date[0]}/DK{len(self.usecase.sql.datas['Etudiants'])+1}-{date[1]}{date[2]}"
        classe = self.usecase.createOrSearchClasse(self.usecase.getIdClasse())
        print("\nDONNEES DE L'ETUDIANT")
        etudiant = {
            "Matricule":matricule,
            "Nom":self.usecase.testSaisie("Nom de l'Etudiant : ").upper(), # type: ignore
            "Prénom":self.usecase.testSaisie("Prenom de l'Etudiant : ").title(), # type: ignore
            "DateNaissance":self.usecase.ver_date("\nINFORMATIONS SUR LA DATE DE NAISSANCE"),
            "Nationnalité":self.usecase.testSaisie(f"\nDONNEES SUPPLEMENTAIRES\n{push}Nationnalité: ").capitalize(), # type: ignore
            "Telephone":self.usecase.agree_number("Etudiant")
        }
        while True:
            choix=self.usecase.question("Confirmer l'enregistrement")
            if choix =="oui":
                if type(classe) == tuple:
                    etudiant["IdClasse"] = classe[0]
                    listeMatricules=self.usecase.listTrans(classe[1]["etudiants"])
                    listeMatricules.append(matricule)
                    changement=f"effectif={classe[1]['effectif'] + 1},etudiants=\"{str(listeMatricules)}\""
                    self.usecase.sql.updateBase("Classe", changement,"idC",classe[0])
                elif type(classe) == dict: 
                    etudiant["IdClasse"] = classe["idC"]
                    classe["etudiants"] = f"{[matricule]}"
                    self.usecase.sql.insert('Classe',tuple(classe.values()), self.usecase.sql.TABLES_OTHERS["Classe"])
                    
                self.usecase.sql.insert("Etudiants",self.user(etudiant), self.usecase.sql.TABLES_USER["Etudiants"])
                self.usecase.sql = MySql()
                self.usecase.showMsg("Etudiant ajouté avec succes")
                break
            break
        
    def setUserMail(self, user:dict, domaine:str = "ism.edu",):
        return  f"{user.get('Prénom').replace(' ', '-').lower()}.{user.get('Nom').split(' ')[-1].lower()}@{domaine}.sn" # type: ignore
    
    def user(self, newEtu:dict):
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
            newEtu.get("IdClasse"),
            '[]'
        )
        
    def addNewChargé(self, newChargé:dict):
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
            "[]"
            )
        
    def addNewResponsableAdmin(self, newResponsableAdmin:dict):
        self.mail = self.setUserMail(newResponsableAdmin, "groupeism")
        return (
            newResponsableAdmin.get("Matricule"),
            newResponsableAdmin.get("Nom"),
            newResponsableAdmin.get("Prénom"),
            self.mail, #Mail ResponsableAdmin
            newResponsableAdmin.get("Telephone"),
            self.mail, #Login ResponsableAdmin
            DEFAULT_PASSWORD,
            "ResponsableAdmin"
        )
        
    def addNewPartenaire(self, newPartenaire:dict):
        return (
            newPartenaire.get("Id"),
            newPartenaire.get("Libelle"),
            newPartenaire.get("Mail"), #Mail Partenaire
            newPartenaire.get("Telephone"),
            newPartenaire.get("Mail"), #Login Partenaire
            DEFAULT_PASSWORD,
            "Partenaire"
        )
    
###########################################################
#################### Class du chargé ######################
###########################################################

class Chargé(User):
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, classes:list = [], commentaires:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.classes = classes #les ids des classes
        self.commentaires = commentaires
        self.usecase=DefaultUseCases()
        self.classeChargé=self.usecase.sql.getTables(f"SELECT * FROM Classe WHERE chargé='{self.matricule}'")
        self.traitement()
    
    # def __init__(self) -> None:
    #     self.classes = [1,3,5,8] #les ids des classes
    #     self.matricule = "ISM2023/staff2-0416"
    #     self.usecase = DefaultUseCases()
    #     self.classeChargé = self.usecase.sql.getTables(f"SELECT * FROM Classe WHERE chargé='{self.matricule}'")
    #     self.traitement()
    
    
        
    def makeCommentaire(self,matriculeEtu:int, newCommentaire:str, data:list):
        for etudiant in data:
            if etudiant.get("Matricule") == matriculeEtu:
                etudiant.get("Commentaires").append(newCommentaire)
                return True
        return False        
        
    #Fonctionnalités du chargé
    def setCommentaires(self, newCommentaire:dict): self.commentaires.append(newCommentaire)
        
    def listeCommentaire(self):
        print("="*TAILLE_SCREEN)
        print(f"{'IdClasse':<20}{'IdEtudiant':<20}{'Commentaire'}")
        print("="*TAILLE_SCREEN)
        for com in self.commentaires:
            print(f"{com.get('idClasse'):<20}{com.get('idEtu'):<20}{com.get('Commentaire')}")
            print('-'*TAILLE_SCREEN)
    
    

    #Setters
    def setClasse(self, newClasse:str) -> None: self.classes.append(newClasse)
        
    # Getters
    def getClasse(self) -> list: return self.classes
    
    def traitement(self):
        while True:
            match self.usecase.controlMenu("Menu General",CHARGE_USECASE["main"]): # "Menu général"
                case 1:
                    while True:
                        match self.usecase.controlMenu("Menu Liste",CHARGE_USECASE["Liste"]): # "Menu liste
                            case 1:
                                self.usecase.showMsg("Liste des etudiants de la Classe",wait=False)
                                self.listeEtudiant()
                            case 2:
                                self.usecase.showMsg("Liste des professeurs",wait=False)
                                self.usecase.lister("Professeurs")
                                self.usecase.pause()
                            case 3: break 
                case 2:
                    while True:
                        match self.usecase.controlMenu("Menu Notes",CHARGE_USECASE["notes"]):
                            case 1:
                                self.usecase.showMsg("Liste des Notes des etudiants",wait=False)
                                self.showNotes()
                                pass
                            case 2:
                                self.usecase.showMsg("Notes de l'etudiant",wait=False)
                                self.showNotesEtu()
                            case 3: break
                case 3:
                    while True:
                        match self.usecase.controlMenu("Menu Modification Notes",CHARGE_USECASE["edit"]):
                            case 1:
                                self.usecase.showMsg("Modifier la note d'une classe",wait=False)
                                self.modifNotes()
                            case 2:
                                self.usecase.showMsg("Modifier la note d'un etudiant",wait=False)
                                self.modifNoteEtu()
                            case 3: break
                case 4:
                    while True:
                        match self.usecase.controlMenu("Menu initialisation Notes",CHARGE_USECASE["insert"]):
                            case 1:
                                self.usecase.showMsg("initialisation de notes pour une classe",wait=False)
                                self.InitNotesClasse()
                            case 2:
                                self.usecase.showMsg("initialisation de notes pour un etudiant",wait=False)
                                self.InitNotesMod()
                            case 3:break
                case 5:
                    while True:
                        match self.usecase.controlMenu("Menu Commentaire",CHARGE_USECASE["commentaire"]):
                            case 1:
                                self.usecase.showMsg("Faire un Commentaire",wait=False)
                                self.DoCommentaire()
                                
                                pass
                            case 2:
                                self.usecase.showMsg("Voir les Commentaires")
                                pass
                            case 3: break
                case 6:
                    break
    def listeEtudiant(self)->None:
        while True:
            att = self.usecase.sql.TABLES_OTHERS["Classe"][:2]
            data = self.usecase.sql.getTables(f"SELECT idC, libelle FROM Classe where chargé='{self.matricule}' ")
            print(tabulate(headers=att,tabular_data= data, tablefmt='double_outline'))
            libelle = self.usecase.testSaisie("Entrez le libelle de la classe : ").upper() # type: ignore
            for classe in self.classeChargé:
                if(classe[1]==libelle):
                    classeEtu=list()
                    if(self.usecase.listTrans(classe[8],"chaine")!=[]):
                        for matricule in self.usecase.listTrans(classe[8],"chaine"):
                            etudiant=self.usecase.sql.getTables(f"SELECT Matricule, Nom, Prenom, DateNaissance, Nationnalité, Mail, Telephone FROM Etudiants Where Matricule='{matricule}' ")
                            if(etudiant!=[]):
                                classeEtu.append(etudiant[0])
                            
                    break
                
            if(classeEtu!=[]):#type:ignore
                break
            
        attributs=self.usecase.sql.TABLES_USER["Etudiants"][:7]
        print(tabulate(headers=attributs,tabular_data=classeEtu, tablefmt='double_outline')) #type:ignore
        self.usecase.pause()
    
    def showNotes(self)->None:
        while True:
            att = self.usecase.sql.TABLES_OTHERS["Classe"][:2]
            data = self.usecase.sql.getTables(f"SELECT idC, libelle FROM Classe where chargé='{self.matricule}' ")
            print(tabulate(headers=att,tabular_data= data, tablefmt='double_outline'))
            libelle = self.usecase.testSaisie("Entrez le libelle de la classe : ").upper() # type: ignore
            for classe in self.classeChargé:
                listEtu=list()
                if(classe[1]==libelle):
                    if(self.usecase.listTrans(classe[8],"chaine")!=[]):
                        listEtu=self.usecase.sql.getTables(f"SELECT Matricule, Nom, Prenom, Notes FROM Etudiants WHERE IdClasse='{classe[0]}' ")
                    break
            break
        
        attributs=self.usecase.sql.TABLES_USER["Etudiants"][:3]
        note=self.usecase.sql.TABLES_USER["Etudiants"][11]
        attributs.append(note)
        print(tabulate(headers=attributs,tabular_data= listEtu, tablefmt='double_outline'))  #type:ignore
        self.usecase.pause()
        
    def InitNotesMod(self)->None:
        while True: 
            module = self.usecase.testSaisie("Entrez le libelle du module : ")
            noteEvaluation = self.usecase.testSaisie("Entrez la note d'evaluation : ","int",0,20)
            noteExam = self.usecase.testSaisie("Entrez la note d'examen : ","int",0,20)
            matricule = self.usecase.testSaisie("Entrez le matricule de l'etudiant' : ").upper() # type: ignore
            notes=self.usecase.sql.getTables(f"SELECT Notes FROM Etudiants WHERE Matricule='{matricule}' ")
            noteList=self.usecase.listTrans(notes[0][0])
            dicoList=self.usecase.convertion(noteList)
            dicoList[f"{module}"]=list()
            dicoList[f"{module}"].append(noteEvaluation)
            dicoList[f"{module}"].append(noteExam)
            print(self.usecase.dicoTrans(dicoList))
            changement=f'Notes="{self.usecase.dicoTrans(dicoList)}" '
            self.usecase.sql.updateBase("Etudiants",changement,"Matricule",matricule)
            if self.usecase.question("Voulez vous ajouter les notes d'un autre module") == 'oui':
                continue
            else: break
            
    def InitNotesClasse(self)->None:
        while True:
            libelle = self.usecase.testSaisie("Entrez le libelle de la classe : ").upper() # type: ignore
            module = self.usecase.testSaisie("Entrez le libelle du module : ").title() # type: ignore
            classe=self.usecase.sql.getTables(f"SELECT * FROM Classe WHERE Libelle='{libelle}' ")
            etudiants=self.usecase.listTrans(classe[0][8],"chaine")
            for etu in etudiants:
                noteEvaluation = self.usecase.testSaisie("Entrez la note d'evaluation : ","int",0,20)
                noteExam = self.usecase.testSaisie("Entrez la note d'examen : ","int",0,20)
                notes = self.usecase.sql.getTables(f"SELECT Notes FROM Etudiants WHERE Matricule='{etu}' ")
                print(notes[0][0])
                noteList = self.usecase.listTrans(notes[0][0])
                dicoList = self.usecase.convertion(noteList)
                dicoList[f"{module}"] = list()
                dicoList[f"{module}"].append(noteEvaluation)
                dicoList[f"{module}"].append(noteExam)
                print(self.usecase.dicoTrans(dicoList))
                changement = f'Notes="{self.usecase.dicoTrans(dicoList)}" '
                self.usecase.sql.updateBase("Etudiants",changement,"Matricule",etu[0])
            if self.usecase.question("Voulez vous ajouter les notes d'un autre module") == 'oui':
                continue
            else: break
        
    def showNotesEtu(self)->None:
        while True:
            matEtu = self.usecase.testSaisie("Entrez le matricule de l'etudiant : ").upper() # type: ignore
            listEtu = self.usecase.sql.getTables(f"SELECT Matricule, Nom, Prenom, Notes FROM Etudiants ")
            for etu in listEtu:
                if(matEtu == etu[0]):
                    attributs = ["Module","Note Evalution","Note Examen"]
                    modules = self.usecase.getListe(etu[3])
                    print(f"Etudiant: {etu[1]} {etu[2]}")
                    print(tabulate(headers=attributs,tabular_data=modules, tablefmt='double_outline'))  #type:ignore
                    self.usecase.pause()
                    break
            break
                    
    def modifNoteEtu(self)->None:
        while True:
            matricule = self.usecase.testSaisie("Entrez le matricule de l'etudiant : ").upper() # type: ignore
            module = self.usecase.testSaisie("Entrer le libelle du module: ").title() # type: ignore
            typeNote = self.usecase.testSaisie("Enter le type de note à modifier [Evaluation|Examen]: ").lower() # type: ignore
            newNote = self.usecase.testSaisie("Entrez la nouvelle note: ","int",0,20)    
            notes = self.usecase.sql.getTables(f"SELECT Notes FROM Etudiants WHERE Matricule='{matricule}' ")
            listNotes = self.usecase.getListe(notes[0][0])
            for liste in listNotes:
                if(liste[0] == module.title()): # type: ignore
                    if(typeNote.lower() == "evaluation"): liste[1] = newNote #type:ignore
                    else: liste[2] = newNote
            dico=dict()
            for i in listNotes:
                dico[f"{i[0]}"] = list()
                dico[f"{i[0]}"].append(i[1])
                dico[f"{i[0]}"].append(i[2])
            changement = f'Notes="{self.usecase.dicoTrans(dico)}" '
            print(changement)
            self.usecase.sql.updateBase("Etudiants",changement,"Matricule",matricule)
            self.usecase.pause()  
            if self.usecase.question("Voulez vous modifier une autre note") == 'oui': continue
            else: break  
            
    def modifNotes(self)->None:
        att = self.usecase.sql.TABLES_OTHERS["Classe"][:2]
        data = self.usecase.sql.getTables(f"SELECT idC, libelle FROM Classe where chargé='{self.matricule}' ")
        print(tabulate(headers=att,tabular_data= data, tablefmt='double_outline'))
        
        libelle = self.usecase.testSaisie("Entrer le libelle de la classe: ").upper() # type: ignore
        module = self.usecase.testSaisie("Entrer le libelle du module: ").title() # type: ignore
        typeNote = self.usecase.testSaisie("Enter le type de note à modifier [Evaluation|Examen]: ").lower()  #type:ignore
        IdClasse = self.usecase.sql.getTables(f"SELECT idC from Classe where Libelle='{libelle}' ")
        etudiants = self.usecase.sql.getTables(f"SELECT Matricule, Nom, Prenom, Notes from Etudiants WHERE IdClasse={IdClasse[0][0]}")
        for etu in etudiants:
            newNote = self.usecase.testSaisie("Entrez la nouvelle note: ","int",0,20) 
            listNotes = self.usecase.getListe(etu[3])
            for liste in listNotes:
                if(liste[0] == module.title()): # type: ignore
                    if(typeNote.lower() == "evaluation"): liste[1] = newNote #type:ignore
                    else: liste[2] = newNote
                    dico = dict()
                    dico[f"{liste[0]}"] = list()
                    dico[f"{liste[0]}"].append(liste[1])
                    dico[f"{liste[0]}"].append(liste[2])
                    changement=f'Notes="{self.usecase.dicoTrans(dico)}" '
                    print(changement)
                    self.usecase.sql.updateBase("Etudiants",changement,"Matricule",etu[0])   
        self.usecase.pause()
             
    def DoCommentaire(self)->None:
        entite = self.usecase.testSaisie("Enter le destinataire du commentaire[Classe|Etudiant]: ").capitalize() #type:ignore
        date = self.usecase.CurrentDate()
        if(entite == "Classe"):
            libelle = self.usecase.testSaisie("Entrer le libelle de la classe: ")
            classe = self.usecase.sql.getTables(f"SELECT * FROM Classe WHERE Libelle='{libelle}' ")
            print(classe[0][8])
            self.usecase.pause()
            commentaire = self.usecase.testSaisie("Saisir votre commentaire: ")
            listCom = list()
            for matricule in self.usecase.listTrans(classe[0][8],"chaine"):
                etudiant = self.usecase.sql.getTables(f"SELECT Commentaires FROM Etudiants WHERE Matricule='{matricule}' ")
                
                com = f"{date[2]}-{date[1]}-{date[0]}---{commentaire}"
                listCom = self.usecase.listTrans(etudiant[0][0],"chaine")
                listCom.append(com) #02-05-2023  ('02',)
                changement = f'Commentaires="{listCom}" '
                self.usecase.sql.updateBase("Etudiants",changement,"Matricule",matricule)
            self.usecase.pause()
                
        elif(entite == "Etudiant"):
            matricule = self.usecase.testSaisie("Saisir le matricule de l'etudiant: ")
            commentaire = self.usecase.testSaisie("Saisir votre commentaire: ")
            etudiant = self.usecase.sql.getTables(f"SELECT Commentaires FROM Etudiants WHERE Matricule='{matricule}' ")
            com = f"{date[2]}-{date[1]}-{date[0]}---{commentaire}"
            listCom = self.usecase.listTrans(etudiant[0][0],"chaine")
            listCom.append(com) #02-05-2023  ('02',)
            changement = f'Commentaires="{listCom}" '
            self.usecase.sql.updateBase("Etudiants",changement,"Matricule",matricule)
            
    def ShowCommentaires(self)->None:
        commentaires = self.usecase.sql.getTables(f"SELECT Commentaires from Chargé where Matricule='{self.matricule}'")
        
###########################################################
################### Quelsques classes #####################
###########################################################
class DefaultUseCases:
    def __init__(self) -> None:
        self.sql = MySql()
        self.all_User_Data = self.sql.datas #Données des utilisateurs.
        self.all_Other_Data = self.sql.component #Données des filières et autres infos
    
    def lister(self, table:str, filtre: str = "Tous", value: str = ""):
        match table:
            case 'Etudiants':
                attributs = self.sql.TABLES_USER["Etudiants"][:7]
                attributs.append("Classe")
                    
                if filtre == "Tous":  data = self.sql.getTables(f"SELECT Matricule, Nom, Prenom, DateNaissance, Nationnalité, Mail, Telephone, libelle FROM Etudiants LEFT JOIN Classe ON Etudiants.idClasse = Classe.idC")
                elif filtre == "Nationnalité": data = self.sql.getTables(f"SELECT Matricule, Nom, Prenom, DateNaissance, Nationnalité, Mail, Telephone, libelle FROM Etudiants LEFT JOIN Classe ON Etudiants.idClasse = Classe.idC WHERE Etudiants.Nationnalité = '{value}'")
                else: data = self.sql.getTables(f"SELECT Matricule, Nom, Prenom, DateNaissance, Nationnalité, Mail, Telephone, libelle FROM Etudiants LEFT JOIN Classe ON Etudiants.idClasse = Classe.idC WHERE Classe.{filtre} = '{value}'") 
            
            case 'Chargés':
                attributs = self.sql.TABLES_USER["Chargé"][:5]
                attributs.append("Classes")
                data = self.sql.getTables(f"SELECT Matricule, Nom, Prenom, mail, Telephone FROM Chargé")
                i = 0
                for classe in self.sql.getTables("SELECT classes FROM Chargé"): #[('[1,2,3]',), ('[1,2,3]',), ('[1,2,3],')]]
                    chargeClasses = "-"
                    listeClasses =  self.listTrans(classe[0])
                    if listeClasses != []:
                        chargeClasses = ""
                        for idC in listeClasses:
                            classe = self.sql.getTables(f"SELECT libelle FROM Classe WHERE idC = {idC}")
                            chargeClasses += f"{classe[0][0]} "
                    data[i] = list(data[i])
                    data[i].append(chargeClasses)
                    i += 1   
                    
            case 'Classes':
                attributs = self.sql.TABLES_OTHERS["Classe"][:4]
                data = self.sql.getTables(f"SELECT idC, Libelle, effectif, chargé FROM Classe")
                
            case 'Modules':
                attributs = self.sql.TABLES_OTHERS["Classe"][:2]
                data = self.sql.getTables(f"SELECT idM, libelle FROM Modules")
                
            case 'Niveau':
                attributs = ["Libelle"]
                data = [[n] for n in NIVEAUX.values()]
                
            case 'Filiere':
                attributs = self.sql.TABLES_OTHERS["filiere"][:2]
                data = self.sql.getTables(f"SELECT idF, libelle FROM filiere")
                
            case 'Professeurs':
                attributs = self.sql.TABLES_OTHERS["professeurs"][:6]
                data = self.sql.getTables(f"SELECT idP, Nom, Prenom, mail, Telephone, modules FROM professeurs")
                    
            case 'Partenaires':
                attributs = self.sql.TABLES_USER["partenaires"][:4]
                data = self.sql.getTables(f"SELECT Id, Libelle, Mail, Telephone FROM partenaires")
                
            case 'ResponsablesAdmin':
                attributs = self.sql.TABLES_USER["responsableAdmin"][:5]
                data = self.sql.getTables(f"SELECT Matricule, Nom, Prenom, mail, Telephone FROM responsableAdmin")
            
        if data != []:#type:ignore
            print(tabulate(headers=attributs,tabular_data= data, tablefmt='double_outline'))#type:ignore
        else:
            self.showMsg("Vous n'avez pas de données !", clear=False)
    
    def loadStudentsFolder(self) -> dict:
        with open(FOLDER_FILE, encoding="UTF-8") as f:
            return json.load(f)
        
    def convertion(self,liste:list)->dict:
        it = iter(liste)
        return dict(zip(it, it))
    
    def dicoTrans(self,dico: dict) -> list:#{key: "value"}
        return list(dico.items())
    
    def getListe(self,dicoChaine)->list:
        module = list()
        modules = list()
        i = 0
        for note in self.listTrans(dicoChaine, "chaine"):
            i += 1
            if(i == 1 or i == 2):
                module.append(note[2:])
            elif(i == 3):
                module.append(note[1:-2])
                modules.append(module)
                module, i = [], 0
        return modules
    
    def header(self,titre:str):
        self.ligne()
        self.ligne()
        self.opération(titre)
    
    def opération(self,title:str): self.showMsg(title,clear=False, wait=False)
    
    def menuUse(self,titre, fonctionnalités:list, Fermer=True):
        self.clear()
        self.opération(titre)
        options = []
        choices = []
        numChoix, tailleCollonne, nbreFonction = 1, len(max(fonctionnalités)) + 10, len(fonctionnalités)
        m = tailleCollonne*nbreFonction
        l = TAILLE_SCREEN-m
        # t = (TAILLE_SCREEN//nbreFonction)
        if l > 0:tailleCollonne += (l // nbreFonction)
        else:tailleCollonne = TAILLE_SCREEN // nbreFonction
        for useCase in  fonctionnalités:
            options.append([useCase,tailleCollonne, 'center'])
            choices.append([numChoix, tailleCollonne, 'center'])
            numChoix += 1
        self.ligneMenu(numChoix,tailleCollonne,'haut')
        self.showMenu(options)
        self.showMenu(choices)
        if Fermer:self.ligneMenu(numChoix,tailleCollonne,'bas')
        
    def ligneMenu(self,nombreFonctionnalités:int,longueurCellule:int,niveau:str):
        match niveau:
            case 'milieu': cotéG, cotéD, separateur = '╠','╣','╩'
            case 'haut':  cotéG, cotéD, separateur = '╔','╗','╦'
            case 'bas': cotéG, cotéD, separateur = '╚','╝','╩' 
        début = list('{}{}'.format('-'*(longueurCellule-1), separateur))*(nombreFonctionnalités-1)#type:ignore
        début[0], début[-1] = f'{cotéG}-',f'{cotéD}'#type:ignore
        print("".join(début))

    def showMenu(self, listeOptions:list,tracer = True, endE = "|", screen:int = TAILLE_SCREEN):
        """
        ### Summary:
            Cette fonction nous permet d'affichez une liste d'option pour l'utilisateur
        ### Args:
            - listeOptions (list): qui contient: exemple : ["Ajouter un étudiant", 50, "Center"]
                - Le libelle 
                - La taille qu'occupera la position dans le menu
                - La position du libelle
            - tracer
            - endE (str, optional): Ce sont les bords de l'option. Defaults to "|".
            - screen (int, optional): C'est la taille de l'écran. Defaults to TAILLE_SCREEN.
        """        
        Som, iCmpt = 0, 1
        l = [['useCase',50, 'center']]
        for j in listeOptions: Som+=j[1]
        if Som <= screen:
            for i in listeOptions:
                if type(i) == type([]) and type(i[1]) == type(1):
                    if iCmpt == len(listeOptions):
                        if i[2] == "left": print(f"{endE}{i[0]:<{i[1]-1}}{endE}", end="")
                        elif i[2] == "right": print(f"{endE}{i[0]:>{i[1]-1}}{endE}", end="")
                        elif i[2]  == "center": print(f"{endE}{i[0]:^{i[1]-1}}{endE}", end="")
                    else:
                        if i[2] == "left": print(f"{endE}{i[0]:<{i[1]-1}}", end="")
                        elif i[2] == "right": print(f"{endE}{i[0]:>{i[1]-1}}", end="")
                        elif i[2]  == "center": print(f"{endE}{i[0]:^{i[1]-1}}", end="")
                    iCmpt +=1
        else: print("error")
        print("")   
   
    def showMsg(self,msg:str, clear:bool = True,color=SUCCESS, motif:str='═', screen:int = TAILLE_SCREEN, wait:bool = True) -> None:
        if clear: self.clear()
        print(f"""╔{motif*(screen-2)}╗\n║{' '*(screen-2)}║\n║{color}{msg:^{screen-2}}{WHITE}║\n║{' '*(screen-2)}║\n╚{motif*(screen-2)}╝""")
        if wait:sleep(2)
        
    def pause(self): os.system("pause")
    
    def showWord(self,mot:str, police:str = "standard")-> str: return figlet_format(mot, font=police)
    
    def start(self):
        space = ' '
        self.clear()
        print("\n\n")
        print("="*(TAILLE_SCREEN-30))
        print(SUCCESS + self.showWord(f"{space*20}Gestionnaire"))
        print(SUCCESS + self.showWord(f"{space*41}de"))
        print(SUCCESS + self.showWord(f"{space*33}notes"))
        print("="*(TAILLE_SCREEN-30))
        
        #Barre de chargements
        nbrePoints, nbreEspace = 0, 4
        for i in range(1,51):
            nbreEspace -= 1
            print(f"Loading{'.'*nbrePoints}{' '*nbreEspace}" + f" {color.Back.GREEN}{' '}"*(i)+f"{color.Back.BLACK}{' '*((TAILLE_SCREEN-50)-20-(2*i))}  " + f"{2*i}%", end='\r')
            nbrePoints += 1
            if nbrePoints > 3:nbrePoints, nbreEspace = 0, 4
            sleep(randint(1, 50)/100)
        sleep(3)

    def accueil(self):
        cpt = 1
        self.start()
        while True:
            
            self.clear()
            print("="*(TAILLE_SCREEN-50))
            print(SUCCESS + self.showWord('Connexion'))
            print("="*(TAILLE_SCREEN-50))
            
            login = input(f"\n{tab*3}Entrez votre login : {SUCCESS}")
            print(BLUE + f"{tab*3}{'='*(len(login)+21)}")
            psw = input(f"\n{tab*3}Entrez votre mot de passe : {SUCCESS}")
            print(BLUE + f"{tab*3}{'='*(len(psw)+28)}")
            sleep(0.5)
            
            user_connect = self.connect(login, psw)
            if user_connect != {}: return user_connect
            else:
                # self.showMsg(ERROR + self.showWord("invalide"))
                if cpt == 3:
                    self.clear()
                    self.ligne("=",100)
                    print(f"\n\t\t{BLUE} {'Vous avez essayer de vous connecter trois(3) fois de suites sans succes'.upper()} !\n")
                    
                    if self.question("Quitter") == "oui": self.quitter()
                    cpt = 0
                else: self.showMsg("VOTRE LOGIN ET/OI MOT DE PASSE ET/SONT INVALIDES ! ",color=ERROR,screen=100)   
                cpt += 1
                              
    def question(self,message:str):
        haut, mil, bas  = f"╔{'-'*((TAILLE_SCREEN-50)-2)}╗", f"╠{'-'*52}╦{'-'*45}╣", f"╚{'-'*52}╩{'-'*45}╝"
        l = f"        {message.upper()} ?"
        texte = f"|{l:^{TAILLE_SCREEN-52}}|"
        oui, non = f"{SUCCESS}Oui",f"{RED}Non{WHITE}"
        choix = f"|{oui:^56}|{non:^56}|"
        print(f"{haut:^{TAILLE_SCREEN}}")
        print(f"{texte:^{TAILLE_SCREEN}}")
        print(f"{mil:^{TAILLE_SCREEN}}")
        print(f"{choix:^{TAILLE_SCREEN+15}}")
        # self.showMenu([[f"{SUCCESS}Oui", 58, "center"],[f"{RED}Non{WHITE}", 57, "center"]], screen=((TAILLE_SCREEN-30)))
        print(f"{bas:^{TAILLE_SCREEN}}")
        return input(f"\n\t\t\t\t\t\t\tFaites votre choix : {SUCCESS}").lower()  
                              
    def listTrans(self,liste: str, typeValue:str= 'entier') -> list: #type:ignore
        match typeValue:
            case 'entier': return [int(i) for i in liste[1:-1].replace("'","").split(',') if i.replace(" ","").isdigit()]
            case 'chaine':  return [i for i in liste[1:-1].replace("'",'').split(',')]
            case 'note': return [float(i) if i.isdigit() or i.count('.') == 1 else i for i in liste[1:-1].replace("'",'').split(',')]
                                 
    def quitter(self):
        self.clear()
        print(SUCCESS + self.showWord("a bientot :)"))
        sleep(5)
        self.clear()
        exit(0)
    
    def clear(self):
        if os.name == 'nt':  os.system("cls") 
        else:  os.system("clear")

    def connect(self, login:str, password:str)-> dict:
        for liste_user in self.all_User_Data.values():
            for user in liste_user:
                if (login == user.get("Login") and password == user.get("Password")): return user
        return {}
    
    def ligne(self, motif:str = "-", nombre:int = TAILLE_SCREEN): print(motif*nombre)
     
    def showComponents(self, attributs:list, data:list):
        self.ligne("=")
        for attribut in attributs: print(f"{attribut}", end=" ")
        self.ligne("=")
        
        for user in data:
            for i in range(len(attributs)): print(f"{user.get(attributs[i])}", end=" ")
            self.ligne()
    
    def control(self,key:str,value,data:list):
        for element in data:
            if(element.get(key)==value): return True
        return False
    
    def DoWhile(self,key:str,data:list):
        while True :
            value = input(f"saisir le {key}: ")
            if(self.control(key,value,data)): #type:ignore
                return value
    
    def getComponentByKey(self,key,value,data) ->dict:
        for element in data:
            if(element.get(key)==value): return element
        return {}

    def listerLesEtudiants(self,data:dict,valeur,filtre="Tous"):
        All_Etudiants = data.get("Etudiants")     
        if (filtre == "Tous"): donnees = All_Etudiants
        elif (filtre == "Niveau"): donnees = [etu for etu in All_Etudiants if (self.getComponentByKey("idC",etu.get("Classe"),data.get("Classes")).get("Niveau") == valeur)]  #type:ignore
        elif (filtre == "Filiere"): donnees = [etu for etu in All_Etudiants if (self.getComponentByKey("idC",etu.get("Classe"),data.get("Classes")).get("Filiere") == valeur)]  #type:ignore
        elif (filtre == "Classe"): donnees = [etu for etu in All_Etudiants if (etu.get("Classe") == valeur)]  #type:ignore
        else: donnees = [etu for etu in All_Etudiants if (etu.get("Nationnalité") == valeur)]  #type:ignore    
        
        print(f"{'Matricule':<10}{'Nom':<10}{'Prenom':<30}{'Date-Naissance':<10}{'Nationnalité':<10}{'Mail':<20}{'Telephone':<10}{'Classe':<10}")
        for etu in donnees: #type:ignore
            print(f"{etu.get('Matricule'):<10}{etu.get('Nom'):<10}{etu.get('Prenom'):<30}{etu.get('Date-Naissance'):<10}{etu.get('Nationnalité'):<10}{etu.get('Mail'):<20}{etu.get('Telephone'):<10}{etu.get('Classe'):<10}")
    
    def Saisie(self,message,min,max):
        nbre = input(f"{message} : ")
        ver = nbre.replace("-","")
        if  ver.isdigit() and (int(nbre) >= min and int(nbre) <= max): return int(nbre)
         
    def testSaisie(self, message:str, catégorie: str = 'str', min: int = 0, max: int = 100, nbreChar: int = 3):
        while True:
            element = input(f"{push}{message}{SUCCESS}")
            print(f"{push}{BLUE}{'='*len(message + element)}")
            match catégorie:
                case 'int':
                    ver = element.replace("-","")
                    if ver.isdigit() and (int(element) >= min and int(element) <= max): return int(element)
                    else:
                        self.showMsg("Vous devez saisir un entier !", color = RED)
                        self.clear()
                case 'str':
                    if(len(element) >= nbreChar): return element
                    else:
                        self.showMsg(f"Vous devez entrer une chaîne d'au moins {nbreChar}(s) charactères !", color = RED)
                        self.clear()
            
    def createUser(self,user:dict): 
        Profil=user.get("TypeP")
        match(Profil):
            case "Admin": return Admin(user["Matricule"],user["Nom"],user["Prenom"],user["Mail"],user["Telephone"],user["Login"],user["Password"],user["TypeP"])
            case "ResponsableAdmin": return ResponsableAdmin(user["Matricule"],user["Nom"],user["Prenom"],user["Mail"],user["Telephone"],user["Login"],user["Password"])
            case "Chargé": return Chargé(user["Matricule"],user["Nom"],user["Prenom"],user["Mail"],user["Telephone"],user["Login"],user["Password"],user["TypeP"])
            case "Etudiant": return Etudiant(user["Matricule"],user["Nom"],user["Prenom"],user["DateNaissance"],user["Nationnalité"],user["Mail"],user["Telephone"],user["Login"],user["Password"],user["TypeP"],user["IdClasse"],user["Notes"],user["Commentaires"])
            case "Partenaire": return Partenaire(user["Id"],user["Libelle"],user["Mail"],user["Telephone"],user["Login"],user["Password"],user["TypeP"])
            
    def test(self,message,text=""):
        if(text!=""): print(text)
        while True:
            element=input(message)
            if(element!=""): return element
                
    def ver_date(self, message:str=""):
        print(message)
        max=self.CurrentDate()[0]
        annee = "{:04d}".format(self.testSaisie("Entrer l'annee","int",1900,int(max)))
        mois = "{:02d}".format(self.testSaisie("Enter le mois","int",1,12))
        jour = "{:02d}".format(self.testSaisie("Enter le jour","int",1,31))
        return f"{jour}-{mois}-{annee}"
            
    def agree_number(self,msg='') -> int:
        phone = [70,75,76,77,78]
        while True:
            number = self.testSaisie(f"{msg}","int",700000000,790000000)
            if (number // 10000000) in phone:   #type:ignore
                return number #type:ignore
        
    def getIdClasse(self):
        niveau = ["L1","L2","L3","M1","M2"]
        all_filières = self.all_Other_Data["filiere"]
        
        while True:
            self.ligne('=', nombre= 50)
            print(f"{'Position':<10}{'Id':<10}{'Libelle'}")
            self.ligne('=', nombre= 50)
            i = 1
            for filiere in all_filières:
                print(f"{i:<10} {filiere['idF']:<10}{filiere['libelle']}")
                self.ligne(nombre=50)
                i += 1
            posFiliere = self.testSaisie("Entrez la position de la filière: ","int",1,len(all_filières))
            if posFiliere != None:  break
            else :self.clear()
            
        while True:
            print("\n1---- Licence 1\n2---- Licence 2\n3---- Licence 3\n4---- Master 1\n5---- Master 2\n")
            pos = self.testSaisie("Entrez l'id du niveau de l'étudiant: ","int",1,5)
            if niveau != None:  break
            else: self.clear()
        
        filiere = all_filières[posFiliere-1] # type: ignore
        niv = niveau[pos-1] #type:ignore
        classe_libelle = f"{niv}-{filiere['libelle']}"
    
        return classe_libelle
        
    def createOrSearchClasse(self, libelle:str) -> tuple | dict:
        all_classes = self.all_Other_Data["Classe"]
        fin, alphabet, cpt = len(libelle), '', 0
        
        for classe in all_classes:
            if classe.get("libelle")[0:fin] == libelle:
                cpt += 1
                if classe.get("effectif") <= DEFAULT_EFFECTIF: return (classe["idC"], classe) 
                
        if cpt > 1: alphabet = f" {ascii_uppercase[cpt-1]}"
        if cpt == 1:
            changement=f"libelle={libelle} A"
            self.sql.updateBase("Classe", changement,'libelle', libelle)
            self.sql.closeDB()
        
        return {
            "idC": len(all_classes) + 1,
            "libelle": f"{libelle}{alphabet}",
            "filière": libelle[3:], 
            "niveau": libelle[:2], 
            "effectif": 1,
            "chargé": "",
            "professeurs":'[]',
            "modules":'[]',
            "Annee_Scolaire":self.CurrentSchoolYear()
        }
            
    def controlMenu(self,opération:str, fonctionnalités:list):
        while True:
            self.ligne()
            self.ligne()
            self.menuUse(opération,fonctionnalités)
            choix = self.testSaisie(f"\n{push}"'Faites un choix: ',"int",1,len(fonctionnalités))
            if choix != None: return choix
            else: self.clear()
            
    def CurrentDate(self)->tuple:
        time = datetime.now()
        a, m, j = time.strftime('%Y'),time.strftime('%m'),time.strftime('%d')
        return (a,m,j)
    
    def CurrentSchoolYear(self)->str:
        currentDate=self.CurrentDate()
        if(currentDate[1]>=9):
            return f"{currentDate[0]}-{int(currentDate[0])+1}"
        else:return f"{int(currentDate[0])-1}-{currentDate[0]}"
        
        
        
class Classe:
    def __init__(self, idC:int, libelle:str, filière:str, niveau:str, effectif:int, chargéClasse:str, professeurs:list = [], étudiants:list = [], modules:list = []) -> None:
        self.idC = idC
        self.libelle = libelle
        self.filière = filière
        self.niveau = niveau
        self.effectif = effectif
        self.étudiants = étudiants
        self.modules = modules
        self.professeurs = professeurs
        self.chargé = chargéClasse

    #Setters
    def setId(self, newId) -> None: self.idC = newId

    def setLibelle(self, newlibelle) -> None:  self.libelle = newlibelle

    def setNiveau(self, newNiveau) -> None: self.niveau = newNiveau

    def setEffectif(self, newEffectif) -> None: self.effectif = newEffectif

    def setModule(self, newModule: str) -> None: self.modules.append(newModule)

    def setProfesseur(self, newProfesseur: str) -> None: self.professeurs.append(newProfesseur)

    def setChargé(self, newChargé: str) -> None: self.chargé = newChargé

    def setEtudiant(self, newEtudiant: str) -> None: self.étudiants.append(newEtudiant)

    #Getters
    def getId(self) -> int: return self.idC

    def getLibelle(self) -> str: return self.libelle

    def getNiveau(self) -> str: return self.niveau

    def getEffectif(self) -> int: return self.effectif

    def getModule(self) -> list: return self.modules

    def getProfesseur(self) -> list: return self.professeurs

    def getChargé(self) -> str: return self.chargé 

    def getEtudiant(self) -> list: return self.étudiants
    
###########################################################
################## Class de l'etudiant ####################
###########################################################

class Etudiant(User):
    def __init__(self, matricule: str, nom: str, prénom: str, dateNaissance:str, nationnalité:str, mail: str, téléphone: int, login: str, password: str, typeP:str, classe, notes,commentaires) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.dateNaissance = dateNaissance
        self.nationnalité = nationnalité
        self.usecase=DefaultUseCases()
        self.notes =self.usecase.getListe(notes)
        self.classe = classe #id de la classe
        self.commentaires = self.usecase.listTrans(commentaires,"chaine")
        self.charge=self.usecase.sql.getTables(f"SELECT chargé From Classe WHERE idC='{self.classe}' ")# type: ignore
        self.traitement()
    
    # def __init__(self) -> None:
    #     self.matricule="ISM2023/DK5-0425"
    #     self.idClasse=8
    #     self.usecase=DefaultUseCases()
    #     self.notes="[ ('Algorithme', ['17', 18]), ('Python', ['0', '0'])]"
    #     # self.charge=self.usecase.sql.getTables(f"SELECT chargé From Classe WHERE idC='{self.idClasse}' ") # type: ignore
    #     self.charge="ISM2023/staff2-0416"
    #     self.nom="THAPKANA"
    #     self.prénom="Kokou Godwin"
    #     self.commentaires=['', '02-05-2023---Bonjour votre bulletion du semestre 1 est disponible.Merci de passer le recupere']
    #     self.traitement()
        
        
    
    def traitement(self)->None:
        while True:
            match self.usecase.controlMenu("Menu General",ETUDIANT_USECASE["main"]):
                case 1:
                    self.usecase.showMsg("Mes notes",wait=False)
                    self.showNotes()
                case 2:
                    match self.usecase.controlMenu("Menu Commentaire",ETUDIANT_USECASE["commentaire"]):
                        case 1:
                            self.usecase.showMsg("Faire un commentaire/Reclamation",wait=False)
                            self.makeCommentaireCharge()
                        case 2:
                            self.usecase.showMsg("Mes Commentaires",wait=False)
                            self.showCommentaires()
                case 3:
                    break
     
    def showNotes(self)->None:
        attributs = ["Module","Note Evalution","Note Examen"]
        print(f"Etudiant: {self.nom} {self.prénom}")
        print(tabulate(headers=attributs,tabular_data=self.notes, tablefmt='double_outline'))  #type:ignore
        self.usecase.pause()
        
    def makeCommentaireCharge(self)->None:
        date = self.usecase.CurrentDate()
        listCom = list()
        commentaire = self.usecase.testSaisie("Saisir votre commentaire: ")
        chargeCom=self.usecase.sql.getTables(f"SELECT Commentaires FROM Chargé WHERE Matricule='{self.charge}' ")
        com = f"{self.nom} {self.prénom}_________{date[2]}-{date[1]}-{date[0]}---{commentaire}"
        
        
        listCom = self.usecase.listTrans(chargeCom[0][0],"chaine")
        listCom.append(com)
        changement = f'Commentaires="{listCom}" '
        self.usecase.sql.updateBase("Chargé",changement,"Matricule",self.charge)
        
    def showCommentaires(self)->None:
        print(tabulate(headers=["Commentaires"],tabular_data=[self.commentaires], tablefmt='double_outline'))  #type:ignore
        self.usecase.pause()
        
        
    
        
    #Setters
    def setDateNaissance(self, newDateNaissance: str) -> None: self.dateNaissance = newDateNaissance
        
    def setNationnalité(self, newNationnalité: str) -> None: self.nationnalité = newNationnalité
        
    def setNote(self, newNote) -> None: self.notes.append(newNote)
        
    def setClasse(self, newClasse) -> None: self.classe = newClasse
        
    #Getters
    def getDateNaissance(self) -> str: return self.dateNaissance
        
    def getNationnalité(self) -> str: return self.nationnalité
        
    def getNote(self) -> list: return self.notes

    def getClasse(self): return self.classe
###########################################################
############### Class de l'administrateur #################
class Filiere:
    def __init__(self, idN:int, libelle:str, classes:list = []) -> None:
        self.id = idN
        self.libelle = libelle
        self.classes = classes
    
    #Setters
    def setId(self, newId:int) -> None: self.id = newId
    
    def setLibelle(self, newLibelle:str) -> None: self.libelle = newLibelle
    
    def setClasse(self, newClasse:str) -> None: self.classes.append(newClasse)
        
    #Getters
    def getId(self) -> int: return self.id
    
    def getLibelle(self) -> str: return self.libelle
    
    def getClasse(self) -> list: return self.classes
       
###########################################################
#################### Class du module ######################
###########################################################

class Module:
    def __init__(self, idN:int, libelle:str, professeurs:list = [], classes:list = [], notes:list = []) -> None:
        self.id = idN
        self.libelle = libelle
        self.classes = classes
        self.professeurs = professeurs
    
    #Setters
    def setId(self, newId:int) -> None: self.id = newId
    
    def setLibelle(self, newLibelle:str) -> None: self.libelle = newLibelle
        
    def setClasse(self, newClasse) -> None: self.classes.append(newClasse)
    
    def setProfesseur(self, newProfesseur) -> None: self.professeurs.append(newProfesseur)
        
    #Getters
    def getId(self) -> int: return self.id
    
    def getLibelle(self) -> str: return self.libelle
    
    def getClasse(self) -> list: return self.classes

    def getProfesseurs(self) -> list: return self.professeurs
###########################################################
#################### Class du niveau ######################
###########################################################
class Niveau:
    def __init__(self, idN:int, libelle:str, classes:list = []) -> None:
        self.id = idN
        self.libelle = libelle
        self.classes = classes
    
    #Setters
    def setId(self, newId:int) -> None: self.id = newId
    
    def setLibelle(self, newLibelle:str) -> None: self.libelle = newLibelle
        
    def setNiveau(self, newClasse:str) -> None: self.classes.append(newClasse)
        
    #Getters
    def getId(self) -> int: return self.id
    
    def getLibelle(self) -> str: return self.libelle
    
    def getClasse(self) -> list: return self.classes
        
###########################################################
############### Class de l'administrateur #################
###########################################################
class Note:
    def __init__(self, libelle:str, etudiant:Etudiant) -> None:
        self.libelle = libelle
        self.etudiant = etudiant
    
    #Setters
    def setLibelle(self, newLibelle:str) -> None: self.libelle = newLibelle
        
    def setEtudiant(self, newEtudiant:Etudiant) -> None: self.etudiant = newEtudiant
    
    #Getters
    def getLibelle(self) -> str: return self.libelle
        
    def getEtudiant(self) -> Etudiant: return self.etudiant   

###########################################################
############### Class de l'administrateur #################
###########################################################


class Partenaire:
    def __init__(self,id:int,libelle:str, mail: str, téléphone: int, login: str, password: str, typeP: str) -> None:
        self.usecase = DefaultUseCases()
        self.all_Etudiants = self.usecase.loadStudentsFolder()
        self.traitement()
        
    # def __init__(self) -> None:
    #     self.usecase = DefaultUseCases()
    #     self.all_Etudiants = self.usecase.loadStudentsFolder()
    #     self.traitement()
    
    def traitement(self):
        while True:
            match self.usecase.controlMenu("Menu général", PARTENAIRE_USECASES["main"]): 
                case 1:
                    self.consult()
                    self.usecase.pause()
                case 2:
                    break
                
    def consult(self):
        while True:
            self.usecase.showMsg("Menu de consultation", wait=False)
            etuMat = self.usecase.testSaisie("Entrez le matricule de l'étudiant : ")
            etu = self.usecase.sql.getTables(f"SELECT * FROM Etudiants WHERE Matricule = '{etuMat}' ")
            if etu != []:
                break
        
        dossierEtudiant = self.all_Etudiants.get(f"{etuMat}")
        data = [[année["Année-Scolaire"]]  for année in dossierEtudiant] #type:ignore ["2020-2021", "2021-2022", "2022-2023"]
        while True:
            self.usecase.showMsg("Menu consultation", wait = False)
            print(f"Nom : {etu[0][1]}")
            print(f"Prénom : {etu[0][2]}")
            print("-"*50)
            print(tabulate(headers=["Année-Scolaire"], tabular_data=data))
            année = self.usecase.testSaisie("Entrez l'année scolaire : ")#2021-2022
            if [année] in data:
                break
        data_Année = dossierEtudiant[data.index([année])]#type:ignore
        self.usecase.showMsg(f"Dossier de l'année {année}", wait = False)
        print(f"Nom     : {etu[0][1]}")
        print(f"Prénom  : {etu[0][2]}")
        print(f"Niveau  : {data_Année.get('niveau')}")#type:ignore
        print(f"filière : {data_Année.get('filière')}")#type:ignore
        print(f"Classe  : {data_Année.get('Classe')}")#type:ignore
        print("="*50)
        attributs = ["Modules", "Note Evaluation", "Note Examen"]
        sessions = self.usecase.dicoTrans(data_Année.get("Période")) #[(NomSession, DicoModules), (NomSession, DicoModules)]
        session_1 = sessions[0]
        session_2 = sessions[1]
        data_session_1 = [[module, notes[0], notes[1]] for module, notes in session_1[1].items()]
        data_session_2 = [[module, notes[0], notes[1]] for module, notes in session_2[1].items()]
        print(f"Notes de {session_1[0]}")
        print("-"*50)
        print(tabulate(headers=attributs, tabular_data=data_session_1, tablefmt='double_outline'))
        
        print(f"\nNotes de {session_2[0]}")
        print("-"*50)
        print(tabulate(headers=attributs, tabular_data=data_session_2, tablefmt='double_outline'))
        print('\n')
        
        
    # Setters
    def setEtudiant(self, newfichierEtudiant:str) -> None:self.etudiants = newfichierEtudiant
    
    # Getters
    def getEtudiants(self) -> str: return self.etudiants
        
###########################################################
################## Class du professeur ####################
###########################################################
class Professeur:
    def __init__(self, idP:int, nom:str, prénom:str, mail:str, téléphone:int, classes:list = [], modules:list = []) -> None:
        self.idP = idP
        self.nom = nom
        self.prénom = prénom
        self.mail = mail
        self.téléphone = téléphone
        self.modules = modules
        self.classes = classes
    
    #Setters
    def setId(self, newId:str) -> None: self.matricule = newId
    
    def setNom(self, newNom:str) -> None: self.nom = newNom
        
    def setPrénom(self, newPrénom:str) -> None: self.prénom = newPrénom
        
    def setMail(self, newMail:str) -> None: self.mail = newMail
        
    def setTéléphone(self, newTéléphone:int) -> None: self.téléphone = newTéléphone
        
    def setLogin(self, newLogin:str) -> None: self.login = newLogin
        
    def setPassword(self, newPassword:str) -> None: self.password = newPassword
        
    def setClasse(self, newClasse:str) -> None: self.classes.append(newClasse)

    def setModule(self, newModule: Module) -> None: self.modules.append(newModule)
        
    #Getters
    def getId(self) -> str:return self.matricule 
    
    def getNom(self) -> str:return self.nom    
    
    def getPrénom(self) -> str:return self.prénom 
          
    def getMail(self) -> str:return self.mail    
     
    def getTéléphone(self) -> int:return self.téléphone 

    def getClasse(self) -> list:return self.classes

    def getModule(self) -> list:return self.modules 

###########################################################
############### Class de la responsable admin##############
###########################################################


class ResponsableAdmin(User):
    # def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str) -> None:
    #     super().__init__(matricule, nom, prénom, mail, téléphone, login, password, "ResponsableAdmin")
    #     self.usecase = DefaultUseCases()
    #     self.sql = MySql()
    #     self.traitement()
    
    def __init__(self) -> None:
        self.usecase = DefaultUseCases()
        self.sql = MySql()
        self.traitement()
         
    def traitement(self):
        while True:
             match self.usecase.controlMenu("Menu général", RP_USECASES["main"]):
                case 1:
                    # print(tabulate(headers=RP_USECASES["liste"], tabular_data=[[1,2,3,4,5,6]], tablefmt='double_outline', colalign="center", stralign="center", numalign='center'))
                    match self.usecase.controlMenu("Menu général", RP_USECASES["add"]):
                        case 1:
                            self.usecase.showMsg("Ajout d'un professeur",wait=False)
                            self.ajoutProf()
                        case 2:
                            self.usecase.showMsg("Ajout d'un modules",wait=False)
                            self.ajoutModule()
                        case 3:
                            self.usecase.showMsg("Ajout d'une filière",wait=False)
                            self.ajoutFiliere()
                case 2:
                    match self.usecase.controlMenu("Menu général", RP_USECASES["liste"]):
                        case 1:
                            self.usecase.showMsg("Liste des professeurs",wait=False)
                            self.usecase.lister("Professeurs")
                            self.usecase.pause()
                        case 2:
                            self.usecase.showMsg("Liste des modules",wait=False)
                            self.usecase.lister("Modules")
                            self.usecase.pause()
                        
                        case 3:
                            self.usecase.showMsg("Liste des filière",wait=False)
                            self.usecase.lister("Filiere")
                            self.usecase.pause()
                        case 4:
                            self.usecase.showMsg("Liste des Chargés",wait=False)
                            self.usecase.lister("Chargés")
                            self.usecase.pause()
                        case 5:
                            self.usecase.showMsg("Liste des niveaux",wait=False)
                            self.usecase.lister("Niveau")
                            self.usecase.pause()
                        case 6:
                            self.filtrer()
                            pass
                        case 7: pass
                case 4:
                    match self.usecase.controlMenu("Menu général", RP_USECASES["more"]):
                        case 1:
                            self.setChargeClasse()
                        case 2:
                            self.usecase.showMsg("Moyenne des Etudiant et de la Classe",wait=False)
                            self.showMoyenne()
                        case 3:
                            match(self.usecase.controlMenu("Menu Statistique",RP_USECASES["stat"])):
                                case 1:
                                    self.usecase.showMsg("Statique",wait=False)
                                    pass
                                case 2:
                                    pass
                        case 4:
                            break
                case 5:
                    break
                
                
    #Fonctionnalité de la responsable
    def filtrer(self) :
        match self.usecase.controlMenu("Menu général", RP_USECASES["filtre"]):#type:ignore
            case 1:
                filtre, valeur = "Tous", ""
                pass
            case 2:
                filtre = "Filiere"
                while True:
                    self.usecase.showMsg("Liste des filière",wait=False)
                    self.usecase.lister("Filiere")
                    filiere = (self.usecase.testSaisie("Entrez le libelle de la filiere : ")).upper() # type: ignore
                    if (filiere,) in self.usecase.sql.getTables("SELECT libelle FROM filiere"):#[(""),("")]
                        valeur = filiere
                        break
            case 3:
                filtre = "Libelle"
                while True:
                    self.usecase.showMsg("Liste des Classes",wait=False)
                    self.usecase.lister("Classes")
                    classe = self.usecase.testSaisie("Entrez le libelle de la classe : ")
                    if (classe,) in self.usecase.sql.getTables("SELECT Libelle FROM Classe"):#[("",),("")]
                        valeur = classe
                        break
            case 4:
                filtre = "Niveau"
                while True:
                    self.usecase.showMsg("Liste des niveaux",wait=False)
                    self.usecase.lister("Niveau")
                    niveau = self.usecase.testSaisie("Entrez le libelle du niveau : ")
                    if niveau in NIVEAUX.values():
                        valeur = str(niveau)[0]+ str(niveau)[-1]
                        break
            case 5:
                filtre = "Nationnalité"
                allNat = set(self.usecase.sql.getTables("SELECT Nationnalité FROM Etudiants"))
                while True:
                    nat = [[i[0]] for i in allNat ]
                    self.usecase.showMsg("Liste des nationnalités",wait=False)#[("Togolaise")]
                    print(tabulate(headers=["Nationnalité"], tabular_data=nat))
                    niveau = self.usecase.testSaisie("Entrez le libelle du niveau : ")
                    if [niveau] in nat:
                        valeur = niveau
                        break
        
        self.usecase.showMsg("Liste des etudiants",wait=False)
        self.usecase.lister("Etudiants",filtre, valeur)#type:ignore
        self.usecase.pause()
        
    def setChargeClasse(self):
        listeClasse = list()
        while True:
            self.usecase.showMsg("Attribuer une classe a un chargé",wait=False)
            self.usecase.lister("Chargés")
            matChargé = self.usecase.testSaisie("Entrez le matricule du chargé : ")
            chargé = self.usecase.sql.getTables(f"SELECT * FROM Chargé WHERE Matricule = '{matChargé}' ") #[(Matricule, nom, prenom),]chargé[0][0]
            if chargé != []:
                break
            else:
                self.usecase.showMsg("Le matricule du chargé le correspond pas !", clear=True)
        
        while True:
            self.usecase.showMsg("Attribuer une classe a un chargé",wait=False)
            self.usecase.lister("Classes")
            idClasse = self.usecase.testSaisie("Entrez l'id de la classe : ", 'int',min=1, max=1000)
            classe = self.usecase.sql.getTables(f"SELECT * FROM Classe WHERE idC = {idClasse} ") #[(informations_chargé),]
            if classe != []:
                listeClasse.append(idClasse)
                if self.usecase.question("Voulez vous ajouter une autre classe") == 'oui':
                    continue
                else: break
            else:
                self.usecase.showMsg("L'id de la classe ne correspond pas !", clear=True)
        self.usecase.showMsg("Attribuer une classe a un chargé",wait=False)
        if self.usecase.question("Voulez vous enregistrer les modifications") == 'oui':
            chargéClasses = self.usecase.listTrans(chargé[0][8])
            classeAyChargé = list()            
            for idC in listeClasse:
                classe = self.usecase.sql.getTables(f"SELECT libelle, chargé FROM Classe WHERE idC = {idC}")
                if classe[0][1]  == "":
                    if idC not in chargéClasses:
                        chargéClasses.append(idC)
                        self.usecase.sql.updateBase("Classe", f"chargé = '{matChargé}'", "idC", idC)
                else:
                    classeAyChargé.append(classe[0][0])
                    
            if len(listeClasse) != len(chargéClasses):
                classes = ", ".join(classeAyChargé)
                self.usecase.showMsg(f"Les classes : {classes} ont déjà un chargé(e) !", clear=False, wait=False)
                self.usecase.pause()
            self.usecase.sql.updateBase("Chargé", f"classes = '{str(chargéClasses)}' ", "Matricule", matChargé)
            self.usecase.showMsg(f"La liste des classes a bien été attribuer à {chargé[0][1]}")
        
    def ajoutFiliere(self):
        filiere = dict()
        filiere["IdF"] = self.usecase.sql.getTables("SELECT count(idF) FROM filiere")[0][0] + 1
        filiere["Libelle"] = self.usecase.testSaisie("Entrez le libelle de la filiere : ").upper() # type: ignore
        while True:
            choix = self.usecase.question("Confirmer l'enregistrement")
            if choix == "oui":
                if self.checkFiliere(filiere["Libelle"]) == []: 
                    self.usecase.sql.insert("filiere",self.addNewFiliere(filiere), self.usecase.sql.TABLES_OTHERS["filiere"])
                    self.usecase.sql = MySql()
                    self.usecase.showMsg("Filiere ajouté avec success")  
                    break
                else:
                    self.usecase.showMsg("La filiere existe déjà dans la base")    
            break
        
    def ajoutModule(self):
        mod = dict()
        mod["IdM"] = self.usecase.sql.getTables("SELECT count(idM) FROM Modules")[0][0] + 1
        mod["Libelle"] = self.usecase.testSaisie("Entrez le libelle du module : ").title() # type: ignore
        mod["coefficient"]=self.usecase.testSaisie("Entrer le coefficient du module:","int",min=1)
        mod["credit"]=self.usecase.testSaisie("Entrer le credit du module:","int",min=1)
        while True:
            choix = self.usecase.question("Confirmer l'enregistrement")
            if choix == "oui":
                if self.checkMod(mod["Libelle"]) == []: 
                    self.usecase.sql.insert("Modules",self.addNewMod(mod), self.usecase.sql.TABLES_OTHERS["Modules"])
                    self.usecase.sql = MySql()
                    self.usecase.showMsg("Modules ajouté avec success")  
                    break
                else:
                    self.usecase.showMsg("Le modules existe déjà dans la base")    
            break
    
    def ajoutProf(self):
        prof = dict()
        prof["IdP"] = self.usecase.sql.getTables("SELECT count(idP) FROM professeurs;")[0][0] + 1
        prof["Nom"] = self.usecase.testSaisie("Entrez le nom du professeur : ").upper() # type: ignore
        prof["Prenom"] = self.usecase.testSaisie("Entrez le prénom du professeur : ").title() # type: ignore
        prof["Mail"] = self.usecase.testSaisie("Entrez le mail de l'établissement : ").lower() # type: ignore
        prof["Telephone"] = self.usecase.agree_number("Entrez le téléphone de l'établissement : ")
        prof["Classes"] = []
        prof["Modules"] = []
        print('')
        while True:
            self.usecase.lister("Classes")
            resul = self.usecase.sql.getTables("SELECT count(idC) FROM Classe")[0][0]
            if resul != 0:
                idC = self.usecase.testSaisie("Entrez l'id de la classe à attribuer au prof : ", 'int', 1, resul) 
                prof["Classes"].append(idC)
                if self.usecase.question("Voulez vous ajouter une autre classe ?") != "oui":
                    break
            else: break
                    
        while True:
            result = self.usecase.sql.getTables("SELECT count(idM) FROM Modules")[0][0]
            print(result)
            if result != 0:
                self.usecase.lister("Modules")
                idM = self.usecase.testSaisie("Entrez l'id de du module du prof : ", 'int', 1, result) 
                prof["Modules"].append(idM)
                if self.usecase.question("Voulez vous ajouter un autre module ?") != "oui":
                    break
            else: break
            
        while True:
            choix = self.usecase.question("Confirmer l'enregistrement")
            if choix == "oui":
                for idM in prof['Modules']:
                    listeProfs = self.usecase.listTrans(self.usecase.sql.getTables(f"SELECT professeurs FROM Modules WHERE idM = {idM}")[0][0])
                    listeProfs.append(prof['IdP'])
                    print(f"professeurs = {str(listeProfs)}", "idM", idM)
                    self.usecase.sql.updateBase("Modules", f"professeurs = '{str(listeProfs)}'", "idM", idM)
                    
                if self.checkProf(prof["Telephone"]) == []: 
                    self.usecase.sql.insert("professeurs",self.addNewProf(prof), self.usecase.sql.TABLES_OTHERS["professeurs"])
                    self.usecase.sql = MySql()
                    self.usecase.showMsg("Professeur ajouté avec success")  
                    break
                else:
                    self.usecase.showMsg("Le prof existe déjà dans la base")    
            break
    
    def addNewProf(self, newProf: dict):
        return (
            newProf.get("IdP"),
            newProf.get("Nom"),
            newProf.get("Prenom"),
            newProf.get("Mail"),
            newProf.get("Telephone"),
            str(newProf.get("Classes")),
            str(newProf.get("Modules"))
        )
        
    def addNewMod(self, newMod: dict):
        return (
            newMod.get("IdM"),
            newMod.get("Libelle"),
            "[]",
            "[]",
            newMod.get("coefficient"),
            newMod.get("credit")
        )
    
    def addNewFiliere(self, newFiliere: dict):
        return (
            newFiliere.get("IdF"),
            newFiliere.get("Libelle"),
            "[]"
        )
    
    def ajouterComponent(self, libelle:str, componentData:list):
        for component in componentData:
            if component.get('Libelle') == libelle:
                return (len(componentData)+1, libelle)
        return False

    def checkProf(self, téléphone: int) -> list:
        return self.usecase.sql.getTables(f"SELECT * FROM professeurs WHERE Telephone = {téléphone}")
    
    def checkMod(self, libelle: str) -> list:
        return self.usecase.sql.getTables(f'SELECT * FROM Modules WHERE libelle = "{libelle}"')
    
    def checkFiliere(self, libelle: str) -> list:
        return self.usecase.sql.getTables(f'SELECT * FROM filiere WHERE libelle = "{libelle}"')
    
    def listerComponent(self, data:list):
        print("="*TAILLE_SCREEN)
        print(f"{'ID':<10}{'Libelle':<15}")
        print("="*TAILLE_SCREEN)

        for compo in data:
            print(f"{compo.get('Id'):<10}{compo.get('Libelle'):<15}")
            print("-"*TAILLE_SCREEN)
    
    def listerProf(self, data:list):
        print("="*TAILLE_SCREEN)
        print(f"{'Matricule':<10}{'Nom':<15}{'Prénom':<20}{'Mail':<20}{'Téléphone':<10}{'Modules':<10}{'Classes':<10}")
        print("="*TAILLE_SCREEN)
        
        for prof in data:
            print(f"{prof.get('Matricule'):<10}{prof.get('Nom'):<15}{prof.get('Prénom'):<20}{prof.get('Mail'):<20}{prof.get('Téléphone'):<10}{prof.get('Modules'):<20}{prof.get('Classes'):<20}")
            print("-"*TAILLE_SCREEN)
    
    def listerChargés(self,data:list):
        print("="*TAILLE_SCREEN)
        print(f"{'Matricule':<10}{'Nom':<15}{'Prénom':<20}{'Mail':<20}{'Téléphone':<10}{'Classes':<10}")
        print("="*TAILLE_SCREEN)
        
        for chargé in data:
            print(f"{chargé.get('Matricule'):<10}{chargé.get('Nom'):<15}{chargé.get('Prénom'):<20}{chargé.get('Mail'):<20}{chargé.get('Téléphone'):<10}{chargé.get('Classes'):<20}")
            print("-"*TAILLE_SCREEN)
    
    def listerClasses(self,data:list):
        print("="*TAILLE_SCREEN)
        print(f"{'IdClasse':<10}{'Libelle':<15}{'Filiere':<20}{'Niveau':<20}{'Effectif':<10}{'Chargé':<10}")
        print("="*TAILLE_SCREEN)
        
        for classe in data:
            print(f"{classe.get('idC'):<10}{classe.get('Libelle'):<15}{classe.get('Filiere'):<20}{classe.get('Niveau'):<20}{classe.get('Effectif'):<10}{classe.get('Chargé'):<20}")
            print("-"*TAILLE_SCREEN)
     
    def ajoutClasseChargé(self,data:dict):
        chargés = data.get('Chargés')
        classes = data.get('Classes')
        
        self.listerClasses(classes) #type:ignore
        idClasse = self.usecase.DoWhile("idC",classes) #type:ignore
        
        while True:
            self.listerChargés(chargés) #type:ignore
            matricule = self.usecase.DoWhile("Matricule",chargés) #type:ignore
            ClassesChargé = self.usecase.getComponentByKey("Matricule",matricule,chargés).get("Classes")

            if(idClasse not in ClassesChargé):break #type:ignore 
            else:print("La classe y est deja")
            
        newValue = str(ClassesChargé.append(idClasse))   #type:ignore 
        changement = f"Classes={newValue}"
        changeCharge = f"Chargé={matricule}"
        self.sql.updateBase("Chargés",changement,"Matricule",matricule)
        self.sql.updateBase("Classes",changeCharge,"idC",idClasse)                

    def showMoyenne(self)->None:
        libelle=self.usecase.testSaisie("Entrer le libelle de la classe ")
        etudiants=self.usecase.sql.getTables(f"SELECT etudiants From Classe where Libelle='{libelle}' ")
        listMoyenne=list()
        moyenneClasse=0.0
        for matEtu in self.usecase.listTrans(etudiants[0][0],"chaine"):
            etu=self.usecase.sql.getTables(f"SELECT Nom,Prenom,Notes From Etudiants where Matricule='{matEtu}'")
            Notes=self.usecase.getListe(etu[0][2])
            moyenne=0.0
            dico=list()
            coef=0
            for note in Notes:
                module=self.usecase.sql.getTables(f"SELECT coefficient,credit from Modules where libelle='{note[0]}' ")
                totalEval=int(note[1])*0.4
                totalExam=int(note[2])*0.6
                moyenneMod=(totalEval+totalExam)*module[0][0]
                coef+=module[0][0]
                moyenne+=moyenneMod
            dico.append(f"{etu[0][0]} {etu[0][1]}")
            dico.append(moyenne/coef)
            listMoyenne.append(dico)
            moyenneClasse+=(moyenne/coef)
        
        attributs=["Etudiant","Moyenne"]
        print(tabulate(headers=attributs,tabular_data=listMoyenne,tablefmt='double_outline'))
        print("-"*100)
        moy=moyenneClasse/len(self.usecase.listTrans(etudiants[0][0],'chaine'))
        text=f"Moyenne de {libelle}{' '*80}{moy}"
        print(tabulate(tabular_data=[[text]],tablefmt='double_outline'))
        self.usecase.pause()
        


class Application:
    def __init__(self) -> None:
        self.useCases = DefaultUseCases()
        self.user_connect = self.useCases.accueil()
        self.user_active=self.useCases.createUser(self.user_connect)
        
if __name__ == "__main__":
    # Application()
    # Admin()
    ResponsableAdmin()
    # Chargé()
    # Partenaire()
    # Etudiant()