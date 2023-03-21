-- SQLite
-- SQLite
CREATE TABLE Felrock(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(50),
    phone INTEGER
);
/*Ajout d'une nouvelle colonne dans la tablea*/
ALTER TABLE Felrock
ADD prénom VARCHAR(250);

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

ALTER TABLE USER RENAME e_mail TO mail;
