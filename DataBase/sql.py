import sqlite3
from constante import *
# ---------------Connexion-------------------



# etablir la connection,si le fichier de la db n'existe pas il le cree
data=sqlite3.connect('./Database.sqlite3')

tables={"Etudiants":"Matricule text,Nom text,Prenom text,DateNaissance text,Nationnalité text,Mail text,Telephone number,Login text,PassWord text,TypeP text,IdClasse number,Notes text",
    "Chargé":"Matricule text,Nom text,Prenom text,mail text,Telephone number,Login text,Password text,TypeP text, Classes text",
    "Admin":"Matricule text,Nom text,Prenom text,mail text,Telephone number,Login text,Password text,TypeP text,Etudiants text,Chargés text,responsableAdmin text,classes text",
    "filiere":"idF number,libelle text,classes text",
    "Modules":"idM number,libelle text,classes text,professeurs text,notes text",
    "Niveau":"idN number,libelle text,classes text",
    "partenaires":"Matricule text,libelle text,mail text,Telephone number,Login text,Password text,TypeP text,etudiants text",
    "professeurs":"idP number,Nom text,Prenom text,mail text,Telephone number,Classes text,modules text",
    "responsableAdmin":"Matricule text,Nom text,Prenom text,mail text,Telephone number,Login text,Password text,TypeP text,classes text,Chargés text"}

curseur=data.cursor()

def initTables(tables:dict):
    for key,value in tables.items():
        requete=f"CREATE TABLE IF NOT EXISTS {key}({value})"
        curseur.execute(requete)

def getTables(requete:str):
    curseur.execute(requete)
    return curseur.fetchall()

# TABLE=curseur.execute("SELECT name FROM sqlite_master")
# TABLE.fetchall()
# print(getTables("SELECT name FROM sqlite_master"))


# requete=f"INSERT INTO Admin values('adm_1','Mohamed','SANGARE','mohamed.sangare@ism.edu.sn',777777777,'mohasang13','passer','{TYPEP[0]}','[]','[]','[]','[]')"

# curseur.execute(requete)
# data.commit()

# print(getTables("SELECT * from Admin "))


TABLES_USER = {
    "Admin": ["Matricule", "Nom", "Prenom", "mail", "Telephone", "Login","Password","TypeP", "Etudiants", "Chargés", "responsableAdmin", "classes"],
    "Chargé": ["Matricule", "Nom", "Prenom", "mail", "Telephone", "Login", "Password", "TypeP",  "Classes"],
    "Etudiants": [ "Matricule", "Nom", "Prénom", "DateNaissance", "Nationnalité", "Mail", "Téléphone", "Login", "Password", "TypeP","IdClasse", "Notes"],
    "partenaires": ["Matricule", "libelle", "mail", "Telephone", "Login", "Password", "TypeP", "etudiants"],
    "responsableAdmin": ["Matricule", "Nom", "Prenom", "mail", "Telephone", "number", "Login", "Password", "TypeP", "classes", "Chargés"]
}


def getUserData(tables:dict) -> dict:
    #Initialisation du dictionnaire qui va contenir les users
    data = dict()
    
    #Pourcourt de la table des users
    for key, value in tables.items():
        
        #Initialisation d'un liste de chaque table
        table_list = []
        
        #Exécution de la requette
        request = f"SELECT * FROM {key}"
        curseur.execute(request)
        
        #Parcourt de la liste de donnée de chaque table
        for user in curseur.fetchall():
            
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
    
print(getUserData(TABLES_USER))

# fermer la connection
data.close()
