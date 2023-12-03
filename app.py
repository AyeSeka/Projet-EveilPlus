import pyodbc
from flask import Flask, render_template, request,  redirect, url_for, flash, jsonify

app = Flask(__name__)


########### INDEX_PAGE ##############
@app.route("/")
def index():
    return render_template("Authentification/index.html")


########### CONNEXION ##############
@app.route("/connexion")
def connexion():
    return render_template("Authentification/connexion.html")

########### Inscription Parent ##############
@app.route("/inscriptionParent")
def inscriptionParent():
    return render_template("Authentification/inscriptionParent.html")

########### Inscription Repetiteur ##############
@app.route("/inscriptionRepetiteur")
def inscriptionRepetiteur():
    return render_template("Authentification/inscriptionRepetiteur.html")

# PARENT
# DEBUT PARENT
@app.route("/accueil_parent")
def Accueil_parent():
    return render_template("Parents/accueil_parent.html", navbar="Partials/header_parent.html")


@app.route("/poste")
def poste():
    return render_template("Parents/Postes/poste.html")


@app.route("/recapitulatif")
def recapitulatif():
    return render_template("Parents/Postes/recapitulatif.html")


@app.route("/historique_des_postes")
def historique_des_postes():
    return render_template("Parents/Postes/historique_des_postes.html")


@app.route("/poster_maintenant")
def poster_maintenant():
    return render_template("Parents/Postes/poster_maintenant.html")

#FIN POSTE
#DEBUT RECHERCHE
# @app.route("/recherche")
# def recherche():
#     return render_template("Parents/Recherches/recherche.html")
# FIN POSTE
# DEBUT RECHERCHE


# ! Back-End Recherche
# ? Fonction pour récupérer les options depuis la base de données
def get_options_from_db(column_name, table_name):
    # conn = pyodbc.connect(
    #     'Driver={SQL Server};'
    #     'Server=HP\\SQLEXPRESS;'
    #     'Database=eveil+;'
    #     'user=HP\\goliy;'

    # )
    conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};" 
                       "Server=DESKTOP-QQGKONI\SQLEXPRESS;" 
                       "Database=eveil_plus;" 
                       "Trusted_Connection=yes")
    
    cursor = conn.cursor()

    # if table_name == "SpecialiteCompetence":
    #     Si la table est specialite_matiere, on doit joindre avec la table Matiere pour obtenir le nom de la matière
    #     query = f"SELECT {table_name}.*, Competence.nom_competence " \
    #         f"FROM {table_name} " \
    #         f"JOIN Competence ON {
    #             table_name}.id_competence = Competence.id_competence"
    # else:
    #     Pour les autres tables, la requête reste la même sans jointure avec la table Matiere
    #     query = f"SELECT * FROM {table_name}"

    query = f"SELECT DISTINCT {column_name} FROM {table_name}"
    # options = cursor.execute(query)
    options = cursor.execute(query).fetchall()

    return options


# ? Recherche
@app.route("/recherche", methods=["GET"])
def recherche():
    #     conn = pyodbc.connect(
    #     'Driver={SQL Server};'
    #     'Server=HP\\SQLEXPRESS;'
    #     'Database=eveil+;'
    #     'user=HP\\goliy;'

    # )
    # cursor = conn.cursor()
    datalist_habitation = get_options_from_db(
        "adresse_repetiteur", "Repetiteur")
    datalist_niveau = get_options_from_db("niveau_repetiteur", "Repetiteur")
    datalist_experience = get_options_from_db("annee_experience", "Repetiteur")
    datalist_competence = get_options_from_db(
        "*", "Competence")
    # print(datalist_habitation)
    # print(datalist_niveau)
    # print(datalist_experience)
    print(datalist_competence)
    # for specialite in datalist_specialite:
    #     print(specialite[3])

    return render_template("Parents/Recherches/recherche.html", datalist_habitation=datalist_habitation, datalist_niveau=datalist_niveau, datalist_experience=datalist_experience, datalist_competence=datalist_competence)


# ? Liste Recherche
@app.route("/liste_recherche", methods=["GET", "POST"])
def liste_recherche():
    # conn = pyodbc.connect(
    #     'Driver={SQL Server};'
    #     'Server=HP\\SQLEXPRESS;'
    #     'Database=eveil+;'
    #     'user=HP\\goliy;'
    # )
    conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};" 
                       "Server=DESKTOP-QQGKONI\SQLEXPRESS;" 
                       "Database=eveil_plus;" 
                       "Trusted_Connection=yes")
    cursor = conn.cursor()
    # Récupérez les données du formulaire
    habitation = request.form.get("habitation")
    niveau = request.form.get("niveau")
    experience = request.form.get("experience")
    specialite = request.form.get("specialite")

    print(habitation)
    print(niveau)
    print(experience)
    print(specialite)

    query = """SELECT  (r.nom_repetiteur), r.annee_experience
            FROM Repetiteur r
            join SpecialiteCompetence s ON (r.id_repetiteur = s.id_repetiteur)
            join Competence c ON (c.id_competence = s.id_competence)
            WHERE 
            adresse_repetiteur = ? AND
            niveau_repetiteur = ? AND
            annee_experience = ? AND
            c.id_competence = ? 
            """
    # r.id_repetiteur = s.id_repetiteur AND
    # m.id_matiere = s.id_matiere
    cursor.execute(query, (habitation, niveau, experience, specialite))
    repetiteurs = cursor.fetchall()
    print(repetiteurs)

    return render_template("Parents/Recherches/liste_recherche.html", repetiteurs=repetiteurs)


@app.route("/liste_repetiteurchoix")
def liste_repetiteurchoix():
    return render_template("Parents/Recherches/liste_repetiteurchoix.html")

# Debut profil Parent
@app.route("/profil_parent")
def profil_parent():
    return render_template("Parents/Profil_Parent/profil_parent.html")

# fin profil Parent
@app.route("/profil_repetiteur")
def profil_repetiteur():
    return render_template("Parents/Recherches/profil_repetiteur.html")

#FIN RECHERCHE
# FIN RECHERCHE
# FIN PARENT

# DEBUT LIBRAIRIE


@app.route("/librairie_parent")
def librairie_parent():
    return render_template("librairie/librairie_parent.html")


@app.route("/librairie_repetiteur")
def librairie_repetiteur():
    return render_template("librairie/librairie_repetiteur.html")

# FIN LIBRAIRIE
# DEBUT REPETITEUR


@app.route("/accueil_repetiteur")
def accueil_repetiteur():
    return render_template("Repetiteur/accueil_repetiteur.html")

# DEBUT RECHERCHE_REPETITEUR


@app.route("/recherche_repetiteur")
def recherche_repetiteur():
    return render_template("Repetiteur/Recherche/recherche_repetiteur.html")


@app.route("/liste_rech_rep")
def liste_rech_rep():
    return render_template("Repetiteur/Recherche/liste_rech_rep.html")


@app.route("/candidature_rep")
def candidature_rep():
    return render_template("Repetiteur/Recherche/candidature_rep.html")


# DEFIN RECHERCHE_REPETITEUR
# FIN REPETITEUR
if __name__ == "__main__":
    app.secret_key = 'admin123'
    app.run(debug=True)
