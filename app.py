from flask import Flask, render_template, request,  redirect, url_for, flash,jsonify

app = Flask(__name__)

# DEBUT PARENT
@app.route("/")
def Accueil_parent():
    return render_template("Parents/accueil_parent.html", navbar="Partials/header_parent.html")

#DEBUT POSTE
@app.route("/poste")
def poste():
    return render_template("Parents/Postes/poste.html")
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
    return render_template("Repetiteur/recherche_repetiteur.html")
# DEFIN RECHERCHE_REPETITEUR
#FIN REPETITEUR
if __name__ == "__main__":
    app.secret_key= 'admin123'
    app.run(debug=True)