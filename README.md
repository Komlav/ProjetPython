# Projet-Python : Gestion des notes et du personel 
## Description du projet
  Le projet porte sur la gestion totale du Personnel et des notes des etudiants d'un Etablissement Universitaire.
## Les fonctionnalités par acteur
### L'administrateur:
> - Ajouter,lister les profils et supprimer le responsable administratif
> - Se connecter et se déconnecter

### Login des profils:
  -Admin:mohamed.sangare@groupism.sn
  -Responsable Administratif:mame-diarra.mabaye@groupeism.sn
  -Chargé de classe:astou.diagne@groupeism.sn
  -Etudiant:hadjia-mariama.balarabe@ism.edu.sn |matriculeEtudiant:ISM2023/DK33-0609(si vous voulez voir son dossier avec le profil Partenaire)
  -Partenaire:isi.groupe@edu.sn
## NB:
  MEME PASSWORD POUR TOUS LES PROFILS: "passer@123"



## Les acteurs et leurs fonctionnalités

- **Un étudiant**
  - Se connecter✅
  - Voir ses notes✅
  - Voir et faire des commentaires✅

- **La chargé de classe**
  - Se connecter✅
  - Lister les étudiants par classe✅
  - Voir toutes les notes des étudiants d'une classe✅
  - Voir les notes d'un étudiant✅
  - Modifier les notes d'une classe ou d'un étudiant✅
  - Voir les commentaires et réclammations✅
  - Faire un commentaire✅
  - Lister les professeurs✅

- **Les écoles partenaires**
  - Se connecter✅
  - Consulter le dossier d'un étudiant✅

- **Le responsable administratif**
  - Se connecter✅
  - Lister tous les étudiants -> Filière, classe, niveau,nationnalité ✅
  - Lister les classes✅
  - Lister les chargés✅
  - Ajouter et lister un prof✅
  - Ajouter et lister un modules✅
  - Ajouter et lister une filières✅
  - Attribuer des classes aux chargés✅
  - Voir la moyenne des etudiants d'une classe et de la classe her self ✅
  - Voir les statistiques des classes ✅ et de la filiere :Stat des Classes:forte et faible moyenne, moyenne de la classe, nbre Etu ayant validé ou Non le semestre  ==Stat  des Classes (filtrées par Filiere) 

- **Admin**
  - Se connecter✅
  - Lister et Ajouter un étudiant / les étudiants✅
  - Lister et Ajouter une chargé / les chargés✅
  - Lister et Ajouter un responsable administratif / responsable administratif✅
  - Lister et Ajouter un partenaire✅

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


  ## Modules et bibliothèques utilisées:
--------------
## *1- Colorama*
> Module qui nous a permis de mettre la couleur dans le script.
> Documentation [Colorama]()

## *2- Tabulate* 
> Module permettant l'affichage des donnée dans des tableaux.
> Documentation sur la bibliothèque [Tabulate](https://pypi.org/project/tabulate/)
## *2- PyFliglet* 
> Module permettant un autre affichage
> Documentation sur la bibliothèque [PyFliglet](http://www.figlet.org/examples.html)


### Tableau des caractères ascii utilisé
documentation[ASCII](https://www.ascii33.com/liste-tables-ascii/table-ascii-etendue-EOM.html)

## Tableau des fichiers utiliser dans le projet et leur contenus...
---
| Fichier           | Commentaire                                                                  |
| ----------------- | ---------------------------------------------------------------------------- |
| `Data.sqlite` | Base de donnée de l'application qui regroupe l'ensemble des données                      |
| `All_Classes.py`  | Fichier qui contients l'ensemble des classes et fonctionnalités              |
| `App.py`          | Fichier principal de l'application                                           |
| `Conception du projet.mdj`| Fichier de conception de l'application                               |


