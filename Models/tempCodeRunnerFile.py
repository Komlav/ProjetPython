
# import ProjetPython.DataBase.sql as m


# from Admin import Admin
# DEFAULT_PASSWORD = "passer@123"

# class DefaultUseCases:
#     def __init__(self) -> None:
#         self.all_User_Data = m.MySql().datas #Données des utilisateurs.
#         self.all_Other_Data = {} #Données des filières et autres infos
        

#     def connect(self, login:str, password:str)-> dict:
#         for liste_user in self.all_User_Data.values():
#             for user in liste_user:
#                 if (login == user.get("Login") and password == user.get("Password")):
#                     return user
#         return {}
    
# class AdminUseCases(Admin):
#     #Use case d'ajout
#     # - Etudiant
#     # - Chargé
#     # - Responsable Adminstratif
#     # - Partenaires
    
#     def __init__(self, admin_data:dict) -> None:
#         super().__init__(admin_data.get("Matricule"),admin_data.get("Nom"),admin_data.get("Prénom"),admin_data.get("Mail"),admin_data.get("Téléphone"),admin_data.get("Login"),admin_data.get("Password"),admin_data.get("TypeP"),admin_data.get("Etudiants"),admin_data.get("Chargés"),admin_data.get("ResponsableAdmin"), admin_data.get("Partenaires")) # type: ignore
        
#     def addNewEtudiant(self, newEtu:dict):
#         self.setEtudiant(newEtu)
#         mail_Etu = f"{newEtu.get('Prénom').replace(' ' ', '-'').lower()}.{newEtu.get('Nom').lower()}@ism.edu.sn" # type: ignore
        
#         Etudiant = (
#             newEtu.get("Matricule"),
#             newEtu.get("Nom"),
#             newEtu.get("Prénom"),
#             newEtu.get("DateNaissance"),
#             newEtu.get("Nationnalité"),
#             mail_Etu, #Mail etudiant
#             newEtu.get("Téléphone"),
#             mail_Etu, #Login etudiant
#             DEFAULT_PASSWORD,
            
#             )
#         # MySql.insert()
        

# a = AdminUseCases({})
