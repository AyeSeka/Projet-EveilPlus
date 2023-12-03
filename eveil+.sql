CREATE DATABASE eveil+;
USE eveil+;

CREATE TABLE Repetiteur (
    id_repetiteur INT PRIMARY KEY IDENTITY(1,1),
    nom_repetiteur VARCHAR(255),
    prenom_repetiteur VARCHAR(255),
    age_repetiteur INT,
    adresse_repetiteur VARCHAR(255),
    email_repetiteur VARCHAR(255),
    annee_experience INT,
    niveau_repetiteur VARCHAR(255),
    disponibilite_repetiteur VARCHAR(255),
    path_photo_repetiteur VARCHAR(255),
    path_piece_repetiteur VARCHAR(255),
    path_background_repetiteur VARCHAR(255)
);

CREATE TABLE Competence (
    id_competence INT PRIMARY KEY IDENTITY(1,1),
    nom_competence VARCHAR(255)
);

CREATE TABLE SpecialiteCompetence (
	id_specialite_matiere INT PRIMARY KEY IDENTITY(1,1),
    id_repetiteur INT,
    id_competence INT,
    FOREIGN KEY (id_repetiteur) REFERENCES Repetiteur(id_repetiteur),
    FOREIGN KEY (id_competence) REFERENCES Competence(id_competence),

);

CREATE TABLE Parent (
    id_parent INT PRIMARY KEY IDENTITY(1,1),
    nom_parent VARCHAR(255),
    prenom_parent VARCHAR(255),
    nombre_enfant INT,
    adresse_parent VARCHAR(255),
    email_parent VARCHAR(255) UNIQUE,
    telephone_parent VARCHAR(255),
    path_photo_parent VARCHAR(255),
    path_piece_parent VARCHAR(255),
    path_background_parent VARCHAR(255)
);

CREATE TABLE Personnel_Eveil (
    id_eveil INT PRIMARY KEY IDENTITY(1,1),
    nom_eveil VARCHAR(255),
    prenom_eveil VARCHAR(255),
    email_eveil VARCHAR(255) UNIQUE,
    telephone_eveil VARCHAR(255),
    adresse_eveil VARCHAR(255),
    fonction_eveil VARCHAR(255),
    path_photo_eveil VARCHAR(255),
    path_piece_eveil VARCHAR(255),
    path_background_eveil VARCHAR(255)
);

CREATE TABLE Librairie (
    id_librairie INT PRIMARY KEY IDENTITY(1,1),
    nom_librairie VARCHAR(255),
    adresse_librairie VARCHAR(255),
    email_librairie VARCHAR(255) UNIQUE,
    telephone_librairie VARCHAR(255),
    path_photo_librairie VARCHAR(255),
    path_piece_librairie VARCHAR(255),
    path_background_librairie VARCHAR(255)
);

CREATE TABLE Fourniture (
    id_fourniture INT PRIMARY KEY IDENTITY(1,1),
    nom_fourniture VARCHAR(255),
    description_fourniture VARCHAR(255),
    prix_fourniture FLOAT,
    path_photo_fourniture VARCHAR(255)
);

CREATE TABLE Paiement_Librairie (
    id_paiement_librairie INT PRIMARY KEY IDENTITY(1,1),
    date_paiement_librairie DATETIME,
    montant FLOAT,
    parent_id INT,
    librairie_id INT,
    FOREIGN KEY (parent_id) REFERENCES Parent(id_parent),
    FOREIGN KEY (librairie_id) REFERENCES Librairie(id_librairie)
);

CREATE TABLE Paiement_Repetiteur (
    id_paiement_repetiteur INT PRIMARY KEY IDENTITY(1,1),
    date_paiement_repetiteur DATETIME,
    montant_paiement_repetiteur FLOAT,
    parent_id INT,
    repetiteur_id INT,
    FOREIGN KEY (parent_id) REFERENCES Parent(id_parent),
    FOREIGN KEY (repetiteur_id) REFERENCES Repetiteur(id_repetiteur)
);

CREATE TABLE Categorie (
    id_categorie INT PRIMARY KEY IDENTITY(1,1),
    nom_categorie VARCHAR(255)
);

CREATE TABLE Stock (
    id_stock INT PRIMARY KEY IDENTITY(1,1),
    quantite_stock INT,
    date_stock DATETIME,
    librairie_id INT,
    fourniture_id INT,
    FOREIGN KEY (librairie_id) REFERENCES Librairie(id_librairie),
    FOREIGN KEY (fourniture_id) REFERENCES Fourniture(id_fourniture)
);

CREATE TABLE Vente (
    id_vente INT PRIMARY KEY IDENTITY(1,1),
    quantite_vendue INT,
    prix_total_vente FLOAT,
    date_vente DATETIME,
    librairie_id INT,
    fourniture_id INT,
    parent_id INT,
    FOREIGN KEY (librairie_id) REFERENCES Librairie(id_librairie),
    FOREIGN KEY (fourniture_id) REFERENCES Fourniture(id_fourniture),
    FOREIGN KEY (parent_id) REFERENCES Parent(id_parent)
);

CREATE TABLE Contrat (
    id_contrat INT PRIMARY KEY IDENTITY(1,1),
    matiere_contrat VARCHAR(255),
    prix_contrat FLOAT,
    date_debut DATETIME,
    date_fin DATETIME,
    id_parent INT,
    id_repetiteur INT,
    FOREIGN KEY (id_parent) REFERENCES Parent(id_parent),
    FOREIGN KEY (id_repetiteur) REFERENCES Repetiteur(id_repetiteur)
);