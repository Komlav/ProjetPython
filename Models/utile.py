# from DataBase.sql import *

class DefaultUseCases:
    
    
    
    
        
    
    

data = {}
def connect(login:str, password:str,data:dict)-> tuple:
    for user in data:
        if (login == user.get("login") and password == user.get("password")):
            if (Role == user.get('role')):
                if (user.get("etat") == 1):
                    return user
                else:
                    clear()
                    showMsg("Vous avez ete bloque !",0,1)
                    os.system("pause")
                    return {}
            else:
                clear()
                showMsg("Vous pouvez pas acceder a cette partie !",0,1)
                os.system("pause")
                return {}
    clear()
    showMsg("Login et/ou mot de passe est/sont incorrect !",0,1)
    return {}