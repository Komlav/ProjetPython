"╦---------------------------------------------------------------------------╗"
"|                           Commentaires                                    |"
"╬---------------------------------------------------------------------------╣"
"|                              14/05/2023                                   |"
"| Commentaire Chargé                                                        |"
"| l'heure du commentaire                                                    |"
"|                                                    Commentaire etudiant   |"
"|                                                    l'heure du commentaire |"
"|                                                                           |"
"|                                                                           |"
"|                                                                           |"
"|                                                                           |"
"|                                                                           |"
"|                                                                           |"
"|                                                                           |"
"|                                                                           |"
"|                                                                           |"
"----------------------------------------------------------------------------╣"
l = "Bonjour Madame comment allez vous ? Bonjour Madame comment allez vous ?Bonjour Madame comment allez vous ?Bonjour Madame comment allez vous ?Bonjour Madame comment allez vous ?Bonjour Madame comment allez vous "
CHAT_LENGHT = 50
TAILLE_SCREEN = 100
BLUE = ""


def chatLeftt( texte: str):
    text = texte.split(" ")
    ligne = ''
    for mot in text:
        ligne += mot + ' '
        if len(ligne) <= CHAT_LENGHT: continue
        else:
            print(f"| {BLUE}{ligne:<{TAILLE_SCREEN-3}} |")
            ligne = ""
            
chatLeftt(l)