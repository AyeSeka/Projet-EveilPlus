from flask import Flask, render_template, request,  redirect, url_for, flash,jsonify

app = Flask(__name__)

# PARENT
@app.route("/")
def Accueil_parent():
    return render_template("Partials/Base_parent.html")

# POSTE
@app.route("/poste")
def poste():
    return render_template("Parents/poste.html")
# POSTE
# RECHERCHE
@app.route("/recherche")
def recherche():
    return render_template("Parents/recherche.html")

@app.route("/liste_recherche")
def liste_recherche():
    return render_template("Parents/liste_recherche.html")

@app.route("/liste_repetiteurchoix")
def liste_repetiteurchoix():
    return render_template("Parents/liste_repetiteurchoix.html")

@app.route("/recherche_confirm")
def recherche_confirm():
    return render_template("Parents/recherche_confirm.html")

# RECHERCHE
# PARENT

# LIBRAIRIE
@app.route("/librairie")
def librairie():
    return render_template("librairie/librairie.html")

# LIBRAIRIE
if __name__ == "__main__":
    app.secret_key= 'admin123'
    app.run(debug=True)