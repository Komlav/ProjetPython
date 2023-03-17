import sqlite3

BASE_FILE = "./Database.sqlite3"

class MySql:
    
    def __init__(self) -> None:
        #Connexion à la base de donnée
        self.base = sqlite3.connect(BASE_FILE)
        #Initialisation du curseur de connexion
        self.curseur = self.base.cursor()
        
        self.TABLES_USER = {
            "Admin": ["Matricule", "Nom", "Prenom", "Mail", "Telephone", "Login","Password","TypeP", "Etudiants", "Chargés", "responsableAdmin", "classes"],
            "Chargé": ["Matricule", "Nom", "Prenom", "Mail", "Telephone", "Login", "Password", "TypeP",  "Classes"],
            "Etudiants": [ "Matricule", "Nom", "Prenom", "DateNaissance", "Nationnalité", "Mail", "Téléphone", "Login", "Password", "TypeP","IdClasse", "Notes"],
            "partenaires": ["Matricule", "libelle", "Mail", "Telephone", "Login", "Password", "TypeP", "etudiants"],
            "responsableAdmin": ["Matricule", "Nom", "Prenom", "Mail", "Telephone","Login", "Password", "TypeP", "Classes", "Chargés"]
        }
        
        self.TABLES_OTHERS = {
            "filiere": ["idF","libelle","classes"], 
            "Modules": ["idM", "libelle", "classes", "professeurs", "notes"],
            "Niveau": ["idN","libelle","classes"],
            "professeurs": ["idP", "Nom", "Prenom", "mail", "Telephone", "Classes", "modules"]
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
            "ResponsableAdmin":"Matricule text, Nom text, Prenom text, mail text, Telephone number, Login text, Password text, TypeP text, classes text, Chargés text"
        }
        
        self.initTables(self.TABLES)
        
        self.datas = self.getUserData(self.TABLES_USER)
        
        #Mise à jour des changemements effectuer
        self.base.commit()
        #Fermeture de la base de donnée
        self.base.close()

    def updateBase(self):
        pass
        
    def initTables(self,tables:dict):
        with self.base:
            for key,value in tables.items():
                requete = f"CREATE TABLE IF NOT EXISTS {key}({value})"
                self.curseur.execute(requete)
                self.base.commit()

    def getTables(self,requete:str):
        with self.base:
            self.curseur.execute(requete)
            return self.curseur.fetchall()

    
    def insert(self,table:str, value:tuple):
        with self.base:
            requette = f"INSERT INTO {table} VALUES {value}"
            self.curseur.execute(requette)
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