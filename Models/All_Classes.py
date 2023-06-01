from http.client import SWITCHING_PROTOCOLS
import os
import json
import sqlite3
from datetime import datetime
from random import randint
from string import ascii_uppercase
from time import sleep

import colorama as color
from colorama import init
from pyfiglet import figlet_format
from tabulate import tabulate 
from Models.Config import *
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


class MySql: 
    def __init__(self) -> None:
        #Connexion à la base de donnée
        self.base = sqlite3.connect(BASE_FILE)
        #Initialisation du curseur de connexion
        self.curseur = self.base.cursor()
        
        self.TABLES_USER = {
            "Admin": ["Matricule", "Nom", "Prenom", "Mail", "Telephone", "Login","Password","TypeP"],
            "Chargé": ["Matricule", "Nom", "Prenom", "Mail", "Telephone", "Login", "Password", "TypeP",  "Classes"],
            "Etudiants": [ "Matricule", "Nom", "Prenom", "DateNaissance", "Nationnalité", "Mail", "Telephone", "Login", "Password", "TypeP","IdClasse", "Notes"],
            "partenaires": ["Id", "Libelle", "Mail", "Telephone", "Login", "Password", "TypeP"],
            "responsableAdmin": ["Matricule", "Nom", "Prenom", "Mail", "Telephone","Login", "Password", "TypeP"]
        }
        
        self.TABLES_OTHERS = {
            "filiere": ["idF","libelle","classes"], 
            "Modules": ["idM", "libelle", "classes", "professeurs","coefficient","credit"],
            "professeurs": ["idP", "Nom", "Prenom", "mail", "Telephone", "modules", "Classes"], 
            "Classe": ["idC", 'libelle', 'Filiere', 'niveau','effectif', 'chargé','professeurs', 'modules', 'etudiants', "Annee_Scolaire"]
        }
        
        self.TABLES = {
            "Etudiants":"Matricule text, Nom text, Prenom text, DateNaissance text, Nationnalité text, Mail text, Telephone number, Login text, PassWord text, TypeP text, IdClasse number, Notes text", 
            "Chargé":"Matricule text, Nom text, Prenom text, mail text, Telephone number, Login text, Password text, TypeP text,  Classes text", 
            "Admin":"Matricule text, Nom text, Prenom text, mail text, Telephone number, Login text, Password text, TypeP text", 
            "Filiere":"idF number, libelle text, classes text", 
            "Modules":"idM number, libelle text, classes text, professeurs text, notes text, coefficient integer, credit integer", 
            "partenaires":"id integer primary key autoincrement, libelle varchar(150), mail varchar(255), Telephone integer, Login varchar(255), Password varchar(150), TypeP varchar(150)", 
            "professeurs":"idP number, Nom text, Prenom text, mail text, Telephone number, Classes text, modules text", 
            "ResponsableAdmin":"Matricule text, Nom text, Prenom text, mail text, Telephone number, Login text, Password text, TypeP text",
            "Classe":"idC number, Libelle text, Filiere text, niveau number, effectif number, chargé text, professeurs text, modules text, etudiants text, Annee_Scolaire text"
        }
        
        self.initTables(self.TABLES)
        # INSERT INTO Admin (Matricule, Nom, Prenom, mail, Telephone, Login, Password, TypeP)VALUES ();
        if self.getTables("SELECT count(matricule) FROM Admin")[0][0] == 0:
            # Définition de l'administrateur par défaut...
            self.insert("Admin", ("ISM2023/staff01-0001", "SANGARE", "Mohamed", "mohamed.sangare@groupism.sn", 781077144, "mohamed.sangare@groupism.sn", 'passer@123', 'Admin'), self.TABLES_USER["Admin"])
            
            #Insertion de quelques filières dans la base...
            filiere = ["MAIE", "MOSIEF", "GLRS", "ETSE", "IAGE", "TTL", "CPD", "CDSD"]
            for i in range(len(filiere)):
                self.insert("Filiere", (i, filiere[i], "[]"), self.TABLES_OTHERS['filiere'])
            
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
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, "Admin")
        self.usecase = DefaultUseCases()
        self.traitement()
        
    def traitement(self):
        while True:
            match self.usecase.controlMenu("Menu général", ADMIN_USECASES["main"]):
                case 1:
                    while True:
                        match  self.usecase.controlMenu("Ajout d'un nouvel utilisateur", ADMIN_USECASES["add"]):
                            case 1:
                                self.usecase.showMsg("Menu d'ajout d'un étudiants",wait=False)
                                self.ajoutEtudiant()
                            case 2:
                                self.usecase.showMsg("Liste des chargés")
                                self.ajoutChargé()
                            case 3:
                                self.usecase.showMsg("Liste des responsables administratifs")
                                self.ajoutRP()
                            case 4:
                                self.usecase.showMsg("Liste des partenaires")
                                self.ajoutPartenaire()
                            case 5:  break
                case 2:
                    while True:
                        match  self.usecase.controlMenu("Liste des utilisateurs", ADMIN_USECASES["liste"]):
                            case 1:
                                self.usecase.showMsg("Liste des étudiants", wait=False)
                                self.usecase.lister("Etudiants")
                                self.usecase.pause()
                                pass
                            case 2:
                                self.usecase.showMsg("Liste des chargés", wait=False)
                                self.usecase.lister("Chargés")
                                self.usecase.pause()
                                pass
                            case 3:
                                self.usecase.showMsg("Liste des responsables", wait=False)
                                
                                self.usecase.lister("ResponsablesAdmin")
                                self.usecase.pause()
                                pass
                            case 4:
                                self.usecase.showMsg("Liste des partenaires", wait=False)
                                
                                self.usecase.lister("Partenaires")
                                self.usecase.pause()
                                pass
                            case 5:
                                break
                    pass
                case 3:
                    while True:
                        match  self.usecase.controlMenu("Suppression d'un Responsable", ADMIN_USECASES["delete"]):
                            case 1:
                                self.usecase.showMsg("Suppression du responsable Administratif",wait=False)
                                self.deleteRP()
                            case 2:
                                break
                    pass
                case 4:
                    self.usecase.quitter()
                    self.user_connect = self.usecase.accueil()
                    self.user_active = self.usecase.createUser(self.user_connect)
                    break
        pass
        
    def deleteRP(self):
        while True:
            RPs=self.usecase.sql.getTables("SELECT * FROM responsableAdmin ")
            print(tabulate(headers=["Matricule","Nom","Prenom"],tabular_data=[[rp[0],rp[1],rp[2]]for rp in RPs],tablefmt="double_outline"))
            matricule=self.usecase.testSaisie("Entrer le matricule du Responsable: ")
            for resp in RPs:
                if resp[0]==matricule:
                    self.usecase.sql.getTables(f"delete FROM responsableAdmin where Matricule='{matricule}' ")
                    self.usecase.showMsg("Responsable Adminitratif supprimé avec succes!")
                    return None
            self.usecase.showMsg("Le matricule saisi ne coorespond à aucun Responsable")
            
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
        date = self.usecase.CurrentDate()
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
                data = self.usecase.loadStudentsFolder(FOLDER_CHARGES_FILE)
                data[f"{charge['Matricule']}"] = {"Commentaire": {}}
                self.usecase.updateFile(FOLDER_CHARGES_FILE,data)
                self.usecase.showMsg("Chargés ajouté avec succes")  
                break
            break
             
    def ajoutEtudiant(self):
        date = self.usecase.CurrentDate()
        etudiant = dict()
        matricule = f"ISM{date[0]}/DK{len(self.usecase.sql.datas['Etudiants'])+1}-{date[1]}{date[2]}"
        classe = self.usecase.createOrSearchClasse(self.usecase.getIdClasse())
        self.usecase.showMsg("Menu d'ajout d'un etudiant", wait=False)
        self.usecase.centerTexte(f"{BLUE}Renseigner les informations de l'étudiant")
        print("")
        etudiant = {
            "Matricule":matricule,
            "Nom":self.usecase.testSaisie("Nom de l'Etudiant : ").upper(), # type: ignore
            "Prénom":self.usecase.testSaisie("Prenom de l'Etudiant : ").title(), # type: ignore
            "DateNaissance":self.usecase.ver_date("INFORMATIONS SUR LA DATE DE NAISSANCE"),
            "Nationnalité":self.usecase.testSaisie(f"\n{push}DONNEES SUPPLEMENTAIRES\n{push}Nationnalité: ").capitalize(), # type: ignore
            "Telephone":self.usecase.agree_number("Numéro de téléphone ")
        }
        etudiant["Mail"] = self.setUserMail(etudiant)
        while True:
            self.usecase.showMsg("Menu d'jaout d'un étudiant", wait= False)
            self.usecase.ligneMenu(4, TAILLE_SCREEN//3, 'haut')
            self.usecase.showMenu([["Matricule",(TAILLE_SCREEN//3), 'center'], ['Nom (1)',(TAILLE_SCREEN//3), 'center'], ["Prénom (2)",(TAILLE_SCREEN//3), 'center']])
            self.usecase.showMenu([[etudiant["Matricule"],(TAILLE_SCREEN//3), 'center'], [etudiant["Nom"],(TAILLE_SCREEN//3), 'center'], [etudiant["Prénom"],(TAILLE_SCREEN//3), 'center']])
            self.usecase.ligneMenu(4, TAILLE_SCREEN//3, 'milieu')
            self.usecase.showMenu([["Mail (3)",(TAILLE_SCREEN//2)-1, 'center'], ['Nationnalité (4)',(TAILLE_SCREEN//2)-1, 'center']])
            self.usecase.showMenu([[etudiant["Mail"],(TAILLE_SCREEN//2)-1, 'center'], [etudiant["Nationnalité"],(TAILLE_SCREEN//2)-1, 'center']])
            self.usecase.ligneMenu(3, TAILLE_SCREEN//2 - 1 , 'milieu')
            self.usecase.showMenu([["Date Naissance (5)",(TAILLE_SCREEN//3), 'center'], ['Téléphone (6)',(TAILLE_SCREEN//3), 'center'], ["Classe (7)",(TAILLE_SCREEN//3), 'center']])
            self.usecase.showMenu([[etudiant["DateNaissance"],(TAILLE_SCREEN//3), 'center'], [etudiant['Telephone'],(TAILLE_SCREEN//3), 'center'], [classe[1]["libelle"] if type(classe) == tuple else classe["libelle"] ,(TAILLE_SCREEN//3), 'center']]) # type: ignore
            self.usecase.ligneMenu(4, TAILLE_SCREEN//3, 'bas')
            print("")
            choix = self.usecase.question("Confirmer l'enregistrement")
            if choix =="oui":
                data = self.usecase.loadStudentsFolder()
                charge = self.usecase.loadStudentsFolder(FOLDER_CHARGES_FILE)
                if type(classe) == tuple:
                    session = self.usecase.setSessions(classe[1]['niveau'])
                    data[f"{etudiant['Matricule']}"] = [
                        {
                            "Année-Scolaire": self.usecase.CurrentSchoolYear(),
                            "niveau": classe[1]["niveau"],
                            "filière": classe[1]["Filiere"],
                            "Classe": classe[1]["libelle"],
                            "Période": {
                                session[0]: {},
                                session[1]: {}
                            },
                            "Commentaire": []
                        }
                    ]
                    if classe[1]["chargé"] != "":
                        charge[f"{classe[1]['chargé']}"]["Commentaire"][f"{etudiant['Matricule']}"] = [] #type: ignore
                        self.usecase.updateFile(FOLDER_CHARGES_FILE,charge)
                    etudiant["IdClasse"] = classe[0]
                    listeMatricules=self.usecase.listTrans(classe[1]["etudiants"])
                    listeMatricules.append(matricule)
                    changement=f"effectif={int(classe[1]['effectif']) + 1},etudiants=\"{str(listeMatricules)}\""
                    self.usecase.sql.updateBase("Classe", changement,"idC",classe[0])
                elif type(classe) == dict: 
                    session = self.usecase.setSessions(classe['niveau'])
                    data[f"{etudiant['Matricule']}"] = [
                        {
                            "Année-Scolaire": self.usecase.CurrentSchoolYear(),
                            "niveau": classe["niveau"],
                            "filière": classe["filière"],
                            "Classe": classe["libelle"],
                            "Période": {
                                session[0]: {},
                                session[1]: {}
                            },
                            "Commentaire": []
                        }
                    ]
                    etudiant["IdClasse"] = classe["idC"]
                    classe["etudiants"] = f"{[matricule]}"
                    self.usecase.sql.insert('Classe',tuple(classe.values()), self.usecase.sql.TABLES_OTHERS["Classe"])
                    
                self.usecase.sql.insert("Etudiants",self.user(etudiant), self.usecase.sql.TABLES_USER["Etudiants"])
                self.usecase.sql = MySql()
                
                self.usecase.updateFile(FOLDER_FILE,data)
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
        self.usecase = DefaultUseCases()
        self.classeChargé = self.usecase.sql.getTables(f"SELECT * FROM Classe WHERE chargé='{self.matricule}'")
        self.traitement()
        
    def modifyEtudiant(self):
        while True:
            self.usecase.showMsg("Menu de modification d'un étudiant", wait= False)
            chargéClasses = self.usecase.sql.getTables(f"SELECT idC, Libelle FROM Classe WHERE chargé = \"{self.matricule}\" ")
            self.usecase.centerTexte(tabulate(headers=["Id classe", "Libelle"], tabular_data= chargéClasses, tablefmt= "double_outline"))
            print("")
            idC = self.usecase.testSaisie("Entrez l'id de la classe ou (-1) pour quitter: ", 'int', min= -1)
            if idC != -1:
                cpt = 0
                for classe in chargéClasses:
                    if classe[0] == idC:
                        cpt = 1
                        self.usecase.showMsg(f"Liste des étudiants de la classe: {classe[1]}", wait= False)
                        etudiants = self.usecase.sql.getTables(f"SELECT Matricule, Nom, Prenom FROM Etudiants WHERE idClasse = {idC}")
                        if etudiants != []:
                            print(tabulate(headers=["Matricule", "Nom", "Prénom"], tabular_data=etudiants, tablefmt="double_outline"))
                            print("")
                            matricule = self.usecase.testSaisie("Entrez le matricule de l'étudiant à modifier ou (-1) pour quitter : ", nbreChar = 2)
                            
                            if matricule != '-1':
                                for etu in etudiants:
                                    if etu[0] == matricule:
                                        while True:
                                            self.usecase.showMsg(f"Information de {etu[1]} {etu[2]}", wait=False)
                                            chargé = self.usecase.showStudentInfo(matricule) # type: ignore
                                            print("")
                                            choix = self.usecase.testSaisie("Entrez le numéro pour modifier l'élément ou (-1) pour quitter : ", 'int', min= -1)
                                            if choix in [1,2,3,4,5,6,7]:
                                                match choix:
                                                    case 1:
                                                        self.usecase.showMsg("Modification du Nom", wait= False)
                                                        print("")
                                                        self.usecase.centerTexte(f"Ancien Nom: {BLUE} {chargé[choix]}") #type: ignore
                                                        new = self.usecase.testSaisie("Entrez le nouveau nom : ")
                                                        self.usecase.modifyStudentAttribute("Nom", new.upper(), matricule) #type: ignore
                                                        mail = f"{chargé[3]}".replace(chargé[choix].lower(), new.lower())#type: ignore
                                                        self.usecase.modifyStudentAttribute("Mail", mail, matricule) #type: ignore
                                                        self.usecase.showMsg("le Nom a bien été changé !", wait= False)
                                                        print("")
                                                        self.usecase.showMsg(f"Information de {etu[1]} {etu[2]}", wait=False)
                                                        self.usecase.showStudentInfo(matricule) # type: ignore
                                                        
                                                        print("")
                                                        if self.usecase.question("Voulez-vous modifier un autre élément") == 'non':
                                                            return None
                                                    case 2:
                                                        self.usecase.showMsg("Modification du Prénom", wait= False)
                                                        print("")
                                                        self.usecase.centerTexte(f"Ancien prénom: {BLUE} {std[choix]}") #type: ignore
                                                        new = self.usecase.testSaisie("Entrez le nouveau prénom :")
                                                        mail = f"{std[3]}".replace(std[choix].replace(" ", '-').lower(), new.replace(" ", '-').lower())#type: ignore
                                                        self.usecase.modifyStudentAttribute("Prenom", new.title(), matricule) #type: ignore
                                                        self.usecase.modifyStudentAttribute("Mail", mail, matricule) #type: ignore
                                                        self.usecase.showMsg("le prénom a bien été changé !", wait= False)
                                                        print("")
                                                        self.usecase.showMsg(f"Information de {etu[1]} {etu[2]}", wait=False)
                                                        self.usecase.showStudentInfo(matricule) # type: ignore
                                                        
                                                        print("")
                                                        if self.usecase.question("Voulez-vous modifier un autre élément") == 'non':
                                                            return None
                                                    case 3:
                                                        self.usecase.showMsg("Modification du Mail", wait= False)
                                                        print("")
                                                        self.usecase.centerTexte(f"Ancien mail: {BLUE} {std[choix]}") #type: ignore
                                                        new = self.usecase.testSaisie("Entrez le nouveau mail :")
                                                        self.usecase.modifyStudentAttribute("Mail", new.lower(), matricule) #type: ignore
                                                        self.usecase.showMsg("le mail a bien été changé !", wait= False)
                                                        print("")
                                                        self.usecase.showMsg(f"Information de {etu[1]} {etu[2]}", wait=False)
                                                        self.usecase.showStudentInfo(matricule) # type: ignore
                                                        
                                                        print("")
                                                        if self.usecase.question("Voulez-vous modifier un autre élément") == 'non':
                                                            return None
                                                    case 4:
                                                        self.usecase.showMsg("Modification de la nationnalité", wait= False)
                                                        print("")
                                                        self.usecase.centerTexte(f"Ancienne nationnalité: {BLUE} {std[choix]}") #type: ignore
                                                        new = self.usecase.testSaisie("Entrez la nouvelle nationnalité :")
                                                        self.usecase.modifyStudentAttribute("Nationnalité", new.title(), matricule) #type: ignore
                                                        self.usecase.showMsg("la nationnalité a bien été changé !", wait= False)
                                                        print("")
                                                        self.usecase.showMsg(f"Information de {etu[1]} {etu[2]}", wait=False)
                                                        self.usecase.showStudentInfo(matricule) # type: ignore
                                                        
                                                        print("")
                                                        if self.usecase.question("Voulez-vous modifier un autre élément") == 'non':
                                                            return None
                                                    case 5:
                                                        self.usecase.showMsg("Modification de la date de naissance", wait= False)
                                                        print("")
                                                        self.usecase.centerTexte(f"Ancienne date de naissance: {BLUE} {std[choix]}") #type: ignore
                                                        new = self.usecase.ver_date("INFORMATIONS SUR LA DATE DE NAISSANCE")
                                                        self.usecase.modifyStudentAttribute("DateNaissance", new, matricule) #type: ignore
                                                        self.usecase.showMsg("la nationnalité a bien été changé !", wait= False)
                                                        print("")
                                                        self.usecase.showMsg(f"Information de {etu[1]} {etu[2]}", wait=False)
                                                        self.usecase.showStudentInfo(matricule) # type: ignore
                                                        
                                                        print("")
                                                        if self.usecase.question("Voulez-vous modifier un autre élément") == 'non':
                                                            return None
                                                    case 6:
                                                        self.usecase.showMsg("Modification du numéro de téléphone", wait= False)
                                                        print("")
                                                        self.usecase.centerTexte(f"Ancienne téléphone: {BLUE} {std[choix]}") #type: ignore
                                                        new = self.usecase.agree_number("Entrez le nouveau téléphone : ")
                                                        self.usecase.modifyStudentAttribute("Telephone", new, matricule) #type: ignore
                                                        self.usecase.showMsg("le téléphone a bien été changé !", wait= False)
                                                        print("")
                                                        self.usecase.showMsg(f"Information de {etu[1]} {etu[2]}", wait=False)
                                                        self.usecase.showStudentInfo(matricule) # type: ignore
                                                        
                                                        print("")
                                                        if self.usecase.question("Voulez-vous modifier un autre élément") == 'non':
                                                            return None
                                                    case 7:
                                                        while True:
                                                            self.usecase.showMsg("Modification de la classe", wait= False)
                                                            print("")
                                                            self.usecase.centerTexte(f"Ancienne classe: {BLUE} {std[choix]}") #type: ignore
                                                            self.usecase.lister("Classes")
                                                            print("")
                                                            idC = self.usecase.testSaisie("Entrez l'id de la classe : ", 'int')
                                                            if self.usecase.sql.getTables(f"SELECT Libelle FROM Classe WHERE idC = {idC}") != []:
                                                                self.usecase.modifyStudentAttribute("idClasse", idC, matricule) #type: ignore
                                                                self.usecase.showMsg("la classe a bien été changé !", wait= False)
                                                                print("")
                                                                self.usecase.showMsg(f"Information de {etu[1]} {etu[2]}", wait=False)
                                                                self.usecase.showStudentInfo(matricule) # type: ignore
                                                                
                                                                print("")
                                                                if self.usecase.question("Voulez-vous modifier un autre élément") == 'non':
                                                                    return None
                                                                else: break
                                                        
                                            elif choix == -1:
                                                return None
                                            else:
                                                self.usecase.showMsg("Le numéro n'est pas valide !", wait= False, clear= False)
                                                self.usecase.pause()
                            else:
                                return None    
                        else:
                            self.usecase.showMsg("Il n'y pas d'étudiant dans cette classe !", wait=False)
                            self.usecase.pause()
                if cpt == 0:
                    self.usecase.showMsg("L'id ne correspond à aucune classe !", wait= False)
                    self.usecase.pause()
            else:
                return None
    
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
                            case 3: 
                                self.modifyEtudiant()
                            case 4: break
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
                            case 2: break
                case 6:
                    self.usecase.showMsg("Suppression d'etudiant",wait=False)
                    self.deleteEtudiant()
                case 7:
                    self.usecase.quitter()
                    self.user_connect = self.usecase.accueil()
                    self.user_active = self.usecase.createUser(self.user_connect)
                    break
    
    def deleteEtudiant(self):
        while True:
            listes=list()
            liste2=list()
            for classEtu in self.classeChargé:
                listeMat = self.usecase.listTrans(classEtu[8],"chaine")
                print(listeMat)
                if listeMat != ['']:
                    for etu in self.usecase.listTrans(classEtu[8],"chaine"):
                        etudiant=self.usecase.sql.getTables(f"select Matricule,Nom,Prenom from Etudiants where Matricule='{etu.strip()}' ")[0]
                        listes.append([etu,etudiant[1],etudiant[2],classEtu[2]])
                        liste2.append(etudiant[0])
            print(tabulate(headers=["Matricule", "Nom", "Prenom", "Classe"],tabular_data= listes, tablefmt='double_outline'))

            matricule=self.usecase.testSaisie("Entrez le matricule de l'etudiant:")
            if matricule in liste2:
                idClasse=self.usecase.sql.getTables(f"select IdClasse from Etudiants where Matricule='{matricule}' ")[0]
                self.usecase.sql.getTables(f"Delete from Etudiants where Matricule='{matricule}'")
                et=self.usecase.sql.getTables(f"select effectif,etudiants from Classe where idC={idClasse[0]} ")[0]
                listMat=self.usecase.listTrans(et[1],"chaine")
                listMat.remove(matricule)
                changement1=f'effectif={et[0]-1},etudiants="{listMat}"  '
                self.usecase.sql.updateBase("Classe",changement1,"idC",idClasse[0])
                self.usecase.showMsg("Etudiant supprimé avec succes")
                return None
            self.usecase.showMsg("Le matricule saisi ne correspond à aucun Etudiant")
        
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
            
        self.usecase.showMsg("Liste des étudiants", wait=False)
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
            dicoList=dict()
            if noteList==[]:
                dicoList=self.usecase.convertion(noteList)
            dicoList[f"{module}"]=list()
            dicoList[f"{module}"].append(noteEvaluation)
            dicoList[f"{module}"].append(noteExam)
            print(self.usecase.dicoTrans(dicoList))
            if noteList==[]:
                changement=f'Notes="{self.usecase.dicoTrans(dicoList)}" '
            else:
                noteList.append(self.usecase.dicoTrans(dicoList))
                changement=f'Notes="{noteList}" '
            self.usecase.sql.updateBase("Etudiants",changement,"Matricule",matricule)
            if self.usecase.question("Voulez vous ajouter les notes d'un autre module") == 'oui':
                continue
            else:
                break
            
    def InitNotesClasse(self)->None:
        while True:
            self.usecase.showMsg("Liste des classes", wait=False)
            self.usecase.lister("Classes")

            libelle = self.usecase.testSaisie("Entrez le libelle de la classe : ").upper() # type: ignore
            module = self.usecase.testSaisie("Entrez le libelle du module : ").title() # type: ignore
            classe=self.usecase.sql.getTables(f"SELECT * FROM Classe WHERE Libelle='{libelle}' ")
            etudiants=self.usecase.listTrans(classe[0][8],"chaine")
            for etu in etudiants:
                noteEvaluation = self.usecase.testSaisie("Entrez la note d'evaluation : ","int",0,20)
                noteExam = self.usecase.testSaisie("Entrez la note d'examen : ","int",0,20)
                notes = self.usecase.sql.getTables(f"SELECT Notes FROM Etudiants WHERE Matricule='{etu}' ")
                print(notes)
                noteList = self.usecase.listTrans(notes[0][0])
                dicoList = self.usecase.convertion(noteList)
                dicoList[f"{module}"] = list()
                dicoList[f"{module}"].append(noteEvaluation)
                dicoList[f"{module}"].append(noteExam)
                changement = f'Notes="{self.usecase.dicoTrans(dicoList)}" '
                self.usecase.sql.updateBase("Etudiants",changement,"Matricule",etu)
            if self.usecase.question("Voulez vous ajouter les notes d'un autre module") == 'oui':
                continue
            else: break
        
    def showNotesEtu(self)->None:
        
        while True:
            classes = self.usecase.sql.getTables(f'SELECT Classes FROM Chargé WHERE Matricule = \"{self.matricule}\"')[0]
            da =  self.usecase.sql.getTables(f"SELECT Matricule, Nom, Prenom FROM Etudiants Where idClasse IN ({classes[0][1:-1]})")
            self.usecase.centerTexte(tabulate(headers=['Matricule', "Nom", "Prénom"], tabular_data=da, tablefmt="double_outline"))
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
        all_Data = self.usecase.loadStudentsFolder(FOLDER_FILE)
        all_Charges_Data = self.usecase.loadStudentsFolder(FOLDER_CHARGES_FILE)
        
        entite = self.usecase.testSaisie("Enter le destinataire du commentaire[Classe|Etudiant]: ").capitalize() #type:ignore
        date = self.usecase.CurrentDate()
        if(entite == "Classe"):
            libelle = self.usecase.testSaisie("Entrer le libelle de la classe: ")
            classe = self.usecase.sql.getTables(f"SELECT * FROM Classe WHERE Libelle='{libelle}' ")
            charge_commentaire = all_Charges_Data.get(f"{self.matricule}")["Commentaire"][f"{classe[0][0]}"] #type: ignore
            
            print(classe[0][8])
            self.usecase.pause()
            commentaire = self.usecase.testSaisie("Saisir votre commentaire: ")
            date = self.usecase.CurrentDate()
            listCom = list()
            newSend = {'Date': f"{date[2]}-{date[1]}-{date[0]}", 'Heure': date[3], 'Auteur': self.matricule, 'Commentaire': commentaire}
            for matricule in self.usecase.listTrans(classe[0][8],"chaine"):
                student_commentaire = all_Data.get(f"{matricule}")[-1]["Commentaire"] #type: ignore
                student_commentaire.append(newSend)
                
            charge_commentaire.append(newSend)
            self.usecase.updateFile(FOLDER_CHARGES_FILE, all_Charges_Data)
            self.usecase.updateFile(FOLDER_FILE, all_Data)
                # etudiant = self.usecase.sql.getTables(f"SELECT Commentaires FROM Etudiants WHERE Matricule='{matricule}' ")
                
                # com = f"{date[2]}-{date[1]}-{date[0]}---{commentaire}"
                # listCom = self.usecase.listTrans(etudiant[0][0],"chaine")
                # listCom.append(com) #02-05-2023  ('02',)
                # changement = f'Commentaires="{listCom}" '
                # self.usecase.sql.updateBase("Etudiants",changement,"Matricule",matricule)
            self.usecase.pause()
                
        elif(entite == "Etudiant"):
            matricule = self.usecase.testSaisie("Saisir le matricule de l'etudiant: ")
            self.usecase.commentaires(str(matricule), self.matricule, self.matricule)
            
            # commentaire = self.usecase.testSaisie("Saisir votre commentaire: ")
            # etudiant = self.usecase.sql.getTables(f"SELECT Commentaires FROM Etudiants WHERE Matricule='{matricule}' ")
            # com = f"{date[2]}-{date[1]}-{date[0]}---{commentaire}"
            # listCom = self.usecase.listTrans(etudiant[0][0],"chaine")
            # listCom.append(com) #02-05-2023  ('02',)
            # changement = f'Commentaires="{listCom}" '
            # self.usecase.sql.updateBase("Etudiants",changement,"Matricule",matricule)
            
    def ShowCommentaires(self)->None:
        self.usecase.loadStudentsFolder()
        pass
        # commentaires = self.usecase.sql.getTables(f"SELECT Commentaires from Chargé where Matricule='{self.matricule}'")
        
###########################################################
################### Quelsques classes #####################
###########################################################
class DefaultUseCases:
    def __init__(self) -> None:
        self.sql = MySql()
        self.all_User_Data = self.sql.datas #Données des utilisateurs.
        self.all_Other_Data = self.sql.component #Données des filières et autres infos
        self.students_data = self.loadStudentsFolder()
        self.students_discuss = self.loadStudentsFolder(FOLDER_FILE) 
    
    def consultStudentFolder(self, matricule: str, année_scolaire: str, session: int)-> list[list]:
        """ ### Cett méthode permet de consulter la liste de note d'un étudiant selon l'année_scolaire et la session.
        - ##### Arguments:
            - `matricule (str)`: C'est le matricule de l'étudiant
            - `année_scolaire (str)`: année de fréquentation de l'étudiant
            - `session (int)`: la session de note que vous voulez voir (Session 1, 2, 3 etc...)

        - ##### Retourne:
            - Une liste des notes de l'année_scolaire et de la session
        """
        matricule = matricule.strip()
        student_data = self.sql.getTables(f"SELECT * FROM Etudiants WHERE Matricule = '{matricule}' ")
        if student_data != []:
            student_folder = self.students_data.get(f"{matricule}")
            school_years = [data["Année-Scolaire"]  for data in student_folder] #type:ignore ["2020-2021", "2021-2022", "2022-2023"]
            if année_scolaire in school_years:
                data_of_year = student_folder[school_years.index(année_scolaire)] #type: ignore
                session_marks = self.dicoTrans(data_of_year.get("Période")) # [(NomSession, DicoModules), (NomSession, DicoModules)]            
                return [[module, notes[0], notes[1]] for module, notes in session_marks[session][1].items()]
        return [] 
    
        
    def calculMoy(self, notes: list) -> tuple[float, int]:
        """
        ### Cette méthode calcul la moyenne d'une liste de module qu'on lui passe. 
        - Arguments:
            - notes (list): Il prend e paramètre une liste qui contient une liste 
            qui contient le module, le coefficient du module et son crédit
        - Returns:
            - _type_: tuple(0: moyenne, 1: longueur)
            - Retourne un tuple de la moyenne de l'étudiant et la longueur du
        module qui a le plus de caractères...
        """
        student_points, somCredit, somCoef, longueur = 0, 0, 0, []
        for note in notes:
            module = self.sql.getTables(f"SELECT libelle, coefficient, credit FROM modules WHERE libelle = '{note[0]}' ")[0]
            moyenne_module = (note[1]*(0.4) + note[2]*(0.6))*module[1]
            longueur.append(len(note[0]))
            somCoef += module[1]
            somCredit += module[2]
            student_points += moyenne_module
        student_mark = student_points / somCoef
        return (student_mark, max(longueur) + 27)
    
    def showData(self, headers: list, data: list, showIndex=False) -> str:
        """### Cette méthode 
        - ##### Arguments:
            - `headers (list)`: ex: ["Id", "Nom", "Prénom], Une liste qui contient les entetes du tableau
            - `data (list)`: ex: [[1, 'TAM', 'Rock'], [2, 'NDEYE', 'Binta'], Une liste qui contient des listes de données selon chaque
            entete qui seront mis dans le tableau
        - ##### Retourne:
            - `Un tableau (str)`: retourne un tableau des données que vous lui passez en parametre
        """
        return tabulate(headers = headers, tabular_data=data, tablefmt='double_outline', showindex=showIndex)
    
    
    def report(self, matricule:str):
        student = self.sql.getTables(f"SELECT * FROM Etudiants WHERE Matricule = '{matricule}' ")
        if student != []:
            dossierEtudiant = self.students_data.get(f"{matricule}")
            dat = [année["Année-Scolaire"]  for année in dossierEtudiant] #type:ignore ["2020-2021", "2021-2022", "2022-2023"]
            dat.append("Menu général")
            while True:
                date = int(self.controlMenu("Liste des années_scolaire", dat))
                if 0 < date and date  <= len(dat)-1: 
                    periode = [i[0] for i in self.dicoTrans(dossierEtudiant[dat.index(dat[date-1])].get("Période"))]#type: ignore #[(NomSession, DicoModules), (NomSession, DicoModules)]
                    periode.append("Menu général")
                    while True:
                        choix = int(self.controlMenu("Liste des sessions", periode))
                        if  date > 0 and choix <= 2:
                            annee = dat[date-1] #type: ignore
                            attributs = ["Modules", "Note Evaluation", "Note Examen"]
                            data_session = self.consultStudentFolder(matricule, annee, choix-1)
                            moySession_1 = self.calculMoy(data_session)  # type: ignore
                            print(f"\nNotes de {periode[choix-1]}\n{'-'*50}\n{self.showData(attributs,data_session)}")  # type: ignore
                            print(f"╔{'═'*(moySession_1[1] + 11)}╗\n║ Moyenne: {SUCCESS}{str(moySession_1[0])[:5]:>{moySession_1[1]}}{WHITE} ║\n╚{'═'*(moySession_1[1] + 11)}╝\n")
                            self.pause()
                        elif choix == 3: break
                elif date == len(dat): break
                
    def showTableau(self, titre: str, donne):
        self.ligneMenu(3,(TAILLE_SCREEN//2)-2, 'haut')
        self.showMenu([['Position', (TAILLE_SCREEN//2)-2,'center'],[titre, (TAILLE_SCREEN//2)-2,'center']])
        self.ligneMenu(3,(TAILLE_SCREEN//2)-2, 'milieu')
        i = 1
        for element in donne:
            self.showMenu([[i, (TAILLE_SCREEN//2)-2,'center'],[element, (TAILLE_SCREEN//2)-2,'center']])
            if i == len(donne):
                self.ligneMenu(3,(TAILLE_SCREEN//2)-2, 'bas')
                break
            self.ligneMenu(3,(TAILLE_SCREEN//2)-2, 'milieu')
            i += 1
        print("\n")
        
    def setSessions(self, niveau):
        num = int(niveau[-1])*2
        return (f'Session {num-1}', f'Session {num}')
        
    def modifyStudentAttribute(self, key: str, newValue, matricule: str):
        self.sql.updateBase("Etudiants", f"{key} = \"{newValue}\"", "Matricule", matricule)
    
    def showStudentInfo(self, matricule: str) :
        std = self.sql.getTables(f"SELECT Matricule, Nom, Prenom, Mail, Nationnalité, DateNaissance,  Telephone, idClasse FROM Etudiants WHERE Matricule = \"{matricule}\" ")
        if std != []:
            classe = self.sql.getTables(f"SELECT Libelle FROM Classe WHERE idC = {std[0][7]}")[0][0]
            self.ligneMenu(4, TAILLE_SCREEN//3, 'haut')
            self.showMenu([["Matricule",(TAILLE_SCREEN//3), 'center'], ['Nom (1)',(TAILLE_SCREEN//3), 'center'], ["Prénom (2)",(TAILLE_SCREEN//3), 'center']])
            self.showMenu([[std[0][0],(TAILLE_SCREEN//3), 'center'], [std[0][1],(TAILLE_SCREEN//3), 'center'], [std[0][2],(TAILLE_SCREEN//3), 'center']])
            self.ligneMenu(4, TAILLE_SCREEN//3, 'milieu')
            self.showMenu([["Mail (3)",(TAILLE_SCREEN//2)-1, 'center'], ['Nationnalité (4)',(TAILLE_SCREEN//2)-1, 'center']])
            self.showMenu([[std[0][3],(TAILLE_SCREEN//2)-1, 'center'], [std[0][4],(TAILLE_SCREEN//2)-1, 'center']])
            self.ligneMenu(3, TAILLE_SCREEN//2 - 1 , 'milieu')
            self.showMenu([["Date Naissance (5)",(TAILLE_SCREEN//3), 'center'], ['Téléphone (6)',(TAILLE_SCREEN//3), 'center'], ["Classe (7)",(TAILLE_SCREEN//3), 'center']])
            self.showMenu([[std[0][5],(TAILLE_SCREEN//3), 'center'], [std[0][6],(TAILLE_SCREEN//3), 'center'], [classe,(TAILLE_SCREEN//3), 'center']])
            self.ligneMenu(4, TAILLE_SCREEN//3, 'bas')
            return std[0]
        
    def showChargeInfo(self, matricule: str) :
        """Matricule, Nom, Prenom, Mail, Telephone, classes

        Args:
            matricule (str): _description_

        Returns:
            _type_: _description_
        """
        std = self.sql.getTables(f"SELECT Matricule, Nom, Prenom, Mail, Telephone, classes FROM Chargé WHERE Matricule = \"{matricule}\" ")
        if std != []:
            classes = self.sql.getTables(f"SELECT Libelle FROM Classe WHERE idC IN ({std[0][5][1:-1]})")
            self.ligneMenu(4, TAILLE_SCREEN//3, 'haut')
            self.showMenu([["Matricule",(TAILLE_SCREEN//3), 'center'], ['Nom (1)',(TAILLE_SCREEN//3), 'center'], ["Prénom (2)",(TAILLE_SCREEN//3), 'center']])
            self.showMenu([[std[0][0],(TAILLE_SCREEN//3), 'center'], [std[0][1],(TAILLE_SCREEN//3), 'center'], [std[0][2],(TAILLE_SCREEN//3), 'center']])
            self.ligneMenu(4, TAILLE_SCREEN//3, 'milieu')
            self.showMenu([["Mail (3)",(TAILLE_SCREEN//2)-1, 'center'], ['Téléphone (4)',(TAILLE_SCREEN//2)-1, 'center']])
            self.showMenu([[std[0][3],(TAILLE_SCREEN//2)-1, 'center'], [std[0][4],(TAILLE_SCREEN//2)-1, 'center']])
            self.ligneMenu(3, TAILLE_SCREEN//2 - 1 , 'milieu')
            self.showMenu([[" Liste des classes",(TAILLE_SCREEN-2), 'center']])
            self.showMenu([[" \t".join([classe[0] for classe in classes]),(TAILLE_SCREEN-(4*len(classes))-2), 'center']])
            self.ligneMenu(2, TAILLE_SCREEN-2, 'bas')
            return std[0]
    
    def commentaires(self, etudiantMatricule:str, chargeMatricule: str, matriculeAuteur: str)->None:
        while True:
            self.showMsg("Mes commentaires", wait=False)
            all_Data = self.loadStudentsFolder(FOLDER_FILE)
            all_Charges_Data = self.loadStudentsFolder(FOLDER_CHARGES_FILE)
            charge_commentaire = all_Charges_Data.get(f"{chargeMatricule}")["Commentaire"][f"{etudiantMatricule}"] #type: ignore
            student_commentaire = all_Data.get(f"{etudiantMatricule}")[-1]["Commentaire"] #type: ignore
            
            self.ligneMenu(2, TAILLE_SCREEN, 'haut')
            print(f"| {BLUE}{'Commentaires':^{TAILLE_SCREEN-3}} |")
            self.ligneMenu(2, TAILLE_SCREEN, 'milieu')
            i, show = 0, True
            for commentaire in student_commentaire:
                if i == 0: print(f"| {YELLOW}{commentaire['Date']:^{TAILLE_SCREEN-3}} |")
                if student_commentaire[i-1]["Date"] != student_commentaire[i]["Date"] and i != 0:
                    print(f"| {YELLOW}{commentaire['Date']:^{TAILLE_SCREEN-3}} |")
                i += 1
                if commentaire["Auteur"] == matriculeAuteur:
                    self.chatRight(commentaire["Commentaire"])
                    print(f"| {commentaire['Heure']:>{TAILLE_SCREEN-3}} |")
                else:    
                    self.chatLeft(commentaire["Commentaire"])
                    print(f"| {commentaire['Heure']:<{TAILLE_SCREEN-3}} |")
                if i == len(student_commentaire):
                    self.ligneMenu(2, TAILLE_SCREEN, 'bas')

            # Envoie d'un nouveau commentaire
            commentaire = input("Entrez un nouveau commentaire (ou -1 pour quitter): \n")
            if commentaire != '-1':
                date = self.CurrentDate()
                newSend = {'Date': f"{date[2]}-{date[1]}-{date[0]}", 'Heure': date[3], 'Auteur': matriculeAuteur, 'Commentaire': commentaire}
                student_commentaire.append(newSend)
                charge_commentaire.append(newSend)
                
                self.updateFile(FOLDER_CHARGES_FILE, all_Charges_Data)
                self.updateFile(FOLDER_FILE, all_Data)
            else:
                break

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
            self.centerTexte(tabulate(headers=attributs,tabular_data= data, tablefmt='double_outline'))#type:ignore
        else:
            self.showMsg("Vous n'avez pas de données !", clear=False)
    
    def loadStudentsFolder(self, fileName=FOLDER_FILE) -> dict:
        with open(fileName, encoding="UTF-8") as f:
            return json.load(f)
        
    def updateFile(self, fileName, data) :
        with open(fileName, 'w', encoding="UTF-8") as f:
            json.dump(data, f)
        
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
    
    def menuUse(self,titre, fonctions:list):
        self.clear()
        self.opération(titre)
        numChoix, tailleCollonne, nbreFonction = 1, len(max(fonctions)), len(fonctions)
        m = tailleCollonne*nbreFonction
        l = TAILLE_SCREEN-m
        if l > 0:tailleCollonne += (l // nbreFonction)
        else:tailleCollonne = TAILLE_SCREEN // nbreFonction
        if nbreFonction <= 3:
            options = list()
            choices = list()
            for useCase in  fonctions:
                options.append([useCase,(TAILLE_SCREEN//3), 'center'])
                choices.append([numChoix, (TAILLE_SCREEN//3), 'center'])
                numChoix += 1
                
            self.ligneMenu(numChoix,(TAILLE_SCREEN//3),'haut')
            self.showMenu(options)
            self.showMenu(choices)
            self.ligneMenu(numChoix,(TAILLE_SCREEN//3),'bas')
        else:
            cpt, n = 1, 0
            # numChoix, tailleCollonne = 1, len(max(fonctions))
            options, choices, mainOptions, mainChoices = list(), list(), list(), list()
            for useCase in  fonctions:
                options.append([useCase,(TAILLE_SCREEN//3), 'center'])
                choices.append([numChoix, (TAILLE_SCREEN//3), 'center'])
                numChoix += 1
                if cpt == 3:
                    n += 1
                    mainOptions.append(options)
                    mainChoices.append(choices)
                    options, choices = list(), list()
                    cpt = 0
                cpt += 1
            x = None
            if len(mainOptions)*3 != nbreFonction:
                x = nbreFonction - n*3
                for i in range(len(options)):
                    options[i][1] = (TAILLE_SCREEN//(x)-(1 if x%2== 0 else 2))
                    choices[i][1] = (TAILLE_SCREEN//(x)-(1 if x%2== 0 else 2))
                mainOptions.append(options)
                mainChoices.append(choices)
            
            cpt = 0
            for i in range(len(mainOptions)):
                if i == 0: self.ligneMenu(4,(TAILLE_SCREEN//3),'haut')
                elif i < len(mainOptions) and i != 0: self.ligneMenu(4,(TAILLE_SCREEN//3),'milieu')   
                self.showMenu(mainOptions[i])
                self.showMenu(mainChoices[i])
                if i == len(mainOptions) - 1:
                    if x != None: self.ligneMenu(x+1,(TAILLE_SCREEN//(x)-(1 if x%2 == 0 else 2)),'bas')
                    else: self.ligneMenu(4,(TAILLE_SCREEN//3),'bas')
    
    # def menuUseOld(self,titre, fonctionnalités:list, Fermer=True):
    #     self.clear()
    #     self.opération(titre)
    #     options = []
    #     choices = []
    #     numChoix, tailleCollonne, nbreFonction = 1, len(max(fonctionnalités)) + 10, len(fonctionnalités)
    #     m = tailleCollonne*nbreFonction
    #     l = TAILLE_SCREEN-m
    #     # t = (TAILLE_SCREEN//nbreFonction)
    #     if l > 0:tailleCollonne += (l // nbreFonction)
    #     else:tailleCollonne = TAILLE_SCREEN // nbreFonction
    #     for useCase in  fonctionnalités:
    #         options.append([useCase,tailleCollonne, 'center'])
    #         choices.append([numChoix, tailleCollonne, 'center'])
    #         numChoix += 1
    #     self.ligneMenu(numChoix,tailleCollonne,'haut')
    #     self.showMenu(options)
    #     self.showMenu(choices)
    #     if Fermer:self.ligneMenu(numChoix,tailleCollonne,'bas')
        
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
            sleep(randint(1, 50)/1000)
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
         
    def testSaisie(self, message:str, catégorie: str = 'str', min: int = 0, max: int = 100, nbreChar: int = 3)-> int|str:
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
            case "Admin": return Admin(user["Matricule"],user["Nom"],user["Prenom"],user["Mail"],user["Telephone"],user["Login"],user["Password"])
            case "ResponsableAdmin": return ResponsableAdmin(user["Matricule"],user["Nom"],user["Prenom"],user["Mail"],user["Telephone"],user["Login"],user["Password"])
            case "Chargé": return Chargé(user["Matricule"],user["Nom"],user["Prenom"],user["Mail"],user["Telephone"],user["Login"],user["Password"],user["TypeP"])
            case "Etudiant": return Etudiant(user["Matricule"],user["Nom"],user["Prenom"],user["DateNaissance"],user["Nationnalité"],user["Mail"],user["Telephone"],user["Login"],user["Password"],user["TypeP"],user["IdClasse"],user["Notes"])
            case "Partenaire": return Partenaire(user["Id"],user["Libelle"],user["Mail"],user["Telephone"],user["Login"],user["Password"],user["TypeP"])
            
    def test(self,message,text=""):
        if(text!=""): print(text)
        while True:
            element=input(message)
            if(element!=""): return element
                
    def ver_date(self, message:str="")-> str:
        # self.centerTexte(message)
        print(f"\n{push}{message}")
        print(f"{push}{BLUE}{'='*(len(message))}")
        max = self.CurrentDate()[0]
        annee = "{:04d}".format(self.testSaisie("Entrer l'annee : ","int",1900,int(max)))
        mois = "{:02d}".format(self.testSaisie("Enter le mois : ","int",1,12))
        jour = "{:02d}".format(self.testSaisie("Enter le jour : ","int",1,31))
        return f"{jour}-{mois}-{annee}"
    
    def centerTexte(self, message: str):
        texte = message.split("\n")
        for line in texte:
            print(f"{line:^{TAILLE_SCREEN}}")
        
    def agree_number(self,msg='') -> int:
        phone = [70,75,76,77,78]
        while True:
            number = self.testSaisie(f"{msg} : ","int",700000000,790000000)
            if (number // 10000000) in phone:   #type:ignore
                return number #type:ignore
        
    def getIdClasse(self)-> str:
        niveau = ["L1","L2","L3","M1","M2"]
        all_filières = self.all_Other_Data["filiere"]
        while True:
            self.showMsg("Liste des filieres", wait=False)
            self.showTableau("Libelle", [filiere['libelle'] for filiere in all_filières])
            posFiliere = self.testSaisie("Entrez la position de la filière: ","int",1,len(all_filières))
            if posFiliere != None:  break
            else :self.clear()
            
        while True:
            self.showMsg("Liste des filieres", wait=False)
            self.showTableau("Libelle", ["Licence 1", "Licence 2", "Licence 3", 'Master 1', 'Master 2'])
            pos = self.testSaisie("Entrez la position du niveau de l'étudiant: ","int",1,5)
            if pos in [1,2,3,4,5]:  break
            else: self.clear()
        
        filiere = all_filières[posFiliere-1] # type: ignore
        niv = niveau[pos-1] #type:ignore
        classe_libelle = f"{niv}-{filiere['libelle']}"
    
        return classe_libelle
        
    def createOrSearchClasse(self, libelle:str) -> tuple[int,dict] | dict:
        all_classes = self.all_Other_Data["Classe"]
        fin, alphabet, cpt = len(libelle), '', 0
        
        for classe in all_classes:
            if classe.get("libelle")[0:fin] == libelle:
                cpt += 1
                if int(classe.get("effectif")) <= DEFAULT_EFFECTIF: return (classe["idC"], classe) 
                
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
            "Etudiants": "[]",
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
            
    def CurrentDate(self) -> tuple[str, str, str, str]:
        time = datetime.now()
        a, m, j = time.strftime('%Y'),time.strftime('%m'),time.strftime('%d')
        return (a,m,j, f"{str(time).split(' ')[1][:5]}")
    
    def CurrentSchoolYear(self) -> str:
        currentDate = self.CurrentDate()
        if(int(currentDate[1])>=9):
            return f"{currentDate[0]}-{int(currentDate[0])+1}"
        else:return f"{int(currentDate[0])-1}-{currentDate[0]}"

    def chatLeft(self, texte: str):
        text = texte.split(" ")
        ligne = ''
        if len(texte) >= CHAT_LENGHT:
            for mot in text:
                ligne += mot + ' '
                if len(ligne) >= CHAT_LENGHT:
                    print(f"| {BLUE}{ligne:<{TAILLE_SCREEN-3}} |")
                    ligne = ""
        else: print(f"| {BLUE}{texte:<{TAILLE_SCREEN-3}} |")
    
    def chatRight(self, texte: str):
        text = texte.split(" ")
        ligne = ''

        if len(texte) >= CHAT_LENGHT:
            for mot in text:
                ligne += mot + ' '
                if len(ligne) >= CHAT_LENGHT: 
                    print(f"| {BLUE}{ligne:>{TAILLE_SCREEN-3}} |")
                    ligne = ""
        else:
            print(f"| {BLUE}{texte:>{TAILLE_SCREEN-3}} |")

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
    def __init__(self, matricule: str, nom: str, prénom: str, dateNaissance:str, nationnalité:str, mail: str, téléphone: int, login: str, password: str, typeP:str, classe, notes) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.dateNaissance = dateNaissance
        self.nationnalité = nationnalité
        self.usecase = DefaultUseCases()
        self.notes = self.usecase.getListe(notes)
        self.classe = classe #id de la classe
        self.charge = self.usecase.sql.getTables(f"SELECT chargé From Classe WHERE idC='{self.classe}' ")[0][0]# type: ignore
        self.traitement()
        
    def traitement(self)->None:
        while True:
            match self.usecase.controlMenu("Menu General",ETUDIANT_USECASE["main"]):
                case 1:
                    self.usecase.showMsg("Mes notes",wait=False)
                    self.showNotes()
                case 2:
                    self.usecase.showMsg("Mes Commentaires",wait=False)
                    self.usecase.commentaires(self.matricule, self.charge, self.matricule)
                case 3:
                    self.usecase.quitter()
                    self.user_connect = self.usecase.accueil()
                    self.user_active = self.usecase.createUser(self.user_connect)
                    break
     
    def showNotes(self)->None:
        # attributs = ["Module","Note Evalution","Note Examen"]
        # print(f"Etudiant: {self.nom} {self.prénom}")
        # print(tabulate(headers=attributs,tabular_data=self.notes, tablefmt='double_outline'))  #type:ignore
        # self.usecase.pause()
        self.usecase.report(self.matricule)

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
        self.id = id
        self.libelle = libelle
        self.mail = mail
        self.telephone = téléphone
        self.login = login
        self.password = password
        self.usecase = DefaultUseCases()
        self.all_Etudiants = self.usecase.loadStudentsFolder()
        self.traitement()
        
    def traitement(self):
        while True:
            match self.usecase.controlMenu("Menu général", PARTENAIRE_USECASES["main"]): 
                case 1:
                    self.consult()
                    self.usecase.pause()
                case 2:
                    self.usecase.quitter()
                    self.user_connect = self.usecase.accueil()
                    self.user_active = self.usecase.createUser(self.user_connect)
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
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, "ResponsableAdmin")
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
                    while True:
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
                            
                            case 7: 
                                self.usecase.showMsg("Liste des partenaires", wait=False)
                                self.usecase.lister("Partenaires")
                                self.usecase.pause()
                            case 8: break
                case 3:
                    self.usecase.showMsg("Menu de modification du chargé", wait=False)
                    self.modifyCharger()
                case 4:
                    match self.usecase.controlMenu("Menu général", RP_USECASES["delete"]):
                        case 1:
                            self.usecase.showMsg("Supprimer un Chargé",wait=False)
                            self.deleteChargé()
                        case 2:
                            self.usecase.showMsg("Supprimer un professeur",wait=False)
                            self.deleteProf()
                        case 3:
                            self.deleteModules()
                        case 4:
                            self.usecase.showMsg("Supprimer un partenaire",wait=False)
                            self.deletePartenaire()
                case 5:
                    match self.usecase.controlMenu("Menu général", RP_USECASES["more"]):
                        case 1:
                            self.setChargeClasse()
                        case 2:
                            self.modifyCharger()
                        case 3:
                            self.usecase.showMsg("Moyenne des Etudiant et de la Classe",wait=False)
                            self.showMoyenne()
                        case 4:
                            match(self.usecase.controlMenu("Menu Statistique",RP_USECASES["stat"])):
                                case 1:
                                    self.viewClassesStats()
                                    pass
                                case 2:
                                    self.viewClassesStatsByFiliere()
                        case 5:
                            continue
                case 6:
                    self.usecase.quitter()
                    self.user_connect = self.usecase.accueil()
                    self.user_active = self.usecase.createUser(self.user_connect)
                    break
                
    #Fonctionnalité de la responsable
    def deleteChargé(self):
        while True:
            chargés=self.usecase.sql.getTables("select Matricule,Nom,Prenom from Chargé ")
            listChargé=list()
            listMat=list()
            for chargé in chargés:
                listChargé.append([chargé[0],chargé[1],chargé[2]])
                listMat.append(chargé[0])
            self.usecase.centerTexte(tabulate(headers=["Matricule", "Nom", "Prenom"],tabular_data= listChargé, tablefmt='double_outline'))    
            matricule=self.usecase.testSaisie("Entrez le matricule du Chargé ou (-1 pour quitter): ", nbreChar = 2)
            if matricule != '-1':
                if matricule in listMat:
                    chargéClasses=self.usecase.sql.getTables(f"select Classes from Chargé where Matricule='{matricule}' ")[0]
                    for idclasse in self.usecase.listTrans(chargéClasses[0]):
                        changement='chargé=" " '
                        self.usecase.sql.updateBase("Classe",changement,"idC",idclasse)
                    self.usecase.sql.getTables(f"Delete from Chargé where Matricule='{matricule}'")
                    self.usecase.showMsg("Chargé supprimé avec succes!")
                    return None
                self.usecase.showMsg("Le matricule saisi ne correspond à aucun Chargé")
            else:
                return None

    def deleteProf(self):
        while True:
            att=["Id Professeur", "Nom", "Prenom"]
            profs=self.usecase.sql.getTables(f"select idP,Nom,Prenom from professeurs ")
            listId=list()
            listprofs=list()
            for prof in profs:
                listprofs.append([prof[0],prof[1],prof[2]])
                listId.append(prof[0])
            self.usecase.centerTexte(tabulate(headers=att,tabular_data= listprofs, tablefmt='double_outline'))   
            
            idProf=self.usecase.testSaisie("Saisir l'id du professeur ou (-1 pour quitter): ","int")
            if idProf != -1:
                l = list()
                
                if idProf in listId:
                    ClassProfMod=self.usecase.sql.getTables(f"select Classes,modules from professeurs where idP={idProf}")[0]
                    if(ClassProfMod[0]!=[]):
                        for classP in self.usecase.listTrans(ClassProfMod[0]):
                            idProfs=self.usecase.sql.getTables(f"select professeurs from Classe where idC='{classP}' ")[0]
                            liste=self.usecase.listTrans(idProfs[0])
                            print(liste)
                            if idProf in liste:
                                liste.remove(idProf)
                                changement=f'professeurs="{liste}" '
                                self.usecase.sql.updateBase("Classe",changement,"idC",classP)
                    for idMod in self.usecase.listTrans(ClassProfMod[1]):
                        professeurs=self.usecase.sql.getTables(f"select professeurs from Modules where idM={idMod}")[0][0]
                        listProfesseurs=self.usecase.listTrans(professeurs)
                        if idProf in listProfesseurs:
                            listProfesseurs.remove(idProf)
                            changement=f'professeurs="{listProfesseurs}" '
                            self.usecase.sql.updateBase("Modules",changement,"idM",idMod)
                        
                    self.usecase.sql.getTables(f"Delete from professeurs where idP={idProf} ")
                    
                    self.usecase.showMsg("Professeur supprimé avec succes")
                    return None
                self.usecase.showMsg("L' Id saisi ne correspond à aucun professeur")
            else: return None
        
    def deleteModules(self):
        while True:
            self.usecase.showMsg("Supprimer un module",wait=False)
            modules = self.usecase.sql.getTables(f"select idM, libelle, coefficient, professeurs, classes from Modules")
            print(tabulate(headers=["idM", "libelle", "coefficient"], tabular_data= [[mod[0], mod[1], mod[2]] for mod in modules ], tablefmt= "double_outline" ))
            print("")
            idM = self.usecase.testSaisie("Entrez l'id du module à supprimer ou (-1 pour quitter): ", 'int', min= -1)
            if idM != -1:
                for Mod in modules:
                #REcherche de l'id saisie par l'utilisateur dans la liste des modules
                    if Mod[0] == idM:
                        # Suppression du modules dans la liste de module des professeurs
                        for idPro in self.usecase.listTrans(Mod[3]):
                            modProf = self.usecase.listTrans(self.usecase.sql.getTables(f"SELECT modules FROM professeurs WHERE idP = {idPro}")[0][0])
                            modProf.remove(idM)
                            self.usecase.sql.updateBase("professeurs", f"modules = '{modProf}' ", "idP", idPro)
                        
                        # Suppression du module dans la liste des classes
                        for idClasse in self.usecase.listTrans(Mod[4]):
                            classeMods = self.usecase.listTrans(self.usecase.sql.getTables(f"SELECT modules FROM Classe WHERE idC = {idClasse}")[0][0])
                            classeMods.remove(idM)
                            self.usecase.sql.updateBase("Classe", f"modules = '{classeMods}' ", "idC", idClasse)
                        
                        # Suppression du module dans la liste des modules
                        self.usecase.sql.delete("idM", idM, "Modules")
                        self.usecase.showMsg(f"Le module {Mod[1]} a été supprimé avec succes !")
                        
                        return None
                self.usecase.showMsg("L'id saisie ne correspond à aucun module !")
                print("")
            else: return None
             
    def deletePartenaire(self):
        while True:
            self.usecase.showMsg("Menu de suppresion de partenaire", wait= False)
            partenaires = self.usecase.sql.getTables("SELECT id, Libelle, Mail FROM partenaires")
            print(tabulate(headers= ["Id", "Libelle", "E-Mail"], tabular_data= partenaires, tablefmt= "double_outline" ))
            print("")
            
            idPart = self.usecase.testSaisie("Entrez le libelle du partenaire à supprimer ou (-1 pour quitter): ", 'int', min = -1)
            if idPart != -1:
                for part in partenaires:
                    if part[0] == idPart:
                        # Suppression du partenaire de la liste des partanires...add()
                        self.usecase.sql.delete("id", idPart, "partenaires")
                        self.usecase.showMsg(f"{part[1]} à été retiré de la liste de vos partenaires !", wait = False)
                        self.usecase.pause()
                        return None
                    
                self.usecase.showMsg("L'id du partenaire que vous avez saisie est invalide !", wait= False)
                self.usecase.pause()
            else:
                return None
    # def deleteFilière(self):
    #     while True:
    #         self.usecase.showMsg("Supprimer une filière",wait=False)
    #         filières = self.usecase.sql.getTables(f"SELECT * FROM filiere")
    #         print(tabulate(headers=["idM", "libelle"], tabular_data= [[fil[0], fil[1]] for fil in filières], tablefmt= "double_outline" ))
    #         print("")
    #         idF = self.usecase.testSaisie("Entrez l'id de la filière à supprimer : ", 'int')
            
    #         # Recherche de l'id de la filière dans liste des filières..
    #         for fil in filières:
    #             print(fil[0])
    #             self.usecase.pause()
    #             if fil[0] == idF:
    #                 # Suppression du module dans la liste des classes
    #                 for idClasse in self.usecase.listTrans(fil[2]):
    #                     # Mise à jour de la filière de la classe à une Chaine Vide !
    #                     self.usecase.sql.updateBase("Classe", f"Filiere = '' ", "idC", idClasse)
                    
    #                 # Suppression de la filière dans la liste des filières...
    #                 self.usecase.sql.delete("idF", idF, "filiere")
    #                 self.usecase.showMsg(f"La filière {fil[1]} a été supprimé avec succes !")
    #                 self.usecase.pause()
    #                 return  None
                
    #         self.usecase.showMsg("L'id saisie ne correspond à aucune filière !", wait=False)
    #         print("")
    #         self.usecase.pause()
            
    def filtrer(self):
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
    
    def modifyCharger(self):
        while True:
            self.usecase.showMsg("Menu de modification d'un chargé", wait= False)
            print("")
            self.usecase.lister("Chargés")
            print("")
            matricule = self.usecase.testSaisie("Entrez le matricule du chargé à modifier ou (-1 pour quitter) : ", nbreChar=2)
            if matricule != '-1':
                if self.usecase.sql.getTables(f"SELECT * FROM Chargé WHERE Matricule = \"{matricule}\"") != []:
                    while True:
                        self.usecase.showMsg(f"Menu de modification de la chargé", wait=False)
                        chargé = self.usecase.showChargeInfo(matricule) # type: ignore
                        print("")
                        choix = self.usecase.testSaisie("Entrez le numéro de l'élément à modifier ou (-1) pour quitter : ",'int', min = -1)
                        match choix:
                            case -1:
                                return None
                            case 1:
                                self.usecase.showMsg("Modification du Nom", wait= False)
                                print("")
                                self.usecase.centerTexte(f"Ancien Nom: {BLUE} {chargé[choix]}") #type: ignore
                                new = self.usecase.testSaisie("Entrez le nouveau nom :")
                                mail = f"{chargé[3]}".replace(chargé[choix].lower(), new.lower())#type: ignore
                                self.sql.updateBase("Chargé", f"Nom = \"{new.upper()}\"", "Matricule", matricule) #type: ignore
                                self.sql.updateBase("Chargé", f"mail = \"{mail}\"", "Matricule", matricule) #type: ignore
                                self.usecase.showMsg("le Nom a bien été changé !", wait= False)
                                print("")
                                self.usecase.showMsg(f"Information de {chargé[1]} {chargé[2]}", wait=False) #type: ignore
                                self.usecase.showStudentInfo(matricule) # type: ignore
                                
                                print("")
                                if self.usecase.question("Voulez-vous modifier un autre élément") == 'non':
                                    return None
                            case 2:
                                self.usecase.showMsg("Modification du prénom", wait= False)
                                print("")
                                self.usecase.centerTexte(f"Ancien prénom: {BLUE} {chargé[choix]}") #type: ignore
                                new = self.usecase.testSaisie("Entrez le nouveau prénom :")
                                mail = f"{chargé[3]}".replace(chargé[choix].replace(" ", '-').lower(), new.replace(" ", '-').lower())#type: ignore
                                self.sql.updateBase("Chargé", f"Prenom = \"{new.title()}\"", "Matricule", matricule) #type: ignore
                                self.sql.updateBase("Chargé", f"mail = \"{mail}\"", "Matricule", matricule) #type: ignore
                                self.usecase.showMsg("le prénom a bien été changé !", wait= False)
                                print("")
                                self.usecase.showMsg(f"Information de {chargé[1]} {chargé[2]}", wait=False) #type: ignore
                                self.usecase.showChargeInfo(matricule) # type: ignore
                                
                                print("")
                                if self.usecase.question("Voulez-vous modifier un autre élément") == 'non':
                                    return None
                            case 4:
                                self.usecase.showMsg("Modification du numéro de téléphone", wait= False)
                                print("")
                                self.usecase.centerTexte(f"Ancienne téléphone: {BLUE} {chargé[choix]}") #type: ignore
                                new = self.usecase.agree_number("Entrez le nouveau téléphone : ")
                                self.sql.updateBase("Chargé", f"Telephone = {new}", "Matricule", matricule)
                                self.usecase.showMsg("le téléphone a bien été changé !", wait= False)
                                print("")
                                self.usecase.showMsg(f"Information de {chargé[1]} {chargé[2]}", wait=False)#type: ignore
                                self.usecase.showChargeInfo(matricule) # type: ignore
                                
                                print("")
                                if self.usecase.question("Voulez-vous modifier un autre élément") == 'non':
                                    return None
                            case 5:
                                while True:
                                    self.usecase.showMsg(f"Liste des classes de {chargé[1]}", wait=False)#type: ignore
                                    classes = self.sql.getTables(f"SELECT Libelle FROM Classe WHERE idC IN ({chargé[5][1:-1]})")#type: ignore
                                    self.usecase.ligneMenu(2, TAILLE_SCREEN - 2 , 'haut')
                                    self.usecase.showMenu([[" Liste des classes",(TAILLE_SCREEN-2), 'center']])
                                    self.usecase.showMenu([[" \t".join([classe[0] for classe in classes]),(TAILLE_SCREEN-(4*len(classes))-2), 'center']])
                                    self.usecase.ligneMenu(2, TAILLE_SCREEN-2, 'milieu')
                                    self.usecase.showMenu([["Retiré une classe", TAILLE_SCREEN//2-1, 'center'], ["Ajouter une classe", TAILLE_SCREEN//2-1, 'center']])
                                    self.usecase.showMenu([[1, TAILLE_SCREEN//2-1, 'center'], [2, TAILLE_SCREEN//2-1, 'center']])
                                    self.usecase.ligneMenu(3, TAILLE_SCREEN//2-1, 'bas')
                                    print("")
                                    choix = self.usecase.testSaisie("Faites votre choix : ", 'int')
                                    if choix in [1, 2]:
                                        match choix:
                                            case 1:
                                                while True:
                                                    self.usecase.showMsg("Retirer une classe", wait= False)
                                                    print("")
                                                    self.usecase.ligneMenu(2, TAILLE_SCREEN - 2 , 'haut')
                                                    self.usecase.showMenu([[f" Liste des classes de {chargé[1]}",(TAILLE_SCREEN-2), 'center']])#type: ignore
                                                    self.usecase.showMenu([[" \t".join([classe[0] for classe in classes]),(TAILLE_SCREEN-(4*len(classes))-2), 'center']])
                                                    self.usecase.ligneMenu(2, TAILLE_SCREEN-2, 'bas')
                                                    print()
                                                    classe = self.usecase.testSaisie("Entrez le libellé de la classe à retirer ou (-1 pour quitter): ", nbreChar = 2).upper()# type: ignore
                                                    if classe != '-1':
                                                        if classe in [classe[0] for classe in classes]:
                                                            clas = self.usecase.listTrans(chargé[5])# type: ignore
                                                            idC = clas[classes.index((classe,))]
                                                            clas.remove(idC) # type: ignore
                                                            self.usecase.sql.updateBase("Classe", "chargé = ''", "idC", idC)
                                                            self.sql.updateBase("Chargé", f"Classes = \"{clas}\"", "Matricule", matricule)# type: ignore
                                                            
                                                            self.usecase.showMsg("La classe a bien été retirée!", wait=False)
                                                            self.usecase.pause()
                                                            
                                                            self.usecase.showMsg(f"Information de {chargé[1]} {chargé[2]}", wait=False) #type: ignore
                                                            self.usecase.showChargeInfo(matricule) # type: ignore
                                                            print("")
                                                            
                                                            if self.usecase.question("Voulez-vous modifier un autre élément") == 'non': break
                                                        else:
                                                            self.usecase.showMsg("Le libelle n'est pas correct !", wait=False)
                                                            self.usecase.pause()
                                                    else: break
                                            case 2:
                                                self.setChargeClasse(matricule) # type: ignore
                                                break
                                    else:
                                        self.usecase.showMsg("Erreur de saisie", wait= False)
                                        print("")
                                        if self.usecase.question("Voulez-vous réessayer") == 'non':
                                            return None
                else:
                    self.usecase.showMsg("Le matricule est incorrect !", wait=False)
                    self.usecase.pause()
            elif matricule == '-1':  return None
            else:
                self.usecase.showMsg("Le matricule est incorrecte ! ", wait=False)
                self.usecase.pause()
       
    def setChargeClasse(self, matricule: str = ""):
        listeClasse = list()
        if matricule == "":
            while True:
                self.usecase.showMsg("Attribuer une classe a un chargé",wait=False)
                self.usecase.lister("Chargés")
                matricule = self.usecase.testSaisie("Entrez le matricule du chargé : ") # type: ignore
                chargé = self.usecase.sql.getTables(f"SELECT * FROM Chargé WHERE Matricule = '{matricule}' ") #[(Matricule, nom, prenom),]chargé[0][0]
                if chargé != []:
                    break
                else:
                    self.usecase.showMsg("Le matricule du chargé le correspond pas !", clear=True)
        else:  chargé = self.usecase.sql.getTables(f"SELECT * FROM Chargé WHERE Matricule = '{matricule}' ") #[(Matricule, nom, prenom),]chargé[0][0]

        while True:
            self.usecase.showMsg("Attribuer une classe à la chargé",wait=False)
            print("")
            self.usecase.centerTexte(f"{BLUE}Liste des classes n'ayant pas de chargé")
            classes = self.usecase.sql.getTables("SELECT idC, Libelle, effectif, niveau FROM Classe WHERE chargé = '' ")
            self.usecase.centerTexte(tabulate(headers= ["id Classe", "Libelle", "Effectif", "Niveau", "Chargé de classe"], tabular_data= classes, tablefmt='double_outline'))            
            print("")
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
                classe = self.usecase.sql.getTables(f"SELECT libelle, chargé, etudiants FROM Classe WHERE idC = {idC}")
                if classe[0][1]  == "":
                    if idC not in chargéClasses:
                        chargéClasses.append(idC)
                        self.usecase.sql.updateBase("Classe", f"chargé = '{matricule}'", "idC", idC)
                        
                        #Ajout des étudiants dans la liste de commentaire de la chargé !
                        charges = self.usecase.loadStudentsFolder(FOLDER_CHARGES_FILE)
                        chargeCommentaire = charges[f"{matricule}"]["Commentaire"]
                        for MatriculeEtudiant in self.usecase.listTrans(classe[0][2], 'chaine'):
                            chargeCommentaire[f"{MatriculeEtudiant.strip()}"] = []
                        self.usecase.updateFile(FOLDER_CHARGES_FILE, charges)
                else:
                    classeAyChargé.append(classe[0][0])
            if len(listeClasse) != len(chargéClasses):
                classes = ", ".join(classeAyChargé)
                self.usecase.showMsg(f"Les classes : {classes} ont déjà un chargé(e) !", clear=False, wait=False)
                self.usecase.pause()
                
            self.usecase.sql.updateBase("Chargé", f"classes = '{str(chargéClasses)}' ", "Matricule", matricule)
            self.usecase.showMsg(f"La liste des classes a bien été attribuer à {chargé[0][1]}")
            
    # def setChargeClasseOld(self):
    #     listeClasse = list()
    #     while True:
    #         self.usecase.showMsg("Attribuer une classe a un chargé",wait=False)
    #         self.usecase.lister("Chargés")
    #         matChargé = self.usecase.testSaisie("Entrez le matricule du chargé : ")
    #         chargé = self.usecase.sql.getTables(f"SELECT * FROM Chargé WHERE Matricule = '{matChargé}' ") #[(Matricule, nom, prenom),]chargé[0][0]
    #         if chargé != []:
    #             break
    #         else:
    #             self.usecase.showMsg("Le matricule du chargé le correspond pas !", clear=True)
        
    #     while True:
    #         self.usecase.showMsg("Attribuer une classe a un chargé",wait=False)
    #         self.usecase.lister("Classes")
    #         idClasse = self.usecase.testSaisie("Entrez l'id de la classe : ", 'int',min=1, max=1000)
    #         classe = self.usecase.sql.getTables(f"SELECT * FROM Classe WHERE idC = {idClasse} ") #[(informations_chargé),]
    #         if classe != []:
    #             listeClasse.append(idClasse)
    #             if self.usecase.question("Voulez vous ajouter une autre classe") == 'oui':
    #                 continue
    #             else: break
    #         else:
    #             self.usecase.showMsg("L'id de la classe ne correspond pas !", clear=True)
    #     self.usecase.showMsg("Attribuer une classe a un chargé",wait=False)
    #     if self.usecase.question("Voulez vous enregistrer les modifications") == 'oui':
    #         chargéClasses = self.usecase.listTrans(chargé[0][8])
    #         classeAyChargé = list()            
    #         for idC in listeClasse:
    #             classe = self.usecase.sql.getTables(f"SELECT libelle, chargé FROM Classe WHERE idC = {idC}")
    #             if classe[0][1]  == "":
    #                 if idC not in chargéClasses:
    #                     chargéClasses.append(idC)
    #                     self.usecase.sql.updateBase("Classe", f"chargé = '{matChargé}'", "idC", idC)
    #             else:
    #                 classeAyChargé.append(classe[0][0])
                    
    #         if len(listeClasse) != len(chargéClasses):
    #             classes = ", ".join(classeAyChargé)
    #             self.usecase.showMsg(f"Les classes : {classes} ont déjà un chargé(e) !", clear=False, wait=False)
    #             self.usecase.pause()
    #         self.usecase.sql.updateBase("Chargé", f"classes = '{str(chargéClasses)}' ", "Matricule", matChargé)
    #         self.usecase.showMsg(f"La liste des classes a bien été attribuer à {chargé[0][1]}")
        
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
        mod["coefficient"]=self.usecase.testSaisie("Entrer le coefficient du module : ","int",min=1)
        mod["credit"]=self.usecase.testSaisie("Entrer le credit du module : ","int",min=1)
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
        prof["Mail"] = self.usecase.testSaisie("Entrez le mail : ").lower() # type: ignore
        prof["Telephone"] = self.usecase.agree_number("Entrez le téléphone  : ")
        prof["Classes"] = []
        prof["Modules"] = []
        print('')
        while True:
            self.usecase.showMsg("Liste des classes", wait=False)
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
            if result != 0:
                self.usecase.showMsg("Liste des modules", wait=False)
                self.usecase.lister("Modules")
                idM = self.usecase.testSaisie("Entrez l'id de du module du prof : ", 'int', 1, result) 
                prof["Modules"].append(idM)
                if self.usecase.question("Voulez vous ajouter un autre module ?") != "oui":
                    break
            else: break
            
        while True:
            self.usecase.showMsg("Enregistrement du nouveau prof", wait=False)
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
        self.usecase.lister("Classes")
        libelle = self.usecase.testSaisie("Entrer le libelle de la classe : ").upper()#type:ignore
        etudiants = self.usecase.sql.getTables(f"SELECT etudiants From Classe where Libelle='{libelle}' ")
        listMoyenne = list()
        moyenneClasse = 0.0
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
            if coef != 0:
                dico.append(f"{etu[0][0]} {etu[0][1]}")
                dico.append(moyenne/coef)
                listMoyenne.append(dico)
                moyenneClasse+=(moyenne/coef)
        self.usecase.showMsg("Moyenne des étudiants dans la classe", wait=False)
        attributs=["Etudiant","Moyenne"]
        print(tabulate(headers=attributs,tabular_data=listMoyenne,tablefmt='double_outline'))
        print("-"*100)
        moy=moyenneClasse/len(self.usecase.listTrans(etudiants[0][0],'chaine'))
        text=f"Moyenne de {libelle}{' '*80}{moy}"
        print(tabulate(tabular_data=[[text]],tablefmt='double_outline'))
        self.usecase.pause()
        
    def moyenneEtuByMatricule(self, matricule: str) -> float:
        marksEtu = self.usecase.sql.getTables(f"SELECT Notes FROM Etudiants WHERE Matricule = '{matricule}' ")
        moyenne = 0.0
        coef = 0
        for note in self.usecase.getListe(marksEtu[0][0]):
            module = self.usecase.sql.getTables(f"SELECT coefficient,credit from Modules where libelle='{note[0]}' ")
            totalEval = int(note[1])*0.4
            totalExam = int(note[2])*0.6
            moyenneMod = (totalEval+totalExam)*module[0][0]
            coef += module[0][0]
            moyenne += moyenneMod
        return 0.0 if coef == 0 else moyenne/coef
    
    def moyenneClasse(self, classeEtu):
        classeMoyenne, nbreVal, nbreNonVal = 0.0, 0, 0
        etuMoyennes = []
        etu = self.usecase.listTrans(classeEtu, "chaine")
        for etuMatricule in etu:
            moyEtu = self.moyenneEtuByMatricule(etuMatricule.strip())
            if moyEtu >= 10:
                nbreVal += 1
            else:
                nbreNonVal += 1
            etuMoyennes.append(moyEtu)
            classeMoyenne +=  moyEtu  
        return [max(etuMoyennes), min(etuMoyennes), classeMoyenne/len(etu), nbreVal, nbreNonVal]
        
    def schoolYearClasses(self, school_year) -> list:
        return self.usecase.sql.getTables(f"SELECT Libelle, etudiants FROM Classe WHERE Annee_Scolaire = '{school_year}' ")
    
    def viewClassesStats(self):
        # Récupérer les classes de l'année_scolaire en cours
        # Parcourir la liste de matricule de chaque classes pour calculer les moyennes
        while True:
            school_Year = self.usecase.testSaisie("Entrez l'année-scolaire de la statistique : ")
            classes = self.schoolYearClasses(school_Year)
            if classes != []:
                data = []
                for classe in classes:
                    classeData = self.moyenneClasse(classe[1])
                    classeData.insert(0, classe[0])
                    data.append(classeData)
                attributs = ["Classe", "Forte moyenne", "Faible moyenne", "Moyenne générale", "Nombre etudiants validé", "Nombre etudiants Non-validé" ]
                self.usecase.showMsg(f"Statistique des classes de l'année_scolaire : {school_Year}", wait = False)
                print(tabulate(headers = attributs, tabular_data = data, tablefmt = "double_outline"))
                print("")
                self.usecase.pause()
                break
            
            
    def viewClassesStatsByFiliere(self):
        while True:
            filiere=self.usecase.testSaisie("Saisir la filiere de la statistique: ")
            school_Year=self.usecase.testSaisie("Saisir l'annee de la statistique: ")
            classes=self.usecase.sql.getTables(f"SELECT Libelle,etudiants from Classe where Filiere='{filiere}' and Annee_Scolaire='{school_Year}' ")
            moyenneEtu,moyenneClasse,nbrVal,nbrNonVal=0.0 ,0.0 ,0 ,0
            listMoyenne=list()
            data=[]
            if(classes!=[]):
                for classe in classes:
                    liste=self.moyenneClasse(classe[1])
                    liste.insert(0,classe[0])
                    data.append(liste)
                break
        attributs = ["Classe", "Forte moyenne", "Faible moyenne", "Moyenne générale", "Nombre etudiants validé", "Nombre etudiants Non-validé" ]
        self.usecase.showMsg(f"Statistique de la Filiere {filiere} à l'Annee_Scolaire {school_Year}",wait=False)
        print(tabulate(headers=attributs,tabular_data=data,tablefmt="double_outline"))
        self.usecase.pause()
            
class Application:
    def __init__(self) -> None:
        self.useCases = DefaultUseCases()
        self.user_connect = self.useCases.accueil()
        self.user_active = self.useCases.createUser(self.user_connect)
        
if __name__ == "__main__":
    Application()
    # Admin()
    # ResponsableAdmin()
    # Chargé()
    # Partenaire()
    # Etudiant()