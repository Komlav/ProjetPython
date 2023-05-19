while True:
        #     all_Data = self.usecase.loadStudentsFolder(FOLDER_FILE)
        #     student_commentaire = all_Data.get(f"{self.matricule}")[-1]["Commentaire"] #type: ignore
            
        #     self.usecase.ligneMenu(2, TAILLE_SCREEN, 'haut')
        #     print(f"| {BLUE}{'Commentaires':^{TAILLE_SCREEN-3}} |")
        #     self.usecase.ligneMenu(2, TAILLE_SCREEN, 'milieu')
        #     i, show = 0, True
        #     for commentaire in student_commentaire:
        #         if i == 0: print(f"| {YELLOW}{commentaire['Date']:^{TAILLE_SCREEN-3}} |")
        #         if student_commentaire[i-1]["Date"] != student_commentaire[i]["Date"] and i != 0:
        #             print(f"| {YELLOW}{commentaire['Date']:^{TAILLE_SCREEN-3}} |")
        #         i += 1
                    
        #         if commentaire["Auteur"] == self.matricule:
        #             self.usecase.chatRight(commentaire["Commentaire"])
        #             print(f"| {commentaire['Heure']:>{TAILLE_SCREEN-3}} |")
        #         else:    
        #             self.usecase.chatLeft(commentaire["Commentaire"])
        #             print(f"| {commentaire['Heure']:<{TAILLE_SCREEN-3}} |")
        #         if i == len(student_commentaire):
        #             self.usecase.ligneMenu(2, TAILLE_SCREEN, 'bas')

        #     # Envoie d'un nouveau commentaire
        #     commentaire = input("Entrez un nouveau commentaire (ou -1 pour quitter)")
        #     if commentaire != '-1':
        #         date = self.usecase.CurrentDate()
                
        #         newSend = {'Date': f"{date[2]}-{date[1]}-{date[0]}", 'Heure': date[]}
        