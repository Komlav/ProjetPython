-- SQLite
DROP TABLE partenaires;

CREATE TABLE partenaires(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Libelle VARCHAR(150),
    Mail VARCHAR(255),
    Telephone INTEGER,
    Login varchar(255),
    Password  varchar(150),
    TypeP varchar(150)
);

INSERT INTO partenaires(Libelle,Mail, Telephone, Login,PassWord,TypeP) VALUES("ucad","ucad@edu.sn",782547144,"ucad@edu.sn","passer@123", "Partenaire");