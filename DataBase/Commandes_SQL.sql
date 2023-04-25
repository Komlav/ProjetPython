-- Commande runner
DROP TABLE Felrock;
CREATE TABLE Felrock(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    libelle VARCHAR(150),
    prénom VARCHAR(250) UNIQUE NOT NULL ,
    mail VARCHAR(255),
    telephone INTEGER,
    login varchar(255),
    password  varchar(150),
    typeP varchar(150)
);
/*Ajout d'une nouvelle colonne dans la tablea*/
-- ALTER TABLE Felrock
-- ADD prénom VARCHAR(250) UNIQUE NOT NULL  ;

/*Renommez la colonne phone en telephone*/
ALTER TABLE user
    RENAME phone TO telephone;

/*Insérer dans la table une nouvelle utilisateur*/
INSERT INTO USER
VALUES(2, "BALARABE", 774521896, "Mariam");

/*Modifier le nom du user mariam*/
UPDATE USER
SET "prénom" = "Mariama"
WHERE id = 2;

UPDATE USER
SET "prénom" = "Felrock Komlavi",
    "nom" = "TAMAKLOE"
WHERE id = 1;

/*Ajout d'une nouvelle colonne a la table*/
ALTER TABLE USER
ADD e_mail VARCHAR(150);

UPDATE USER
SET "e_mail" = "felrockkomlavi@gmail.com"
WHERE id = 1;

UPDATE USER
SET "mail" = "hadji-mariam.balarabe@ism.edu.sn"
WHERE id = 2;

ALTER TABLE USER RENAME mail TO mail;
