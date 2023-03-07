# Projet-Python : Gestion des notes

## Les acteurs et leurs fonctionnalités:
- **Un étudiant**
    - Se connecter
    - Voir ses notes
    - Faire une réclammation ou un commentaire sur ses notes
    - Modifier son profil

- **La chargé de classe** 
    - Se connecter
    - Voir toutes les notes d'une classe
    - Voir les notes d'un étudiant
    - Modifier les notes d'une classe ou d'un étudiant
    - Voir les commentaires et réclammations
    - Faire un commentaire 
    - Modifier son profil

- **Les écoles partenaires**
    - Se connecter
    - Consulter le dossier d'un étudiant

- **Le responsable administratif**
    - Se connecter 
    - Voir les notes des classes
    - Attribuer des classes aux chargés
    - Voir les statistiques des classes et du batiment 

- **Admin**
    - Se connecter
    - Ajouter un étudiant 
    - Ajouter une chargé
    - Ajouter un responsable administratif

## Les entités:
- **Un étudiant**
    - Matricule
    - Nom complet
    - Date de naissance
    - Nationnalité
    - Niveau
    - Classe
    - Filière
    - Ses Notes
    - Son mail
    - Son login et mot de passe
    - Téléphone
    - Profil

- **La chargé de classe**
    - Matricule
    - Nom complet
    - Mail
    - Login et password
    - Classes
    - Téléphone
    - Profil

- **Le responsable administratif**
    - Matricule
    - Nom complet
    - Mail
    - Téléphone
    - Login et password
    - Classes
    - Profil

- **Une classe**
    - Id
    - Libelle
    - Filière
    - Niveau
    - Effectif
    - Notes
    - Professeurs
    - Chargé de classe

- **Module**
    - Id
    - Libelle

- **Professeur**
    - Id 
    - Nom complet
    - Mail
    - Téléphone
    - Modules
    - Classes
    - Profil

- **Niveau**
    - Id
    - Libelle

- **Filière**
    - Id
    - Libelle

- **Note**
    - Module
    - Etudiant
    - Libelle (note elle même)

- **Profil**
    - Id
    - Libelle