-- SQLite
-- INSERT INTO professeurs (idP, Nom, Prenom, mail, Telephone, Classes, modules)
-- VALUES 
-- (1, "BAILA", "Birane Wane", "douvewane@gmail.Com", 774561236, "[1, 2]", "[3, 5, 12]"),
-- (2, "ALY", "Aly", "aly.aly@gmail.Com", 781478523, "[1, 2]", "[11, 10]"),
-- (3, "NGOMA", "Romary", "romary.ngoma@gmail.Com", 784567852, "[1, 2]", "[7]"),
-- (4, "Lo", "Massamba", "massamba.lo@gmail.Com", 708458523, "[1]", "[2]"),
-- (5, "DIABANG", "Ndontele", "ndotele.diabang@gmail.Com", 774120033, "[1, 2]", "[4]"),
-- (6, "NDOYE", "Mohamed", "mohamed.ndoye@gmail.Com", 761594873, "[1]", "[6]"),
-- (7, "MBAYE", "Mame Diarra", "mame-diarra.mbaye@gmail.Com", 761574458, "[1]", "[8]"),
-- (8, "SAGNA", "Olivier", "olivier.sagna@gmail.Com", 787417410, "[1, 2]", "[9]"),
-- (9, "SAMB", "Kara", "kara.samb@gmail.Com", 701234567, "[1, 2]", "[13]");

-- UPDATE Classe SET professeurs = "[1,2,3,4,5,6,7,8,9]", modules = '[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,26]' WHERE idC = 1; 
-- UPDATE Classe SET professeurs = "[1,2,3,5,8,9]", modules = "[3, 4, 5, 7, 9, 11, 12, 13]" WHERE idC = 2; 
-- UPDATE Classe SET  professeurs = "[1,2,3,5,8,9]", modules = "[3, 4, 5, 7, 9, 11, 12, 13]" WHERE Libelle = "L3-ETSE"; 
-- UPDATE professeurs SET  Classes = "[1, 2, 3, 4, 5, 8]", modules = "[3, 4, 5, 7, 9, 11, 12, 13]" WHERE Libelle = "L3-ETSE"; 

-- UPDATE Classe SET idC = 4 WHERE Libelle = "L2-IAGE"; 
-- UPDATE professeurs SET  Classes = "[1, 2, 3, 4, 5, 8]", modules = "[3, 4, 5, 7, 9, 11, 12, 13]" WHERE Libelle = "L3-ETSE"; 

INSERT INTO Classe (idC, Libelle, Filiere, niveau, effectif, `chargé`, professeurs, modules, etudiants, Annee_Scolaire)
VALUES (5,	"M2-CDSD","CDSD",	"M2",	1	,""	,"[]",	'[]',"['ISM2023/DK3-0601']",	'2022-2023');
-- DELETE FROM Classe WHERE idC = 5;
-- UPDATE Classe SET idC = 5 WHERE Libelle = "M2-CDSD"; 
-- UPDATE professeurs SET  Classes = "[1, 2, 3, 4, 5, 8]", modules = "[3, 4, 5, 7, 9, 11, 12, 13]" WHERE Libelle = "L3-ETSE"; 

-- UPDATE Classe SET professeurs = "[1,2,3,5,8,9]", modules = "[3, 4, 5, 7, 9, 11, 12, 13]" WHERE Libelle = "L2-MOSIEF"; 
-- UPDATE professeurs SET  Classes = "[1, 2, 3, 4, 5, 8]", modules = "[3, 4, 5, 7, 9, 11, 12, 13]" WHERE Libelle = "L3-ETSE"; 

-- UPDATE Classe SET professeurs = "[1,2,3,5,8,9]", modules = "[3, 4, 5, 7, 9, 11, 12, 13]" WHERE Libelle = "L1-TTL"; 
-- UPDATE professeurs SET  Classes = "[1, 2, 3, 4, 5, 8]", modules = "[3, 4, 5, 7, 9, 11, 12, 13]" WHERE Libelle = "L3-ETSE"; 

-- UPDATE Modules SET classes = "[1]" WHERE Session = 4; 
-- UPDATE Modules SET professeurs = "[1]", classes = "[1,2]" WHERE idM = 3; 
-- UPDATE Modules SET professeurs = "[5]", classes = "[1,2]" WHERE idM = 4; 
-- UPDATE Modules SET professeurs = "[1]", classes = "[1,2]" WHERE idM = 5; 
-- UPDATE Modules SET professeurs = "[6]", classes = "[1]" WHERE idM = 6; 
-- UPDATE Modules SET professeurs = "[3]", classes = "[1,2]" WHERE idM = 7; 
-- UPDATE Modules SET professeurs = "[7]", classes = "[1]" WHERE idM = 8; 
-- UPDATE Modules SET professeurs = "[8]", classes = "[1,2]" WHERE idM = 9; 
-- UPDATE Modules SET professeurs = "[2]", classes = "[1]" WHERE idM = 10; 
-- UPDATE Modules SET professeurs = "[2]", classes = "[1,2]" WHERE idM = 11; 
-- UPDATE Modules SET professeurs = "[1]", classes = "[1,2]" WHERE idM = 12; 
-- UPDATE Modules SET professeurs = "[9]", classes = "[1,2]" WHERE idM = 13; 

-- UPDATE Classe SET chargé = "ISM2023/staff2-0602" WHERE idC = 2; 
-- INSERT INTO `Chargé` (Matricule, Nom, Prenom, mail, Telephone, Login, Password, TypeP, Classes)
-- VALUES ("ISM2023/staff2-0602",	"SARR",	"Bernard",	"bernard.sarr@groupeism.sn",	774587515,"bernard.sarr@groupeism.sn",	"passer@123",	"Chargé",	"[2]");

-- UPDATE Filiere SET classes = "[1]" WHERE idF = 0; 
-- UPDATE Filiere SET classes = "[2]" WHERE idF = 2; 


-- INSERT INTO partenaires (id, libelle, mail, Telephone, Login, Password, TypeP)
-- VALUES 
-- (1, "Institu Supérieur d'Informatique", "isi.groupe@edu.sn", 774102589, "isi.groupe@edu.sn", "passer@123", "partenaire"),
-- (2, "BEM Management School", "bem.groupe@edu.sn", 78452820, "bem.groupe@edu.sn", "passer@123", "partenaire"),
-- (3, "IAM", "iam.groupe@edu.sn", 701472589, "iam.groupe@edu.sn", "passer@123", "partenaire");