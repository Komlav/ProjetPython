# Projet-Python : Gestion des notes

## Les acteurs et leurs fonctionnalités

- **Un étudiant**
  - Se connecter
    - Voir ses notes
    - Voir ses commentaires
    - Faire une réclammation ou un commentaire sur ses notes

- **La chargé de classe**
  - Se connecter
  - Lister les étudiants par classe
  - Voir toutes les notes des étudiants d'une classe
  - Voir les notes d'un étudiant
  - Modifier les notes d'une classe ou d'un étudiant
  - Voir les commentaires et réclammations
  - Faire un commentaire

- **Les écoles partenaires**
  - Se connecter
  - Lister les étudiants
  - Consulter le dossier d'un étudiant

- **Le responsable administratif**é00
  - Se connecter
  - Voir la moyenne des etudiants d'une classe/ de la classe
  - Lister tous les étudiants -> Filière, classe, niveau,nationnalité
  - Lister les classes
  - Lister les chargés
  - Attribuer des classes aux chargés
  - Voir les statistiques des classes et de la filiere

- **Admin**
  - Se connecter
  - Lister et Ajouter un étudiant / les étudiants
  - Lister et Ajouter une chargé / les chargés
  - Lister et Ajouter un responsable administratif / responsable administratif

## Les entités

- **User**
  - Matricule
  - Nom
  - Prénom
  - Mail
  - Téléphone
  - Login
  - Password
  - TypeP

- **Un étudiant**
  - Matricule
  - Nom complet
  - Date de naissance
  - Nationnalité
  - Classe
  - Ses Notes
  - Son mail
  - Son login et mot de passe
  - Téléphone
  - Type

- **Partenaire**
  - Id
  - Libelle
  - Mail
  - Login
  - Password
  - Téléphone

- **La chargé de classe**
  - Matricule
  - Nom complet
  - Mail
  - Login et password
  - Classes
  - Téléphone
  - Type

- **Le responsable administratif**
  - Matricule
  - Nom complet
  - Mail
  - Téléphone
  - Login et password
  - Classes
  - Type

- **Une classe**
  - Id
  - Libelle
  - Filière
  - Niveau
  - Effectif
  - Etudiants
  - Modules
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

- **Type**
  - Id
  - Libelle
