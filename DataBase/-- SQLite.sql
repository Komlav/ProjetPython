-- SQLite
CREATE TABLE Felrock(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(50),
    phone INTEGER
);
/*Ajout d'une nouvelle colonne dans la tablea*/
ALTER TABLE Felrock ADD prénom VARCHAR(250);

/*Renommez la colonne phone en telephone*/
ALTER TABLE user RENAME phone TO telephone;

/*Insérer dans la table une nouvelle utilisateur*/
INSERT INTO USER VALUES(2,"BALARABE", 774521896, "Mariam");

/*Modifier le nom du user mariam*/
UPDATE USER SET "prénom" = "Mariama" WHERE id = 2;
UPDATE USER SET "prénom" = "Felrock Komlavi", "nom" = "TAMAKLOE" WHERE id = 1;