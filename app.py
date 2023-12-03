from flask import Flask, render_template, request,  redirect, url_for, flash,jsonify

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
@app.route("/recherche")
def recherche():
    return render_template("Parents/Recherches/recherche.html")

@app.route("/liste_recherche")
def liste_recherche():
    return render_template("Parents/Recherches/liste_recherche.html")

@app.route("/liste_repetiteurchoix")
def liste_repetiteurchoix():
    return render_template("Parents/Recherches/liste_repetiteurchoix.html")

@app.route("/profil_repetiteur")
def profil_repetiteur():
    return render_template("Parents/Recherches/profil_repetiteur.html")

#FIN RECHERCHE
# FIN PARENT

#DEBUT LIBRAIRIE
@app.route("/librairie_parent")
def librairie_parent():
    return render_template("librairie/librairie_parent.html")

@app.route("/librairie_repetiteur")
def librairie_repetiteur():
    return render_template("librairie/librairie_repetiteur.html")

#FIN LIBRAIRIE
#DEBUT REPETITEUR
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
#FIN REPETITEUR
if __name__ == "__main__":
    app.secret_key= 'admin123'
    app.run(debug=True)