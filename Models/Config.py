# ================================== Queslques constantes =============================== #

tab = '\t'
push = '\t'*4
DEFAULT_PASSWORD = "passer@123"
DEFAULT_EFFECTIF = 40
TAILLE_SCREEN = 150
BASE_FILE = "./DataBase/Database.sqlite3"
FOLDER_FILE = "DataBase/JSONS/Students_Marks.json"
FOLDER_CHARGES_FILE = "DataBase/JSONS/Chargés.json"
CHAT_LENGHT = TAILLE_SCREEN // 2 - 10


EGALE = "="

POLICES = ['avatar', 'banner', 'banner3-D', 'banner3', 'banner4', 'big', "isometric3", 'bulbhead']



# ================================== Users Functions =============================== #
RP_USECASES = {
    "main": ["Ajouter un nouveau", "Voir toutes les listes", "Modifier un élément","Supprimer","Plus", "Se déconnecter"],
    "add": ["Ajouter un professeurs", "Ajouter un module", "Ajouter une filière"],
    "liste": ["Lister les professeurs", "Lister les modules", "Lister les filières", "Lister les chargés", "Lister les niveaux", "Lister les étudiants", "Liste des partenaires", "Menu général"],
    "delete": ["Supprimer un chargé","Supprimer un Professeur", "Supprimer un module", "Supprimer un partenaire"],
    "more": ["Attribuer des classes aux chargés","Modifier un chargé", "Voir la moyenne des etudiants d'une classe","Voir les statistiques", "Menu general"],
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
    "main": ["Ajouter un nouveau", "Voir toutes les listes", "Supprimer un Responsable", "Se déconnecter"],
    "add": ["Ajouter un étudiant","Ajouter un(e) chargé","Ajouter un(e) responsable","Ajouter un partenaire", "Retourner au menu général"],
    "liste" : ["Lister les étudiants", "Lister les chargé(e)s", "Lister les responsables","Lister les partenaires", "Retourner au menu général"],
    "delete": ["Suppression du responsable Administratif", "Menu général"]
}

CHARGE_USECASE={
    "main":["Lister un profil","Voir les notes","Modifier un élément","Initier Les notes d'un module","Commentaire","Supprimer un etudiant", "Se deconnecter"],
    "Liste":["Lister les etudiants par Classe","Lister les professeurs", "Menu général"],
    "notes":["Notes d'une Classe","Notes d'un etudiant", "Menu général"],
    "edit":["Modifier les notes d'une classe","Modifier les notes d'un etudiant", "Modifier un etudiant", "Menu général"],
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
