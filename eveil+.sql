CREATE DATABASE eveil_plus;
USE eveil_plus;

CREATE TABLE Repetiteur (
    id_repetiteur INT PRIMARY KEY IDENTITY(1,1),
    nom_repetiteur VARCHAR(30) NOT NULL,
    prenom_repetiteur VARCHAR(55) NOT NULL,
    date_naissance date NOT NULL,
    lieu_habitation_rep VARCHAR(55)NOT NULL,
    email_repetiteur VARCHAR(30) UNIQUE,
	mot_de_passe VARCHAR(255) not null,
	confirm_mot_de_passe VARCHAR(255),
    annee_experience INT NOT NULL,
    niveau_repetiteur VARCHAR(10) NOT NULL,
    EstActif BIT ,
    path_photo_repetiteur VARCHAR(255),
);

CREATE TABLE Parent (
    id_parent INT PRIMARY KEY IDENTITY(1,1),
    nom_parent VARCHAR(20),
    prenom_parent VARCHAR(55),
	Email VARCHAR(30) not null unique,
	mot_de_passe VARCHAR(255) not null,
	confirm_mot_de_passe VARCHAR(255),
    lieu_habitation VARCHAR(55),
    telephone_parent1 VARCHAR(15),
	telephone_parent2 VARCHAR(15),
    path_photo_parent VARCHAR(255),
    

);
create table users(
	id_user INT PRIMARY KEY IDENTITY(1,1),
	Email VARCHAR(30) not null unique,
	mot_de_passe VARCHAR(255) not null,
	Roles VARCHAR(30) not null
)

CREATE TABLE Competence (
    id_competence INT PRIMARY KEY IDENTITY(1,1),
    nom_competence VARCHAR(55) NOT NULL
);

--CREATE TABLE SpecialiteCompetence (
--	id_specialite_matiere INT PRIMARY KEY IDENTITY(1,1),
--	id_repetiteur INT,
--	id_competence INT,
--	FOREIGN KEY (id_repetiteur) REFERENCES Repetiteur(id_repetiteur),
--	FOREIGN KEY (id_competence) REFERENCES Competence(id_competence),

--);


drop table Parent;


CREATE TABLE Personnel_Eveil (
    id_eveil INT PRIMARY KEY IDENTITY(1,1),
    nom_eveil VARCHAR(255),
    prenom_eveil VARCHAR(255),
    email_eveil VARCHAR(255) UNIQUE,
	mot_de_passe VARCHAR(255) not null,
	confirm_mot_de_passe VARCHAR(255),
    telephone VARCHAR(15),
    adresse VARCHAR(55),
    path_photo_eveil VARCHAR(255),
);

CREATE TABLE Produits (
    IdProduits INT PRIMARY KEY IDENTITY(1,1),
    NomProduits VARCHAR(55) not null,
    DesciptionProduits VARCHAR(55) not null,
    Prix FLOAT not null,
    path_photo_Produits VARCHAR(255),
    
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

CREATE TABLE Paiement_Repetiteur (
    id_paiement_repetiteur INT PRIMARY KEY IDENTITY(1,1),
    date_paiement_repetiteur DATETIME,
    montant_paiement_repetiteur FLOAT,
);



CREATE TABLE Stock (
    id_stock INT PRIMARY KEY IDENTITY(1,1),
    quantite_stock INT,
	
);

CREATE TABLE Vente (
    IdVente INT PRIMARY KEY IDENTITY(1,1),
    QuantiteVendue INT not null,
    PrixTotal FLOAT not null,
);

CREATE TABLE Poste (
    IdPoste INT PRIMARY KEY IDENTITY(1,1),
    NbresJours INT not null,
	NbreEnfant INT not null,
	lieu_habitation VARCHAR(55) not null,
	DateLimte datetime,
	DatePublication datetime
);