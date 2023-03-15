
import sqlite3
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
print(getTables("SELECT name FROM sqlite_master"))


# for table in getTables():
#     print(table)

# fermer la connection
data.close()