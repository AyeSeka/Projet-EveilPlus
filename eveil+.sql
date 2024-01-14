CREATE DATABASE eveil_plus;
USE eveil_plus;
CREATE TABLE Repetiteur (
    IdRepetiteur INT PRIMARY KEY IDENTITY(1,1),
    NomRepetiteur VARCHAR(30) NOT NULL,
    PrenomRepetiteur VARCHAR(55) NOT NULL,
    DateNaissance date,
    lieu_hab_rep VARCHAR(55),
    AnneeExperience INT ,
    NiveauRepetiteur VARCHAR(10),
    EstActif BIT
);

CREATE TABLE MatiereSciences (
    IdMatiereSciences INT PRIMARY KEY IDENTITY(1,1),
    NomMatiereSciences VARCHAR(170) NOT NULL,
);

CREATE TABLE MatiereLitteraire (
    IdMatiereLitteraire INT PRIMARY KEY IDENTITY(1,1),
    NomMatiereLitteraire VARCHAR(170) NOT NULL,
);

CREATE TABLE Dispense (
    IdDispense INT PRIMARY KEY IDENTITY(1,1),
    IdRepetiteur int,
	FOREIGN KEY(IdRepetiteur) REFERENCES Repetiteur(IdRepetiteur),
	Matiere VARCHAR(255) NULL,
	Classe VARCHAR(255) NULL
);

--select * from ContratTemporaire

--select * from HistoriquePoste H JOIN Poste P ON H.IdPoste=P.IdPoste
--SELECT  * FROM Repetiteur r JOIN users u ON r.IdUser=u.IdUser JOIN Dispense d ON r.IdRepetiteur=d.IdRepetiteur join Competence c ON (r.IdCompetence = c.IdCompetence) WHERE  1=1

--select * from Parent P JOIN users u ON P.IdUser=u.IdUser

--SELECT * FROM Candidature C JOIN HistoriquePoste H on C.IdHistoriquePoste = H.IdHistoriquePoste JOIN Poste P ON H.IdPoste=P.IdPoste JOIN Repetiteur R ON C.IdRepetiteur=R.IdRepetiteur join Competence Cpt ON (R.IdCompetence = Cpt.IdCompetence) JOIN users U ON R.IdUser=U.IdUser
--SELECT  * FROM Repetiteur r JOIN users u ON r.IdUser=u.IdUser JOIN Dispense d ON r.IdRepetiteur=d.IdRepetiteur join Competence c ON (r.IdCompetence = c.IdCompetence)

--SELECT * FROM Dispense D join Repetiteur R on D.IdRepetiteur=R.IdRepetiteur
--SELECT R.*, NomCompetence, U.*, D.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence JOIN Dispense D on D.IdRepetiteur=R.IdRepetiteur


insert into MatiereSciences (NomMatiereSciences) values ('Maths'),
														('P-Chemie'),
														('SVT'),
														('Hist-Geo')

insert into MatiereLitteraire (NomMatiereLitteraire) values ('Français'),	
														('Anglais'),
														('Allemand'),
														('Espagnol'),
														('Phylosophie')


CREATE TABLE ClassePrimaire (
    IdClassePrimaire INT PRIMARY KEY IDENTITY(1,1),
    NomClassePrimaire VARCHAR(255) NOT NULL,
);

insert into ClassePrimaire (NomClassePrimaire) values ('CP1'),
													('CP2'),
													('CE1'),
													('CE2'),
													('CM1'),
													('CM2')


CREATE TABLE ClasseCollege (
    IdClasseCollege INT PRIMARY KEY IDENTITY(1,1),
    NomClasseCollege VARCHAR(255) NOT NULL,
);

insert into ClasseCollege (NomClasseCollege) values ('6ième'),
													('5ième'),
													('4ième'),
													('3ième')


CREATE TABLE ClasseLycee (
    IdClasseLycee INT PRIMARY KEY IDENTITY(1,1),
    NomClasseLycee VARCHAR(255) NOT NULL,
);

insert into ClasseLycee (NomClasseLycee) values ('2ndA'),
												('2ndC'),
												('1ièmeA'),
												('1ièmeD'),
												('1ièmeC'),
												('TleA'),
												('TleD'),
												('TleC')


--SELECT  * FROM Repetiteur r join Competence c ON (r.IdCompetence = c.IdCompetence)

CREATE TABLE Competence (
    IdCompetence INT PRIMARY KEY IDENTITY(1,1),
    NomCompetence VARCHAR(55) NOT NULL
);

insert into Competence (NomCompetence) values ('Sciences'),
												('Litterature'),
												('Sciences et Litterature')

ALTER TABLE Repetiteur   
ADD IdCompetence int,
FOREIGN KEY(IdCompetence) REFERENCES Competence(IdCompetence),
	IdUser int,
FOREIGN KEY(IdUser) REFERENCES users(IdUser);

CREATE TABLE Parent(
	IdParent int primary key IDENTITY(1,1),
	NomParent varchar(20) NULL,
	PrenomParent varchar(55) NULL,
	LieuHabitation varchar(55) NULL,
	TelephoneParent1 varchar(15) NULL,
	TelephonePparent2 varchar(15) NULL,
	);
ALTER TABLE Parent   
ADD IdUser int,
FOREIGN KEY(IdUser) REFERENCES users(IdUser)

create table users(
	IdUser INT PRIMARY KEY IDENTITY(1,1),
	Email VARCHAR(30) not null unique,
	mot_de_passe VARCHAR(255) not null,
	confirm_mot_de_passe varchar(255) NULL,
	Roles VARCHAR(30) not null,
	path_PhotoProfil VARCHAR(255)
)




CREATE TABLE Personnel_Eveil (
    IdPersoEveil INT PRIMARY KEY IDENTITY(1,1),
    NomPersoEveil VARCHAR(25),
    PrenomPersoEveil VARCHAR(55),
    Telephone VARCHAR(15),
    Adresse VARCHAR(55)
);
ALTER TABLE Personnel_Eveil   
ADD IdUser int,
FOREIGN KEY(IdUser) REFERENCES users(IdUser)

CREATE TABLE Produits (
    IdProduits INT PRIMARY KEY IDENTITY(1,1),
    NomProduits VARCHAR(55) not null,
    DesciptionProduits VARCHAR(55) not null,
    Prix FLOAT not null,
	IdCategorie int,
	FOREIGN KEY(IdCategorie) REFERENCES CategorieProduits(IdCategorie),
    path_photo_Produits VARCHAR(255)
    
);


CREATE TABLE CategorieProduits (
    IdCategorie INT PRIMARY KEY IDENTITY(1,1),
    NomCategorie VARCHAR(30)
);

CREATE TABLE Commande (
    IdCommande INT PRIMARY KEY IDENTITY(1,1),
    DateCommande DATETIME,
    Montant FLOAT,
);

--CREATE TABLE Paiement_Repetiteur (
--    id_paiement_repetiteur INT PRIMARY KEY IDENTITY(1,1),
--    date_paiement_repetiteur DATETIME,
--    montant_paiement_repetiteur FLOAT,
--);



CREATE TABLE Stock (
    IdStock INT PRIMARY KEY IDENTITY(1,1),
    QuantiteStock INT,
	
);

CREATE TABLE Vente (
    IdVente INT PRIMARY KEY IDENTITY(1,1),
    QuantiteVendue INT not null,
    PrixTotal FLOAT not null,
);

CREATE TABLE Poste (
    IdPoste INT PRIMARY KEY IDENTITY(1,1),
	NbreEnfant INT not null,
    NbresJours INT not null,
	lieu_habitation VARCHAR(55) not null,
	NiveauEnfant varchar(90) NOT NULL,
	DateLimte Date NOT NULL,
	DatePublication varchar(35) NOT NULL
	Classe varchar(200),
	Matiere varchar(200)
);

ALTER TABLE Poste
ADD IdParent int FOREIGN KEY(IdParent) REFERENCES Parent(IdParent);

select * from HistoriquePoste
SELECT  * FROM HistoriquePoste H join Poste P on H.IdPoste=P.IdPoste
CREATE TABLE HistoriquePoste(
	IdHistoriquePoste int IDENTITY(1,1) NOT NULL,
	IdPoste int NULL,
	FOREIGN KEY(IdPoste) REFERENCES Poste(IdPoste)
 )

--debut nouveau script

UPDATE users
SET path_PhotoProfil = 'default_profil.png'
WHERE path_PhotoProfil is null;
 

	UPDATE Poste
SET Classe = '3ième, 4ième', Matiere= 'Maths, P-Chemie, Français'
WHERE Classe is null and Matiere is null and NiveauEnfant= 'Collège';

	UPDATE Poste
SET Classe = 'Primaire, 3ième, 4ième, 1ièmeA', Matiere= 'Toutes les Matière du Primaire , Maths, P-Chemie, Français'
WHERE Classe is null and Matiere is null and NiveauEnfant= 'Collège, Primaire, Lycée';

	UPDATE Poste
SET Classe = 'TleC, TleD, 1ièmeA', Matiere= 'Maths, P-Chemie, SVT, Français'
WHERE Classe is null and Matiere is null and NiveauEnfant= 'Lycée';

UPDATE Poste
SET Classe = '3ième, 4ième, TleD, 1ièmeA', Matiere= 'Maths, P-Chemie, SVT, Français'
WHERE Classe is null and Matiere is null and NiveauEnfant= 'Collège, Lycée';

UPDATE Poste
SET Classe = 'Primaire', Matiere= 'Toutes les Matière '
WHERE Classe is null and Matiere is null and NiveauEnfant= 'Primaire';


CREATE TABLE Candidature(
	IdCandidature int PRIMARY KEY IDENTITY(1,1) NOT NULL,
	DateCandidature VARCHAR(55) NOT NULL, 
	IdRepetiteur int,
	FOREIGN KEY(IdRepetiteur) REFERENCES Repetiteur(IdRepetiteur),
	IdHistoriquePoste int,
	FOREIGN KEY(IdHistoriquePoste) REFERENCES HistoriquePoste(IdHistoriquePoste)

);
--Fin nouveau script

CREATE TABLE ContratPar_Rep (
	IdContrat int PRIMARY KEY IDENTITY(1,1) NOT NULL,
	StatutContrat bit NULL,
	DateDebutContrat date NULL,
	
);

CREATE TABLE ContratTemporaire(
	IdContratTemporaire int PRIMARY KEY IDENTITY(1,1) NOT NULL,
	StatutContratTemporaire bit NOT NULL,
	tempsContratTemporaire VARCHAR(55) NOT NULL, 
	IdParent int,
	FOREIGN KEY(IdParent) REFERENCES Parent(IdParent),
	IdRepetiteur int,
	FOREIGN KEY(IdRepetiteur) REFERENCES Repetiteur(IdRepetiteur)

);


ALTER TABLE Candidature
DROP CONSTRAINT FK__Candidatu__IdPos__17F790F9;



DBCC CHECKIDENT('Candidature', RESEED, 0);
select * from Candidature



ALTER TABLE ContratPar_Rep 
ADD IdParent int,
FOREIGN KEY(IdParent) REFERENCES Parent(IdParent),
	IdRepetiteur int,
FOREIGN KEY(IdRepetiteur) REFERENCES Repetiteur(IdRepetiteur);


CREATE TABLE NiveauEtudeEleve(
	IdNiveauEtudeint int PRIMARY KEY IDENTITY(1,1) NOT NULL,
	NomNiveauEtude varchar(55) NOT NULL,
	);


CREATE TABLE NoteRepetiteur (
	IdNote int primary key IDENTITY(1,1) NOT NULL,
	NoteRepetiteur int NOT NULL,
) 

ALTER TABLE NoteRepetiteur 
ADD IdRepetiteur int,
FOREIGN KEY(IdRepetiteur) REFERENCES Repetiteur(IdRepetiteur),
	IdParent int,
FOREIGN KEY(IdParent) REFERENCES Parent(IdParent);

insert into NiveauEtudeEleve (NomNiveauEtude) values ('Primaire'),
												('Collège'),
												('Lycée')

DBCC CHECKIDENT('ContratTemporaire', RESEED, 0);
select * from ContratTemporaire















SELECT
    name
FROM
    sys.foreign_keys
WHERE
    parent_object_id = OBJECT_ID('Candidature') AND 
    referenced_object_id = OBJECT_ID('Poste');