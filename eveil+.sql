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


SELECT  * FROM Repetiteur r join Competence c ON (r.IdCompetence = c.IdCompetence)

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
	DatePublication datetime NOT NULL
);

ALTER TABLE Poste
ADD IdParent int FOREIGN KEY(IdParent) REFERENCES Parent(IdParent);

CREATE TABLE ContratPar_Rep (
	IdContrat int PRIMARY KEY IDENTITY(1,1) NOT NULL,
	StatutContrat bit NULL,
	DateDebutContrat date NULL,
	
);
select * from Parent
SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser
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


ALTER TABLE Repetiteur   
ADD IdCompetence int,
FOREIGN KEY(IdCompetence) REFERENCES Competence(IdCompetence),
	IdUser int,
FOREIGN KEY(IdUser) REFERENCES users(IdUser);


insert into Competence (NomCompetence) values ('Sciences'),
												('Litterature'),
												('Sciences et Litterature')

ALTER TABLE Parent   
ADD IdUser int,
FOREIGN KEY(IdUser) REFERENCES users(IdUser)


ALTER TABLE Personnel_Eveil   
ADD IdUser int,
FOREIGN KEY(IdUser) REFERENCES users(IdUser)


--CREATE TABLE Paiement_Repetiteur (
--    id_paiement_repetiteur INT PRIMARY KEY IDENTITY(1,1),
--    date_paiement_repetiteur DATETIME,
--    montant_paiement_repetiteur FLOAT,
--);

ALTER TABLE Poste
ADD IdParent int FOREIGN KEY(IdParent) REFERENCES Parent(IdParent);

ALTER TABLE ContratPar_Rep 
ADD IdParent int,
FOREIGN KEY(IdParent) REFERENCES Parent(IdParent),
	IdRepetiteur int,
FOREIGN KEY(IdRepetiteur) REFERENCES Repetiteur(IdRepetiteur);


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