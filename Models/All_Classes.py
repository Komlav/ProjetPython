from random import randint
import sqlite3
import os
from string import ascii_uppercase
from time import sleep, time 
from datetime import datetime

# from tabulate import tabulate ## python -m pip install tabulate

from pyfiglet import figlet_format
import colorama as color #pip install colorama : C'est un module qui permet de mettre la couleur 
from colorama import init
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

DEFAULT_PASSWORD = "passer@123"
DEFAULT_EFFECTIF = 40
TAILLE_SCREEN = 150
BASE_FILE = "./DataBase/Database.sqlite3"
EGALE = "="

POLICES = ['avatar', 'banner', 'banner3-D', 'banner3', 'banner4', 'big', "isometric3", 'bulbhead']


ADMIN_USECASES = {
    "main": ["Ajouter un nouveau", "Voir toutes les listes", "Modifier une information", "Se déconnecter"],
    "add": ["Ajouter un étudiant","Ajouter un(e) chargé","Ajouter un(e) responsable", "Retourner au menu général"],
    "liste" : ['Lister les étudiants', 'Lister les chargé(e)s', 'Lister les responsables', "Retourner au menu général"],
    "edit": ["Profil"]
}


class MySql:
    
    def __init__(self) -> None:
        #Connexion à la base de donnée
        self.base = sqlite3.connect(BASE_FILE)
        #Initialisation du curseur de connexion
        self.curseur = self.base.cursor()
        
        self.TABLES_USER = {
            "Admin": ["Matricule", "Nom", "Prenom", "Mail", "Telephone", "Login","Password","TypeP", "Etudiants", "Chargés", "responsableAdmin", "classes"],
            "Chargé": ["Matricule", "Nom", "Prenom", "Mail", "Telephone", "Login", "Password", "TypeP",  "Classes"],
            "Etudiants": [ "Matricule", "Nom", "Prenom", "DateNaissance", "Nationnalité", "Mail", "Telephone", "Login", "Password", "TypeP","IdClasse", "Notes"],
            "partenaires": ["Matricule", "libelle", "Mail", "Telephone", "Login", "Password", "TypeP", "etudiants"],
            "responsableAdmin": ["Matricule", "Nom", "Prenom", "Mail", "Telephone","Login", "Password", "TypeP", "Classes", "Chargés"]
        }
        
        self.TABLES_OTHERS = {
            "filiere": ["idF","libelle","classes"], 
            "Modules": ["idM", "libelle", "classes", "professeurs", "notes"],
            "Niveau": ["idN","libelle","classes"],
            "professeurs": ["idP", "Nom", "Prenom", "mail", "Telephone", "Classes", "modules"], 
            "Classe": ["idC", 'libelle', 'filière', 'niveau', 'effectif', 'chargé', 'professeurs', 'modules', 'etudiants']
        }
        
        self.TABLES = {
            "Etudiants":"Matricule text, Nom text, Prenom text, DateNaissance text, Nationnalité text, Mail text, Telephone number, Login text, PassWord text, TypeP text, IdClasse number, Notes text", 
            "Chargé":"Matricule text, Nom text, Prenom text, mail text, Telephone number, Login text, Password text, TypeP text,  Classes text", 
            "Admin":"Matricule text, Nom text, Prenom text, mail text, Telephone number, Login text, Password text, TypeP text, Etudiants text, Chargés text, responsableAdmin text, classes text", 
            "Filiere":"idF number, libelle text, classes text", 
            "Modules":"idM number, libelle text, classes text, professeurs text, notes text", 
            "Niveau":"idN number, libelle text, classes text", 
            "partenaires":"Matricule text, libelle text, mail text, Telephone number, Login text, Password text, TypeP text, etudiants text", 
            "professeurs":"idP number, Nom text, Prenom text, mail text, Telephone number, Classes text, modules text", 
            "ResponsableAdmin":"Matricule text, Nom text, Prenom text, mail text, Telephone number, Login text, Password text, TypeP text, classes text, Chargés text",
            "Classe":"idC number, Libelle text, Filiere text, niveau number, effectif number, chargé text, professeurs text, modules text, etudiants text"
        }
        
        self.initTables(self.TABLES)
        
        self.datas = self.getUserData(self.TABLES_USER)
        self.component = self.getUserData(self.TABLES_OTHERS)
        
        
        #Mise à jour des changemements effectuer
        self.base.commit()
        #Fermeture de la base de donnée
    def closeDB(self):
        self.base.close()

    def updateBase(self,attribut:str,newValue,key:str,value,table:str):
        requete=f" UPDATE {table} SET {attribut}={newValue} WHERE {key}={value}" #L2 GRLS
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
            val = ','.join(['?']*len(colonne))
            self.curseur.execute(f"INSERT INTO {table} VALUES ({val})",value)
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
    def __init__(self, matricule:str, nom:str, prénom:str, mail:str, téléphone:int, login:str, password:str, typeP:str) -> None:
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
    # def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, etudiants:list = [], chargés:list = [], responsableAdmin:list = [], partenaires:list = []) -> None:
    #     super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
    #     self.etudiants = etudiants
    #     self.chargés = chargés
    #     self.responsableAdmins = responsableAdmin
    #     self.partenaires = partenaires
    #     self.usecase = DefaultUseCases()
    #     self.traitement()
        
    def __init__(self) -> None:
        self.usecase = DefaultUseCases()
        self.traitement()
        
    def MenuAdmin(self) -> int|None:
        retour=1
        while(retour==1):
            print("1-Ajouter un etudiant") 
            print("2-Lister les etudiant") 
            print("3-Ajouter un chargé") 
            print("4-Lister les chargés") 
            print("5-Ajouter un responsable Administratif") 
            print("6-Lister les responsables Administratifs") 
            print("7-Quitter") 
            choix=self.usecase.Saisie("Faites un choix",1,7)
            if not str(choix).isdigit():
                self.usecase.clear()
            else:
                return choix
        
    
    def traitement(self):
        while True:
            match self.usecase.controlMenu("Menu général", ADMIN_USECASES["main"]):
                case 1:
                    while True:
                        match  self.usecase.controlMenu("Ajout d'un nouvel utilisateur", ADMIN_USECASES["add"]):
                            case 1:
                                self.ajoutEtudiant()
                            case 2:
                                # self.ajoutChargé()
                                pass
                            case 3:
                                # self.ajoutRP()
                                pass
                            case 4:
                                break
                case 2:
                    while True:
                        match  self.usecase.controlMenu("Liste des utilisateurs", ADMIN_USECASES["list"]):
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
                    # self.ajoutEtudiant()
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
                    break
        pass
    
    def setUserMail(self, user:dict, domaine:str = "ism.edu",):
        return  f"{user.get('Prénom').replace(' ', '-').lower()}.{user.get('Nom').split(' ')[-1].lower()}@{domaine}.sn" # type: ignore
    
    def ajoutEtudiant(self):
        time = datetime.now()
        a, m, j = time.strftime('%Y'),time.strftime('%m'),time.strftime('%d')
        etudiant = dict()
        matricule = f"ISM{a}/DK{len(self.usecase.sql.datas['Etudiants'])+1}-{m}{j}"
        classe = self.usecase.createOrSearchClasse(self.usecase.getIdClasse())
        etudiant = {
            "Matricule":matricule,
            "Nom":self.usecase.test("Nom: "),
            "Prénom":self.usecase.test("Prenom: "),
            "DateNaissance":self.usecase.ver_date("\nInformations sur la date de naissance"),
            "Nationnalité":self.usecase.test("Nationnalité: "),
            "Telephone":self.usecase.agree_number("Etudiant")
        }
        
        print(etudiant)
        
        while True:
            choix=self.usecase.question("Confirmer l'enregistrement")
            if choix =="oui":
                if type(classe) == tuple:
                    etudiant["IdClass"] = classe[0]
                    self.usecase.sql.updateBase("effectif", classe[1]["effectif"] + 1, "idC", classe[0], "Classe")
                    listeMatricules=self.usecase.listTrans(classe[1]["etudiants"])
                    listeMatricules.append(matricule)
                    self.usecase.sql.updateBase("etudiants",str(listeMatricules), "idC", classe[0], "Classe")
                elif type(classe) == dict: 
                    etudiant["IdClasse"] = classe["idC"]
                    classe["etudiants"] = f"{[matricule]}"
                    self.usecase.sql.insert('Classe',tuple(classe.values()), self.usecase.sql.TABLES_OTHERS["Classe"])
                    
                self.usecase.sql.insert("Etudiants",self.user(etudiant), self.usecase.sql.TABLES_USER["Etudiants"])
                self.usecase.sql = MySql()
                self.usecase.sql.closeDB()
                self.usecase.showMsg("Etudiant ajouté avec succes")
                break
        
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
            newChargé.get("Classe")
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
            "ResponsableAdmin",
            newResponsableAdmin.get("Classes"),
            newResponsableAdmin.get("Chargés")
        )
        
    def addNewPartenaire(self, newPartenaire:dict):
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
    
###########################################################
#################### Class du chargé ######################
###########################################################
class Chargé(User):
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, classes:list = [], commentaires:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.classes = classes #les ids des classes
        self.commentaires = commentaires
        self.usecase=DefaultUseCases()
        
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
    
    def MenuCharge(self) -> int|None:
        retour=1
        while(retour==1):
            print("1-Lister les Etudiants d'une classe") 
            print("2-Voir les notes des etudiants d'une classe") 
            print("3-Voir les notes d'un etudiant") 
            print("4-Modifier la note d'un etudiant") 
            print("5-Modifier les notes d'une classe") 
            print("6-Voir les commentaires") 
            print("7-Faire un commentaire") 
            print("8-Quitter") 
            choix=self.usecase.Saisie("Faites un choix",1,8)
            if not str(choix).isdigit():
                self.usecase.clear()
            else:
                return choix
    
    #Setters
    def setClasse(self, newClasse:str) -> None:
        self.classes.append(newClasse)
        
    # Getters
    def getClasse(self) -> list:
        return self.classes
    
###########################################################
################### Quelsques classes #####################
###########################################################
class DefaultUseCases:

    def __init__(self) -> None:
        self.sql = MySql()
        self.all_User_Data = self.sql.datas #Données des utilisateurs.
        self.all_Other_Data = self.sql.component #Données des filières et autres infos
    
    def header(self,titre:str):
        self.ligne()
        self.ligne()
        self.opération(titre)
    
    def opération(self,title:str):
        self.showMsg(title,clear=False)
    
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
        else:tailleCollonne = TAILLE_SCREEN // nbreFonction-5
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
        Som = 0
        iCmpt = 1
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
   
    def showMsg(self,msg:str, clear:bool = True,color=SUCCESS, motif:str='═', screen:int = TAILLE_SCREEN) -> None:
        if clear: self.clear()
        print(f"""╔{motif*(screen-2)}╗\n║{' '*(screen-2)}║\n║{color}{msg:^{screen-2}}{WHITE}║\n║{' '*(screen-2)}║\n╚{motif*(screen-2)}╝""")
        if clear:sleep(2)
        
    def pause(self):
        os.system("pause")
    
    def showWord(self,mot:str, police:str = "standard")-> str:
        return figlet_format(mot, font=police)
    
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
            tab = '\t'
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
        print(f"╔{'-'*((TAILLE_SCREEN)-2)}╗")
        self.showMenu([[f"        {message} ?", (TAILLE_SCREEN-50), "center"]])
        print(f"╠{'-'*52}╦{'-'*45}╣")
        self.showMenu([[f"{SUCCESS}Oui", 58, "center"],[f"{RED}Non{WHITE}", 57, "center"]], screen=((TAILLE_SCREEN-50)+20))
        print(f"╚{'-'*52}╩{'-'*45}╝")
        return input(f"\n\t\t\t\tFaites votre choix : {SUCCESS}").lower()  
              
                      
    def listTrans(self,liste: str) -> list:
        return [float(i) if i.isdigit() or i.count('.') == 1 else i for i in liste[1:-2].replace("'",'').split(',')]
                    
    def quitter(self):
        self.clear()
        print(SUCCESS + self.showWord("a bientot :)"))
        sleep(5)
        self.clear()
        exit(0)
    
    def clear(self):
        if os.name == 'nt':
            os.system("cls") 
        else:
            os.system("clear")

    def connect(self, login:str, password:str)-> dict:
        for liste_user in self.all_User_Data.values():
            for user in liste_user:
                if (login == user.get("Login") and password == user.get("Password")):
                    return user
        return {}
    
    def ligne(self, motif:str = "-", nombre:int = TAILLE_SCREEN):
        print(motif*nombre)
     
    def showComponents(self, attributs:list, data:list):
        self.ligne("=")
        for attribut in attributs: print(f"{attribut}", end=" ")
        self.ligne("=")
        
        for user in data:
            for i in range(len(attributs)): print(f"{user.get(attributs[i])}", end=" ")
            self.ligne()
    
    def control(self,key:str,value,data:list):
        for element in data:
            if(element.get(key)==value):
                return True
        return False
    
    def DoWhile(self,key:str,data:list):
        while True :
            value = input(f"saisir le {key}: ")
            if(self.control(key,value,data)): #type:ignore
                return value
    
    def getComponentByKey(self,key,value,data) ->dict:
        for element in data:
            if(element.get(key)==value):
                return element
        return {}

    def listerLesEtudiants(self,data:dict,valeur,filtre="Tous"):
        All_Etudiants=data.get("Etudiants")     
        if(filtre == "Tous"):
            donnees=All_Etudiants
        elif(filtre == "Niveau"):
            donnees = [etu for etu in All_Etudiants if(self.getComponentByKey("idC",etu.get("Classe"),data.get("Classes")).get("Niveau") == valeur)]  #type:ignore
            # for etu in All_Etudiants: #type:ignore
            #     if(self.getComponentByKey("idC",etu.get("Classe"),data.get("Classes")).get("Niveau") == valeur):
            #         donnees.append(etu)
        elif(filtre == "Filiere"):
            donnees=[etu for etu in All_Etudiants if(self.getComponentByKey("idC",etu.get("Classe"),data.get("Classes")).get("Filiere") == valeur)]  #type:ignore
        elif(filtre == "Classe"):
            donnees=[etu for etu in All_Etudiants if(etu.get("Classe") == valeur)]  #type:ignore
        else:
            donnees=[etu for etu in All_Etudiants if(etu.get("Nationnalité") == valeur)]  #type:ignore    
        
        print(f"{'Matricule':<10}{'Nom':<10}{'Prenom':<30}{'Date-Naissance':<10}{'Nationnalité':<10}{'Mail':<20}{'Telephone':<10}{'Classe':<10}")
        for etu in donnees: #type:ignore
            print(f"{etu.get('Matricule'):<10}{etu.get('Nom'):<10}{etu.get('Prenom'):<30}{etu.get('Date-Naissance'):<10}{etu.get('Nationnalité'):<10}{etu.get('Mail'):<20}{etu.get('Telephone'):<10}{etu.get('Classe'):<10}")
    
    def Saisie(self,message,min,max):
        nbre = input(f"{message}\n")
        ver = nbre.replace("-","")
        if ver.isdigit() and (int(nbre) >= min and int(nbre) <= max):
            return int(nbre)
            
    def createUser(self,user:dict): 
        Profil=user.get("TypeP")
        match(Profil):
            case "Admin":
                return Admin(user["Matricule"],user["Nom"],user["Prenom"],user["Mail"],user["Telephone"],user["Login"],user["Password"],user["TypeP"])
            
    def test(self,message):
        while True:
            element=input(message)
            if(element!=""):
                return element
                
    def ver_date(self, message:str=""):
        print(message)
        annee = "{:04d}".format(self.Saisie("Entrez l'annee :",1900,9999))
        mois = "{:02d}".format(self.Saisie("Entrez le mois :",1,12))
        jour = "{:02d}".format(self.Saisie("Entrez le jour :",1,31))
        return f"{jour}-{mois}-{annee}"
            
    def agree_number(self,msg=''):
        phone = [70,75,76,77,78]
        while True:
            number = self.Saisie(f"Entrez le numéro de téléphone {msg}:",700000000,790000000)
            if (number // 10000000) in phone:   #type:ignore
                return number
        
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
            posFiliere = self.Saisie("Entrez la position de la filière : ",1,len(all_filières))
            if posFiliere != None:
                break
            else :self.clear()
            
        while True:
            
            pos = self.Saisie("1---- Licence 1\n2---- Licence 2\n3---- Licence 3\n4---- Master 1\n5---- Master 2\nEntrez l'id du niveau de l'étudiant : \n",1,5)
            if niveau != None:
                break
            else: self.clear()
        
        filiere = all_filières[posFiliere-1]
        niv = niveau[pos-1] #type:ignore
        classe_libelle = f"{niv}-{filiere['libelle']}"
        
        return classe_libelle
        
    def createOrSearchClasse(self, libelle:str) -> tuple | dict:
        all_classes = self.all_Other_Data["Classe"]
        fin, alphabet, cpt = len(libelle), '', 0
        
        for classe in all_classes:
            if classe.get("libelle")[0:fin] == libelle:
                cpt += 1
                if classe.get("effectif") <= DEFAULT_EFFECTIF:
                    return (classe["idC"], classe) 
                
        if cpt > 1: alphabet = f" {ascii_uppercase[cpt-1]}"
        if cpt == 1:
            self.sql.updateBase("libelle", f'{libelle} A', 'libelle', libelle, "Classe")
            self.sql.closeDB()
        
        return {
            "idC": len(all_classes) + 1,
            "libelle": f"{libelle}{alphabet}",
            "filière": libelle[3:], 
            "niveau": libelle[:2], 
            "effectif": 1,
            "chargé": "",
            "professeurs":'[]',
            "modules":'[]'
        }
            
    def controlMenu(self,opération:str, fonctionnalités:list):
        while True:
            self.ligne()
            self.ligne()
            self.menuUse(opération,fonctionnalités)
            choix = self.Saisie('Faites un choix',1,len(fonctionnalités))
            if choix != None:
                return choix
            else: self.clear()
        
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
    def setId(self, newId) -> None:
        self.idC = newId

    def setLibelle(self, newlibelle) -> None:
        self.libelle = newlibelle

    def setNiveau(self, newNiveau) -> None:
        self.niveau = newNiveau

    def setEffectif(self, newEffectif) -> None:
        self.effectif = newEffectif

    def setModule(self, newModule: str) -> None:
        self.modules.append(newModule)

    def setProfesseur(self, newProfesseur: str) -> None:
        self.professeurs.append(newProfesseur)

    def setChargé(self, newChargé: str) -> None:
        self.chargé = newChargé

    def setEtudiant(self, newEtudiant: str) -> None:
        self.étudiants.append(newEtudiant)

    #Getters
    def getId(self) -> int:
        return self.idC

    def getLibelle(self) -> str:
        return self.libelle

    def getNiveau(self) -> str:
        return self.niveau

    def getEffectif(self) -> int:
        return self.effectif

    def getModule(self) -> list:
        return self.modules

    def getProfesseur(self) -> list:
        return self.professeurs

    def getChargé(self) -> str:
        return self.chargé 

    def getEtudiant(self) -> list:
        return self.étudiants
    
class Application:
    def __init__(self) -> None:
        self.useCases = DefaultUseCases()
        self.user_connect = self.useCases.accueil()
        self.user_active=self.useCases.createUser(self.user_connect)
        
        

###########################################################
################### Quelsques classes #####################
###########################################################
         
###########################################################
################## Class de l'etudiant ####################
###########################################################

class Etudiant(User):
    def __init__(self, matricule: str, nom: str, prénom: str, dateNaissance:str, nationnalité:str, mail: str, téléphone: int, login: str, password: str, typeP:str, classe, notes:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.dateNaissance = dateNaissance
        self.nationnalité = nationnalité
        self.notes = notes 
        self.classe = classe #id de la classe
        self.commentaires = []
        self.usecase=DefaultUseCases()
        
    def MenuEtudiant(self) -> int|None:
        retour=1
        while(retour==1):
            print("1-Voir mes notes") 
            print("2-Voir mes commentaires") 
            print("3-Faire un commentaire") 
            print("4-Quitter") 
            choix=self.usecase.Saisie("Faites un choix",1,4)
            if not str(choix).isdigit():
                self.usecase.clear()
            else:
                return choix    
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
###########################################################
############### Class de l'administrateur #################
class Filiere:
    def __init__(self, idN:int, libelle:str, classes:list = []) -> None:
        self.id = idN
        self.libelle = libelle
        self.classes = classes
    
    #Setters
    def setId(self, newId:int) -> None:
        self.id = newId
    
    def setLibelle(self, newLibelle:str) -> None:
        self.libelle = newLibelle
    
    def setClasse(self, newClasse:str) -> None:
        self.classes.append(newClasse)
        
    #Getters
    def getId(self) -> int:
        return self.id
    
    def getLibelle(self) -> str:
        return self.libelle
    
    def getClasse(self) -> list:
        return self.classes
       
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
    def setId(self, newId:int) -> None:
        self.id = newId
    
    def setLibelle(self, newLibelle:str) -> None:
        self.libelle = newLibelle
        
    def setClasse(self, newClasse) -> None:
        self.classes.append(newClasse)
    
    def setProfesseur(self, newProfesseur) -> None:
        self.professeurs.append(newProfesseur)
        
    #Getters
    def getId(self) -> int:
        return self.id
    
    def getLibelle(self) -> str:
        return self.libelle
    
    def getClasse(self) -> list:
        return self.classes

    def getProfesseurs(self) -> list:
        return self.professeurs
###########################################################
#################### Class du niveau ######################
###########################################################
class Niveau:
    def __init__(self, idN:int, libelle:str, classes:list = []) -> None:
        self.id = idN
        self.libelle = libelle
        self.classes = classes
    
    #Setters
    def setId(self, newId:int) -> None:
        self.id = newId
    
    def setLibelle(self, newLibelle:str) -> None:
        self.libelle = newLibelle
        
    def setNiveau(self, newClasse:str) -> None:
        self.classes.append(newClasse)
        
    #Getters
    def getId(self) -> int:
        return self.id
    
    def getLibelle(self) -> str:
        return self.libelle
    
    def getClasse(self) -> list:
        return self.classes
        
###########################################################
############### Class de l'administrateur #################
###########################################################
class Note:
    def __init__(self, libelle:str, etudiant:Etudiant) -> None:
        self.libelle = libelle
        self.etudiant = etudiant
    
    #Setters
    def setLibelle(self, newLibelle:str) -> None:
        self.libelle = newLibelle
        
    def setEtudiant(self, newEtudiant:Etudiant) -> None:
        self.etudiant = newEtudiant
    
    #Getters
    def getLibelle(self) -> str:
        return self.libelle
        
    def getEtudiant(self) -> Etudiant:
        return self.etudiant   

###########################################################
############### Class de l'administrateur #################
###########################################################
class Partenaire(User):
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, fichierEtudiant:str) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.etudiants = fichierEtudiant
        self.usecase=DefaultUseCases()
    
    def MenuPartenaire(self) -> int|None:
        retour=1
        while(retour==1):
            print("1-Lister les etudiants") 
            print("2-Consuletr le dossier d'un etudiant") 
            print("3-Quitter") 
            choix=self.usecase.Saisie("Faites un choix",1,3)
            if not str(choix).isdigit():
                self.usecase.clear()
            else:
                return choix     
    # Setters
    def setEtudiant(self, newfichierEtudiant:str) -> None:
        self.etudiants = newfichierEtudiant
        
    # Getters
    def getEtudiants(self) -> str:
        return self.etudiants
        
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
    def setId(self, newId:str) -> None:
        self.matricule = newId
    
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
        
    def setClasse(self, newClasse:str) -> None:
        self.classes.append(newClasse)

    def setModule(self, newModule: Module) -> None:
        self.modules.append(newModule)
        
    #Getters
    def getId(self) -> str:
        return self.matricule 
    
    def getNom(self) -> str:
        return self.nom    
    
    def getPrénom(self) -> str:
        return self.prénom 
          
    def getMail(self) -> str:
        return self.mail    
     
    def getTéléphone(self) -> int:
        return self.téléphone 

    def getClasse(self) -> list:
        return self.classes

    def getModule(self) -> list:
        return self.modules 

###########################################################
############### Class de la responsable admin##############
###########################################################
class ResponsableAdmin(User):
    def __init__(self, matricule: str, nom: str, prénom: str, mail: str, téléphone: int, login: str, password: str, typeP: str, classes:list = [], chargés:list = []) -> None:
        super().__init__(matricule, nom, prénom, mail, téléphone, login, password, typeP)
        self.classes = classes
        self.chargés = chargés
        self.default=DefaultUseCases()
        self.sql=MySql()
        
    def MenuResponsableAdmin(self) -> int|None:
        retour=1
        while(retour==1):
            print("1-Ajouter un professeurs")
            print("2-Lister les etudiants(Possibilité de filtre)") 
            print("3-Lister les classes") 
            print("4-Lister les chargés")
            print("5-Lister les professeurs")
            print("6-Attribuer une classe à un chargé") 
            print("7-Voir les statistiques") 
            print("8-Voir la moyenne des etudiants d'une classe") 
            print("9-Quitter") 
            choix=self.default.Saisie("Faites un choix",1,9)
            if not str(choix).isdigit():
                self.default.clear()
            else:
                return choix     
        
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
        idClasse = self.default.DoWhile("idC",classes) #type:ignore
        
        while True:
            self.listerChargés(chargés) #type:ignore
            matricule = self.default.DoWhile("Matricule",chargés) #type:ignore
            ClassesChargé = self.default.getComponentByKey("Matricule",matricule,chargés).get("Classes")

            if(idClasse not in ClassesChargé):break #type:ignore 
            else:print("La classe y est deja")
            
        newValue=str(ClassesChargé.append(idClasse))   #type:ignore 
        self.sql.updateBase("Classes",newValue,"Matricule",matricule,"Chargés")
        self.sql.updateBase("Chargé",matricule,"idC",idClasse,"Classes")
        
    # Setters
    def setClasse(self, newClasse:str) -> None:
        self.classes.append(newClasse)
        
    def setclasse(self, newChargé: Chargé) -> None:
        self.chargés.append(newChargé)
        
    # Getters     
    def getClasse(self) -> list:
        return self.classes
        
    def getChargé(self) -> list:
        return self.chargés
                
                
                
if __name__ == "__main__":
    # Application()
    Admin()