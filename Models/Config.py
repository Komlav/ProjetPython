# ================================== Queslques constantes =============================== #

tab = '\t'
push = '\t'*4
DEFAULT_PASSWORD = "passer@123"
DEFAULT_EFFECTIF = 40
TAILLE_SCREEN = 150
BASE_FILE = "./DataBase/Data.sqlite3"
FOLDER_FILE = "DataBase/JSONS/Students_Marks.json"
FOLDER_CHARGES_FILE = "DataBase/JSONS/Chargés.json"
CHAT_LENGHT = TAILLE_SCREEN // 2 - 10


EGALE = "="

POLICES = ['avatar', 'banner', 'banner3-D', 'banner3', 'banner4', 'big', "isometric3", 'bulbhead']



# ================================== Users Functions =============================== #
RP_USECASES = {
    "main": ["Ajouter un nouveau", "Voir toutes les listes", "Modifier un chargé","Supprimer","Plus", "Se déconnecter"],
    "add": ["Ajouter un professeurs", "Ajouter un module", "Ajouter une filière", "Menu général"],
    "liste": ["Lister les professeurs", "Lister les modules", "Lister les filières", "Lister les chargés", "Lister les niveaux", "Lister les étudiants", "Liste des partenaires", "Menu général"],
    "delete": ["Supprimer un chargé","Supprimer un Professeur", "Supprimer un module", "Supprimer un partenaire","Menu général"],
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
    "main":["Lister un profil","Gérer les notes","Modifier un élément", "Commentaire","Supprimer un etudiant", "Se deconnecter"],
    "Liste":["Lister les etudiants par Classe","Lister les professeurs", "Menu général"],
    "notes":["Gérer les notes", "Menu général"],
    "edit":["Modifier les notes d'une classe","Modifier les notes d'un etudiant", "Modifier un etudiant", "Menu général"],
    "insert":["Pour une classe","Pour un etudiant","Menu général"],
    "commentaire":["Envoyer à une classe", "Envoyer à un étudiant","Menu général"]
}

PARTENAIRE_USECASES = {
    "main":["Consulter le dossier d'un etudiant", "Se deconnecter"],
    "dossier":["Menu général"]
}

ETUDIANT_USECASE={
    "main":["Voir mes notes","Commentaire","Se deconnecter"],
    "commentaire":["Faire un commentaire","Voir mes commentaires"]
}

# Session_1 = {
#     "Algorithmique et Langages de Programmation":	[2,	3],
#     "Business English 1":	[2,	2],
#     "CISCO IT Essentials 1 PC Harware & Software":	[2,	2],
#     "Comptabilité Générale 1":	[2,	3],
#     "Conception Graphique et Multimédia 1":	[2,	2],
#     "Droit du Numérique":	[1,	2],
#     "Fondamentaux du Management":	[1,	2],
#     "Informatique Appliquée":	[2,	2],
#     "Leadership - Dév. Personnel - Techniques d'enquete - Actions de Recherche Encadrées (ARE)":	[1,	2],
#     "Marketing 1: Concepts Fondamentaux & Comportement du Consommateur":	[1,	2],
#     "Statistiques Descriptives":	[2,	2],
#     "Technologies Web 1: HTLM5 - CSS3":	[2,	2],
#     "Théories des Systèmes d'Exploitation": [2,2]
# }

# Session_2 = {
    # Algorithmique et Langages de Programmation	19,00	19,00
    # Business English 1	13,00	13,00
    # CISCO IT Essentials 1 PC Harware & Software	17,00	19,00
    # Comptabilité Générale 1	17,00	15,50
    # Conception Graphique et Multimédia 1	16,00	17,00
    # Droit du Numérique	17,00	17,00
    # Fondamentaux du Management	12,50	12,50
    # Informatique Appliquée	18,00	18,00
    # Leadership - Dév. Personnel - Techniques d'enquete - Actions de Recherche Encadrées (ARE)	15,00	15,00
    # Marketing 1: Concepts Fondamentaux & Comportement du Consommateur	19,00	19,00
    # Statistiques Descriptives	15,50	15,50
    # Technologies Web 1: HTLM5 - CSS3	18,00	18,00
    # Théories des Systèmes d'Exploitation
# }
# Session_3 = {
#         "Administration Système Windows": [2, 3],
#         "Algo Avancée & Structures de Données": [2, 4],
#         "Analyse Combinatoire et Lois de Probabilité": [2, 2],
#         "Analyse et Conception 1 (UML)": [2, 3],
#         "Architecture des Réseaux Informatiques: Certification CISCO CCNA": [2, 2],
#         "Business English": [2, 2],
#         "Electronique Digitale": [1, 2],
#         "Entrepreneurship: Atelier Build Your Business (BYB)": [2, 3],
#         "Programmation C": [2, 2],
#         "Programmation Objet 2: Python": [2, 2],
#         "Programmation Web 1:, PhP": [2, 2],
#         "Systèmes de Gestion de Bases de Données": [2, 2]
# }
# Session_4 = {
# "Business English 4": [2, 2, 3],
# "AGORA - Soft Skills & Grands Projets": [3, 4, 9],
# "Mathématiques Appliquées: Analyse 2 - Algèbre 2": [2, 3, 5],
# "Recherche Opérationelle": [1, 2, 5],
# "Administration Systèmes Linux": [2, 2, 4],
# "Electronique Digitale 2": [1, 2, 7],
# "Architecture des Réseaux Informatiques: Certification CISCO CCNA 1-2": [1, 2, 6],
# "Algo Avancée & Structures de Données 2": [2, 3, 1],
# "Programmation Objet 3: Python": [1,2, 2 ],
# "Programmation Objet 4: C++": [1, 2, 2],
# "Programmation Objet 5: JAVA": [2, 2, 1], 
# "Analyse et Conception 2": [2, 2, 1],
# "Technologies Web 3: PhP/MySQL": [2, 2, 1]
# }
# s = sqlite3.connect(BASE_FILE)
# c = s.cursor()
# i = 14
# for libelle, data in Session_1.items():
#     c.execute(f"INSERT INTO Modules (idM, libelle, classes, professeurs,notes, coefficient, credit, Session) VALUES ({i}, \"{libelle}\", '[2]', '[]', '[]', {data[0]},  {data[1]}, 1)")
#     i += 1
#     s.commit()
