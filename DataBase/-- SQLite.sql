-- SQLite
CREATE TABLE Felrock(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom VARCHAR(50),
    phone INTEGER
);

ALTER TABLE Felrock ADD prénom VARCHAR(250);

ALTER TABLE user RENAME phone TO telephone;

 