CREATE DATABASE eveil_plus;
USE eveil_plus;
CREATE TABLE Repetiteur (
    IdRepetiteur INT PRIMARY KEY IDENTITY(1,1),
    NomRepetiteur VARCHAR(30) NOT NULL,
    PrenomRepetiteur VARCHAR(55) NOT NULL,
    DateNaissance date NOT NULL,
    lieu_hab_rep VARCHAR(55)NOT NULL,
    AnneeExperience INT NOT NULL,
    NiveauRepetiteur VARCHAR(10) NOT NULL,
    EstActif BIT
);


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
	NiveauEnfant varchar(25) NOT NULL,
	DateLimte datetime,
	DatePublication datetime
);

ALTER TABLE Poste
ADD IdParent int FOREIGN KEY(IdParent) REFERENCES Parent(IdParent);

CREATE TABLE ContratPar_Rep (
	IdContrat int PRIMARY KEY IDENTITY(1,1) NOT NULL,
	StatutContrat bit NULL,
	DateDebutContrat date NULL,
	
);

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