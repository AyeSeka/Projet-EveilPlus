from datetime import datetime
import os
import pyodbc
from flask import Flask, jsonify, render_template, request,  redirect, sessions, url_for, flash, session
from flask_bcrypt import Bcrypt
from functools import wraps
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
# from flask_sse import sse
import json
from flask_socketio import SocketIO, emit, join_room

# from flask_login import current_user, login_required
app = Flask(__name__)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)


# app.config["REDIS_URL"] = "redis://localhost:6379/0"
# app.register_blueprint(sse, url_prefix='/sse')


# conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
#                       "Server=Geek_Machine\SQLEXPRESS;"
#                        "Database=eveil_plus;"
#                        "Trusted_Connection=yes")

# conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
#                        "Server=MTN_ACADEMY\SQLEXPRESS;"
#                        "Database=eveil_plus;"
#                        "Trusted_Connection=yes")
conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                       "Server=DESKTOP-QQGKONI\SQLEXPRESS;"
                       "Database=eveil_plus;"
                       "Trusted_Connection=yes")
# conn = pyodbc.connect(
#     'Driver={SQL Server};'
#     'Server=HP\\SQLEXPRESS;'
#     'Database=eveil_plus;'
#     'user=HP\\goliy;'

# )

# connection_string = (
#     "Driver={ODBC Driver 17 for SQL Server};"
#     "Server=MTN_ACADEMY\SQLEXPRESS"
#     "Database=eveil_plus;"
#     "Trusted_Connection=yes"
# )
# # Fonction pour se connecter à la base de données SQL Server
# def connect_db():
#     return pyodbc.connect(connection_string)


######### Modification photo paramètre #############

# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# # Dossier par défaut
# DEFAULT_FOLDER = os.path.abspath('Static/img/user_img')


################## TEST_APP ####################
# ! Mes Paramètre Uploads Pictures
# ? Configuration pour le stockage des images du parent et du répétiteur
UPLOAD_FOLDER_PARENT = 'Static/uploads/images_profil_parent'
UPLOAD_FOLDER_REPETITEUR = 'Static/uploads/images_profil_repetiteur'
UPLOAD_FOLDER_PERSO = 'Static/uploads/images_profil_perso'


app.config['UPLOAD_FOLDER_PARENT'] = UPLOAD_FOLDER_PARENT
app.config['UPLOAD_FOLDER_REPETITEUR'] = UPLOAD_FOLDER_REPETITEUR
app.config['UPLOAD_FOLDER_PERSO'] = UPLOAD_FOLDER_PERSO


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['SESSION_TYPE'] = 'filesystem'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ? Modifier photo de profil du parent
# Route pour la modification du profil (y compris la mise à jour de la photo de profil)
@app.route('/upload_profile_photo_perso', methods=['POST'])
def upload_profile_photo_perso():
    
    if 'photo' not in request.files:
        return "Aucun fichier sélectionné"
        # return redirect(request.url)

    file = request.files['photo']

    if file.filename == '':
        return "Aucun fichier sélectionné"
        # return redirect(request.url)

    if file and allowed_file(file.filename):
        # Assurez-vous que le dossier d'uploads existe, sinon, créez-le
        if not os.path.exists(UPLOAD_FOLDER_PERSO):
            os.makedirs(UPLOAD_FOLDER_PERSO)

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER_PERSO'], filename)
        file.save(file_path)

        # Remplacez les barres obliques inverses par des barres obliques normales dans le chemin
        # file_path = file_path.replace('\\', '/')

        # Extraire la partie relative du chemin complet
        relative_path = os.path.relpath(
            file_path, app.config['UPLOAD_FOLDER_PERSO'])
        print(relative_path)

        # Récupérez l'ID de l'utilisateur connecté depuis la session
        user_id = session.get('IdUser')

        if user_id is not None:
            # Mettez à jour le chemin de la photo de profil dans la base de données
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET path_PhotoProfil = ? WHERE IdUser = ?", (relative_path, user_id))
            conn.commit()

            # Flash message pour indiquer la mise à jour réussie
            flash('Profil mis à jour avec succès!', 'success')
        else:
            # Gérer le cas où l'ID de l'utilisateur n'est pas présent dans la session
            return "Erreur id de l'utilisateur"

        # Redirigez vers la page du profil mis à jour
        return redirect(url_for('profil_persoEveil'))

    return redirect(request.url)

# ? Modifier photo de profil du parent
# Route pour la modification du profil (y compris la mise à jour de la photo de profil)
@app.route('/upload_profile_photo_parent', methods=['POST'])
def upload_profile_photo_parent():
    
    if 'photo' not in request.files:
        return "Aucun fichier sélectionné"
        # return redirect(request.url)

    file = request.files['photo']

    if file.filename == '':
        return "Aucun fichier sélectionné"
        # return redirect(request.url)

    if file and allowed_file(file.filename):
        # Assurez-vous que le dossier d'uploads existe, sinon, créez-le
        if not os.path.exists(UPLOAD_FOLDER_PARENT):
            os.makedirs(UPLOAD_FOLDER_PARENT)

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER_PARENT'], filename)
        file.save(file_path)

        # Remplacez les barres obliques inverses par des barres obliques normales dans le chemin
        # file_path = file_path.replace('\\', '/')

        # Extraire la partie relative du chemin complet
        relative_path = os.path.relpath(
            file_path, app.config['UPLOAD_FOLDER_PARENT'])
        print(relative_path)

        # Récupérez l'ID de l'utilisateur connecté depuis la session
        user_id = session.get('IdUser')

        if user_id is not None:
            # Mettez à jour le chemin de la photo de profil dans la base de données
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET path_PhotoProfil = ? WHERE IdUser = ?", (relative_path, user_id))
            conn.commit()

            # Flash message pour indiquer la mise à jour réussie
            flash('Profil mis à jour avec succès!', 'success')
        else:
            # Gérer le cas où l'ID de l'utilisateur n'est pas présent dans la session
            return "Erreur id de l'utilisateur"

        # Redirigez vers la page du profil mis à jour
        return redirect(url_for('profil_parent'))

    return redirect(request.url)


# ? Modifier photo de profil du répétiteur
# Route pour la modification du profil (y compris la mise à jour de la photo de profil)
@app.route('/upload_profile_photo_repetiteur', methods=['POST'])
def upload_profile_photo_repetiteur():
    if 'photo' not in request.files:
        return "Aucun fichier sélectionné"
        # return redirect(request.url)

    file = request.files['photo']

    if file.filename == '':
        return "Aucun fichier sélectionné"
        # return redirect(request.url)
        
    if file and allowed_file(file.filename):
        # Assurez-vous que le dossier d'uploads existe, sinon, créez-le
        if not os.path.exists(UPLOAD_FOLDER_REPETITEUR):
            os.makedirs(UPLOAD_FOLDER_REPETITEUR)

        filename = secure_filename(file.filename)
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER_REPETITEUR'], filename)
        file.save(file_path)

        # Remplacez les barres obliques inverses par des barres obliques normales dans le chemin
        # file_path = file_path.replace('\\', '/')

        # Extraire la partie relative du chemin complet
        relative_path = os.path.relpath(
            file_path, app.config['UPLOAD_FOLDER_REPETITEUR'])
        print(relative_path)

        # Récupérez l'ID de l'utilisateur connecté depuis la session
        user_id = session.get('IdUser')

        if user_id is not None:
            # Mettez à jour le chemin de la photo de profil dans la base de données
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET path_PhotoProfil = ? WHERE IdUser = ?", (relative_path, user_id))
            conn.commit()

            # Flash message pour indiquer la mise à jour réussie
            flash('Profil mis à jour avec succès!', 'success')
        else:
            # Gérer le cas où l'ID de l'utilisateur n'est pas présent dans la session
            return "Erreur id de l'utilisateur"

        # Redirigez vers la page du profil mis à jour
        return redirect(url_for('profil_repetiteur'))

    return redirect(request.url)


# ! Notifications Repetiteur
# ? Affichage Notifications
@app.route("/liste_notification_repetiteur")
def liste_notification_repetiteur():
    IdUser = session.get('IdUser')

    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()

    print(IdUser)
    print(type(IdUser))
    print(IdUser)
    return render_template("Repetiteur/liste_notification_repetiteur.html", id_user=IdUser, usersRepetiteur=usersRepetiteur)


# ? Rejoindre la salle pour avoir la notification
# Exemple générique pour stocker et récupérer les notifications
stored_notifications = {}


def get_stored_notifications(tutor_id):
    return stored_notifications.get(tutor_id, [])


def reset_stored_notifications(tutor_id):
    stored_notifications[tutor_id] = []
# @socketio.on('join')
# def handle_join(data):
#     room = data['room']
#     join_room(room)
#     print(f'Client a rejoint la salle : {room}')


@socketio.on('join')
def handle_join(data):
    tutor_id = data['tutor_id']
    room = str(tutor_id)
    join_room(room)
    print(f'Client a rejoint la salle : {room}')

    # Émettre les notifications enregistrées pour le répétiteur
    stored_notifications = get_stored_notifications(tutor_id)
    for notification in stored_notifications:
        emit('notification_repetiteur', notification, room=room)

    # Réinitialiser les notifications enregistrées après les avoir émises
    reset_stored_notifications(tutor_id)


# ? Envoie Notification
@socketio.on('choose_tutor')
def handle_choose_tutor(message):
    print('Répétiteur choisi:', message['message'])
    notification = message['message']
    tutor_id = message['tutor_id']

    # Rejoindre une salle spécifique basée sur l'ID du répétiteur
    room = tutor_id
    join_room(room)

    # Émettre le message uniquement à cette salle spécifique
    socketio.emit('notification_repetiteur', notification, room=room)

# @socketio.on('choose_tutor')
# def handle_choose_tutor(message):
#     print('Répétiteur choisi:', message['message'])
#     notification = message['message']
#     tutor_id = message['tutor_id']
#     socketio.emit('notification',
#                   notification, id_tutor=tutor_id)
# @socketio.on('choose_tutor')
# def handle_choose_tutor(message):
#     print('Répétiteur choisi:', message['message'])
#     # Assurez-vous que l'ID du tuteur est inclus dans le message
#     tutor_id = int(message['tutor_id'])
#     print(tutor_id)
#     print(type(tutor_id))
#     socketio.emit('notification', {
#                   'message': 'Un parent a choisi un répétiteur !', 'tutor_id': tutor_id}, room=tutor_id)


@socketio.on('test_event')
def handle_test_event():
    print('Événement de test reçu côté serveur')


@app.route("/")
def index():
    return render_template("Authentification/index.html")


@app.route("/rechercher_testApp", methods=["GET"])
def rechercher_testApp():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()
    datalist_habitation = get_options_from_db(
        "lieu_hab_rep", "Repetiteur")
    datalist_niveau = get_options_from_db("NiveauRepetiteur", "Repetiteur")
    datalist_experience = get_options_from_db("AnneeExperience", "Repetiteur")
    datalist_competence = get_options_from_db(
        "*", "Competence")
    return render_template("Test_app/rechercheTest/rechercher_testApp.html", datalist_habitation=datalist_habitation, datalist_niveau=datalist_niveau, datalist_experience=datalist_experience, datalist_competence=datalist_competence, usersParent=usersParent)


@app.route("/liste_recherche_testApp", methods=["GET", "POST"])
def liste_recherche_testApp():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()

    habitation = request.form.get("habitation")
    niveau = request.form.get("niveau")
    experience = request.form.get("experience")
    specialite = request.form.get("specialite")

    query = """SELECT  * FROM Repetiteur r join Competence c ON (r.IdCompetence = c.IdCompetence)
            WHERE
            lieu_hab_rep = ? AND
            NiveauRepetiteur = ? AND 
            AnneeExperience = ? AND
            r.IdCompetence = ?
            """
    cursor.execute(query, (habitation, niveau, experience, specialite))
    repetiteurs = cursor.fetchall()
    etat_repetiteur = None
    message = None

    # Vérifiez si tous les critères de recherche sont satisfaits
    if habitation and niveau and experience and specialite and len(repetiteurs) == 0:
        message = "Aucune correspondance trouvée."
        print("Message:", message)
    elif len(repetiteurs) > 0:
        etat_repetiteur = repetiteurs[0][7]
        print("Recherche:", habitation, niveau, experience, specialite)
        print("Repetiteurs:", repetiteurs)

    cursor.commit()

    print("Repetiteurs:", repetiteurs)
    print("Users Parent:", usersParent)
    print("État du répétiteur:", etat_repetiteur)
    print("Message:", message)

    return render_template("Test_app/rechercheTest/liste_recherche_testApp.html", repetiteurs=repetiteurs, usersParent=usersParent, etat_repetiteur=etat_repetiteur, message=message)


@app.route("/poste_testApp", methods=["GET", "POST"])
def poste_testApp():
    # if request.method == "POST":
    # Récupérer les données du formulaire
    # habitation = request.form.get("habitation")
    # niveau = request.form.get("niveau")
    # enfant = request.form.get("enfant")
    # seance = request.form.get("seance")
    # date_limite = request.form.get("date_limite")

    # Stocker les données dans la carte temporaire
    # Stocker les informations dans la session
    # session['data_recap'] = {
    #     'habitation': habitation,
    #     'niveau': niveau,
    #     'enfant': enfant,
    #     'seance': seance,
    #     'date_limite': date_limite
    # }
    # data_recap = {
    #     "habitation": habitation,
    #     "niveau": niveau,
    #     "enfant": enfant,
    #     "seance": seance,
    #     "date_limite": date_limite,
    # }

    # print(data_recap)

    # return redirect(url_for("recapitulatif"))

    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()

    cursor.execute("SELECT * from NiveauEtudeEleve")
    niveauEtudiant = cursor.fetchall()

    cursor.execute("SELECT lieu_hab_rep from Repetiteur")
    lieu_repetiteur = cursor.fetchall()

    # for lieu in lieu_repetiteur:
    #     print(lieu[0])
    # print(lieu_repetiteur)

    # print(niveauEtudiant)
    conn.commit()
    return render_template("Test_app/postTest/poste_testApp.html", usersParent=usersParent, niveauEtudiant=niveauEtudiant, lieu_repetiteur=lieu_repetiteur)


@app.route("/recap_testApp", methods=["GET", "POST"])
def recap_testApp():
    IdUser = session.get('IdUser')

    if request.method == "POST":
        # Récupérer les données du formulaire
        habitation = request.form.get("habitation")
        niveau = ', '.join(request.form.getlist("niveau[]"))
        enfant = request.form.get("enfant")
        seance = request.form.get("seance")
        date_limite = request.form.get("date_limite")

        # Convertir la chaîne de date en objet de date
        date_limite = datetime.strptime(date_limite, '%Y-%m-%d').date()

        # Comparer les dates
        if date_limite <= datetime.now().date():
            flash(f"Veuillez choisir une date limite valide", 'danger')
            return redirect(url_for('poste_testApp'))

        # Stocker les données dans la carte temporaire
        # Stocker les informations dans la session
        data_recap = {
            'habitation': habitation,
            'niveau': niveau,
            'enfant': enfant,
            'seance': seance,
            'date_limite': date_limite
        }
        session['data_recap'] = {
            "habitation": habitation,
            "niveau": niveau,
            "enfant": enfant,
            "seance": seance,
            "date_limite": date_limite,
        }

    # Récupérer les informations depuis la session

    # print(IdUser)
    # print(data_recap)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()
    return render_template("Test_app/postTest/recap_testApp.html", usersParent=usersParent, data_recap=data_recap)


########### INFO ##############
#  Mécanisme de protection pour obligier le user à se connecter
# ? Utiliser le décorateur @login_required


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Veuillez vous connecter pour accéder à cette page.', 'danger')
            return redirect(url_for('connexion'))
        return f(*args, **kwargs)
    return decorated_function


########### CONNEXION ##############
@app.route("/connexion", methods=['GET', 'POST'])
def connexion():
    return render_template("Authentification/connexion.html")


@app.route("/success_connexion", methods=['GET', 'POST'])
def success_connexion():

    Email = request.form["Email"]
    mot_de_passe = request.form["mot_de_passe"]
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE Email = '{Email}'")
    users = cursor.fetchone()

    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser")
    usersParent = cursor.fetchone()

    cursor.execute(
        "SELECT Pe.*, U.* FROM Personnel_Eveil Pe JOIN users U ON Pe.IdUser=U.IdUser")
    usersPersonnel = cursor.fetchone()
    cursor.execute(
        "SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence")
    usersRepetiteur = cursor.fetchone()

    cursor.commit()
    if users is not None:
        session['IdUser'] = users.IdUser

        # session['IdRepetiteur'] = usersRepetiteur.IdRepetiteur
        # print(session['IdUser'])
        # Vérification du mot de passe haché
        if bcrypt.check_password_hash(users[2], mot_de_passe) and users[4] == 'Parent':
            session['user_id'] = users[0]
            # Authentification réussie
            # flash(f"Succès! Bienvenue, nous somme heureux de vous revoit", 'success')
            return redirect(url_for('Accueil_parent'))
        elif users and bcrypt.check_password_hash(users[2], mot_de_passe) and users[4] == 'Repetiteur':

            # flash(f"Succès! Bienvenue, nous somme heureux de vous revoit", 'success')
            session['user_id'] = users[0]

            return redirect(url_for('accueil_repetiteur'))
        elif users and bcrypt.check_password_hash(users[2], mot_de_passe) and users[4] == 'Admin':

            # flash(f"Succès! Bienvenue, nous somme heureux de vous revoit", 'success')
            session['user_id'] = users[0]

            return redirect(url_for('dashboard_admin'))
        else:
            flash(
                'connexion échoué! Vous avez certainement entré un e-mail ou mot de passe incorrect', 'danger')
            return redirect(url_for('connexion'))

    else:
        # Utilisateur non trouvé
        flash('Utilisateur non trouvé! Vous avez certainement entré un e-mail ou mot de passe incorrect', 'danger')
        return redirect(url_for('connexion'))

    # return render_template("Authentification/connexion.html")

########### Inscription Parent ##############


@app.route("/inscriptionPerso", methods=['GET', 'POST'])
def inscriptionPerso():
    return render_template("Authentification/inscriptionPerso.html")

@app.route("/Succes_inscriptionPerso", methods=['GET', 'POST'])
def Succes_inscriptionPerso():
    if request.method == 'POST':
        Email = request.form["Email"]
        mot_de_passe = request.form["mot_de_passe"]
        # confirm_mot_de_passe = request.form["confirm_mot_de_passe"]
        Roles = request.form["Roles"]
        NomPersoEveil = request.form["NomPersoEveil"]
        PrenomPersoEveil = request.form["PrenomPersoEveil"]
        Adresse = request.form["Adresse"]
        Telephone = request.form["Telephone"]
        if not all([Email, mot_de_passe, Roles, NomPersoEveil, PrenomPersoEveil, Adresse, Telephone,]):
            flash('Veuillez remplir tous les champs du formulaire.', 'danger')
            return redirect(url_for('inscriptionPerso'))

        mot_de_passe_hache = bcrypt.generate_password_hash(mot_de_passe).decode('utf-8')
        cursor = conn.cursor()
        # Exécuter une requête pour vérifier l'existence de l'utilisateur
        cursor.execute(f"SELECT COUNT(*)  FROM users WHERE Email = '{Email}'")
        # Récupérer le résultat
        row_count = cursor.fetchone()[0]
        if row_count != 0:
            print()
            flash(f"L'utilisateur {Email} existe déjà.", 'danger')
            return redirect(url_for('inscriptionPerso'))
        else:

            cursor.execute(f"INSERT INTO users (Email, mot_de_passe, Roles, path_PhotoProfil) VALUES ('{Email}','{mot_de_passe_hache}','{Roles}', 'default_profil.png')")
            cursor.execute("SELECT SCOPE_IDENTITY()")
            listId = cursor.fetchone()
            cursor.execute(f"INSERT INTO Personnel_Eveil (NomPersoEveil, PrenomPersoEveil, Adresse, Telephone, IdUser) VALUES ('{NomPersoEveil}', '{PrenomPersoEveil}', '{Adresse}', '{Telephone}', '{listId[0]}')")
            # Commit des modifications
            conn.commit()
            flash('Inscription réussie! Connectez-vous maintenant.', 'success')
            return redirect(url_for('connexion'))
    return render_template("Authentification/inscriptionPerso.html")

@app.route("/inscriptionParent", methods=['GET', 'POST'])
def inscriptionParent():
    return render_template("Authentification/inscriptionParent.html")


@app.route("/Succes_inscription_parent", methods=['GET', 'POST'])
def Succes_inscription_parent():
    if request.method == 'POST':
        Email = request.form["Email"]
        mot_de_passe = request.form["mot_de_passe"]
        confirm_mot_de_passe = request.form["confirm_mot_de_passe"]
        Roles = request.form["Roles"]
        NomParent = request.form["NomParent"]
        PrenomParent = request.form["PrenomParent"]
        # LieuHabitation = request.form["LieuHabitation"]
        TelephoneParent1 = request.form["TelephoneParent1"]
        # TelephonePparent2 = request.form["TelephonePparent2"]
        if not all([Email, mot_de_passe, confirm_mot_de_passe, Roles, NomParent, PrenomParent, TelephoneParent1]):
            flash('Veuillez remplir tous les champs du formulaire.', 'danger')
            return redirect(url_for('inscriptionParent'))

        mot_de_passe_hache = bcrypt.generate_password_hash(mot_de_passe).decode('utf-8')
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*)  FROM users WHERE Email = '{Email}'")
        # Récupérer le résultat
        row_count = cursor.fetchone()[0]
        if row_count != 0:
            print()
            flash(f"L'utilisateur {Email} existe déjà.", 'danger')
            return redirect(url_for('inscriptionParent'))
        else:

            cursor.execute(f"INSERT INTO users (Email, mot_de_passe, Roles, path_PhotoProfil) VALUES ('{Email}','{mot_de_passe_hache}','{Roles}', 'default_profil.png')")
            cursor.execute("SELECT SCOPE_IDENTITY()")
            listId = cursor.fetchone()
            cursor.execute(f"INSERT INTO Parent (NomParent, PrenomParent,TelephoneParent1, IdUser) VALUES ('{NomParent}', '{PrenomParent}', '{TelephoneParent1}', '{listId[0]}')")
            # Commit des modifications
            conn.commit()
            flash('Inscription réussie! Connectez-vous maintenant.', 'success')
            return redirect(url_for('connexion'))
    return render_template("Authentification/inscriptionParent.html")


########### Inscription Repetiteur ##############
@app.route("/inscriptionRepetiteur", methods=['GET', 'POST'])
def inscriptionRepetiteur():
    cursor = conn.cursor()
    cursor.execute("SELECT * from Competence")
    Competence = cursor.fetchall()
    conn.commit()
    return render_template("Authentification/inscriptionRepetiteur.html", Competence=Competence)


@app.route("/Succes_inscription_repetiteur", methods=['GET', 'POST'])
def Succes_inscription_repetiteur():
    if request.method == 'POST':
        Email = request.form["Email"]
        mot_de_passe = request.form["mot_de_passe"]
        # confirm_mot_de_passe = request.form["confirm_mot_de_passe"]
        Roles = request.form["Roles"]
        NomRepetiteur = request.form["NomRepetiteur"]
        PrenomRepetiteur = request.form["PrenomRepetiteur"]
        # lieu_hab_rep = request.form["lieu_hab_rep"]
        # DateNaissance = request.form["DateNaissance"]
        # AnneeExperience = request.form["AnneeExperience"]
        # NiveauRepetiteur = request.form["NiveauRepetiteur"]
        EstActif = request.form["EstActif"]
        IdCompetence = request.form["IdCompetence"]
        # Vérifier si tous les champs sont remplis
        if not all([Email, mot_de_passe, Roles, NomRepetiteur, PrenomRepetiteur, EstActif, IdCompetence]):
            flash('Veuillez remplir tous les champs du formulaire.', 'danger')
            return redirect(url_for('inscriptionRepetiteur'))

        mot_de_passe_hache = bcrypt.generate_password_hash(
            mot_de_passe).decode('utf-8')
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*)  FROM users WHERE Email = '{Email}'")
        # Récupérer le résultat
        row_count = cursor.fetchone()[0]
        if row_count != 0:
            print()
            flash(f"L'utilisateur {Email} existe déjà.", 'danger')
            return redirect(url_for('inscriptionRepetiteur'))
        else:
            cursor.execute(f"INSERT INTO users (Email, mot_de_passe, Roles, path_PhotoProfil) VALUES ('{Email}','{mot_de_passe_hache}','{Roles}', 'default_profil.png')")
            cursor.execute("SELECT SCOPE_IDENTITY()")
            listId = cursor.fetchone()

            # Définir le nom de l'image par défaut (à personnaliser selon votre structure de dossiers)
            # default_image = 'default_profil.png'

            cursor.execute(f"INSERT INTO Repetiteur (NomRepetiteur, PrenomRepetiteur, EstActif, IdCompetence, IdUser) VALUES ('{NomRepetiteur}','{PrenomRepetiteur}','{EstActif}','{IdCompetence}','{listId[0]}')")
            # Commit des modifications
            conn.commit()
            flash('Inscription réussie! Connectez-vous maintenant.', 'success')
            return redirect(url_for('connexion'))
    return render_template("Authentification/inscriptionRepetiteur.html")

# PARENT
# DEBUT PARENT


# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'IdUser' not in session:
#             return redirect(url_for('connexion'))
#         return f(*args, **kwargs)
#     return decorated_function

@app.route("/accueil_parent")
@login_required
def Accueil_parent():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    query = """SELECT  * FROM Repetiteur r JOIN users u ON r.IdUser=u.IdUser JOIN Dispense d ON r.IdRepetiteur=d.IdRepetiteur join Competence c ON (r.IdCompetence = c.IdCompetence) order by AnneeExperience desc """
    # r.IdRepetiteur = c.IdRepetiteur AND
    # cursor.execute("SELECT * FROM Repetiteur R JOIN Dispense D ON R.IdRepetiteur=D.IdRepetiteur JOIN Competence C ON R.IdCompetence=C.IdCompetence")
    # info_rep = cursor.fetchall()

    cursor.execute(query)
    repetiteurs = cursor.fetchall()
    
    if repetiteurs:
        etat_repetiteur = repetiteurs[0][7]
    else:
        etat_repetiteur = None

    cursor.commit()

    if usersParent:
        # Assurez-vous de remplacer l'indice par celui approprié dans votre résultat SQL
        prenom_parent = usersParent[1]
        # Assurez-vous de remplacer l'indice par celui approprié dans votre résultat SQL
        nom_parent = usersParent[2]

        flash(f'Bienvenue, cher parent {prenom_parent} {nom_parent}!', 'success')
        # Ajoutez cette ligne pour indiquer que l'utilisateur vient de se connecter
        session['just_logged_in'] = True

        return render_template("Parents/accueil_parent.html", usersParent=usersParent, repetiteurs=repetiteurs, etat_repetiteur=etat_repetiteur)
    else:
        flash('Répétiteur non trouvé.', 'danger')
        return redirect(url_for('connexion'))


@app.route("/poste", methods=["GET", "POST"])
@login_required
def poste():
    # Vérifier si tous les champs sont remplis
    
    # if request.method == "POST":
    # Récupérer les données du formulaire
    # habitation = request.form.get("habitation")
    # niveau = request.form.get("niveau")
    # enfant = request.form.get("enfant")
    # seance = request.form.get("seance")
    # date_limite = request.form.get("date_limite")

    # Stocker les données dans la carte temporaire
    # Stocker les informations dans la session
    # session['data_recap'] = {
    #     'habitation': habitation,
    #     'niveau': niveau,
    #     'enfant': enfant,
    #     'seance': seance,
    #     'date_limite': date_limite
    # }
    # data_recap = {
    #     "habitation": habitation,
    #     "niveau": niveau,
    #     "enfant": enfant,
    #     "seance": seance,
    #     "date_limite": date_limite,
    # }

    # print(data_recap)

    # return redirect(url_for("recapitulatif"))

    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()

    cursor.execute("SELECT * from NiveauEtudeEleve")
    niveauEtudiant = cursor.fetchall()

    cursor.execute("SELECT lieu_hab_rep from Repetiteur")
    lieu_repetiteur = cursor.fetchall()
    
    cursor.execute("SELECT * FROM ClassePrimaire")
    ClassePrimaire = cursor.fetchall()

    cursor.execute("SELECT * FROM ClasseCollege")
    ClasseCollege = cursor.fetchall()

    cursor.execute("SELECT * FROM ClasseLycee")
    ClasseLycee = cursor.fetchall()

    cursor.execute("SELECT * FROM MatiereSciences")
    MatiereSciences = cursor.fetchall()

    cursor.execute("SELECT * FROM MatiereLitteraire")
    MatiereLitteraire = cursor.fetchall()

    # for lieu in lieu_repetiteur:
    #     print(lieu[0])
    # print(lieu_repetiteur)

    # print(niveauEtudiant)
    conn.commit()
    return render_template("Parents/Postes/poste.html", 
                           usersParent=usersParent,
                           niveauEtudiant=niveauEtudiant, 
                           lieu_repetiteur=lieu_repetiteur, 
                           ClassePrimaire=ClassePrimaire, 
                           ClasseCollege=ClasseCollege, 
                           ClasseLycee=ClasseLycee,
                           MatiereSciences=MatiereSciences,
                           MatiereLitteraire=MatiereLitteraire
                           )


@app.route("/recapitulatif", methods=["GET", "POST"])
@login_required
def recapitulatif():
    IdUser = session.get('IdUser')

    if request.method == "POST":
        # Récupérer les données du formulaire
        habitation = request.form.get("habitation")
        niveau = ', '.join(request.form.getlist("niveau[]"))
        Classe = ', '.join(request.form.getlist("Classe[]"))
        Matiere = ', '.join(request.form.getlist("Matiere[]"))
        enfant = request.form.get("enfant")
        seance = request.form.get("seance")
        date_limite = request.form.get("date_limite")
        if not all([habitation, niveau, Classe, Matiere, enfant, seance, date_limite]):
            flash('Veuillez remplir tous les champs du formulaire.', 'danger')
            return redirect(url_for('poste'))
        # Convertir la chaîne de date en objet de date
        # date_limite = datetime.strptime(date_limite, '%Y-%m-%d').date()

        # # Comparer les dates
        # if date_limite <= datetime.now().date():
        #     flash(f"Veuillez choisir une date limite valide", 'danger')
        #     return redirect(url_for('poste'))

        # Stocker les données dans la carte temporaire
        # Stocker les informations dans la session
        data_recap = {
            'habitation': habitation,
            'niveau': niveau,
            'Classe' : Classe,
            'Matiere' : Matiere,
            'enfant': enfant,
            'seance': seance,
            'date_limite': date_limite
        }
        session['data_recap'] = {
            "habitation": habitation,
            "niveau": niveau,
            'Classe' : Classe,
            'Matiere' : Matiere,
            "enfant": enfant,
            "seance": seance,
            "date_limite": date_limite,
        }

    # Récupérer les informations depuis la session

    # print(IdUser)
    # print(data_recap)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    

    cursor.commit()
    return render_template("Parents/Postes/recapitulatif.html", usersParent=usersParent, data_recap=data_recap)


@app.route("/Modif_recap", methods=["GET", "POST"])
@login_required
def Modif_recap():
    IdUser = session.get('IdUser')
    data_recap = session.get('data_recap', {})

    if request.method == "POST":
        # Récupérer les données modifiées du formulaire
        habitation = request.form.get("habitation")
        niveau = ', '.join(request.form.getlist("niveau[]"))
        Classe = ', '.join(request.form.getlist("Classe[]"))
        Matiere = ', '.join(request.form.getlist("Matiere[]"))
        enfant = request.form.get("enfant")
        seance = request.form.get("seance")
        date_limite = request.form.get("date_limite")

        # Mettre à jour les données dans la session
        data_recap.update({
            'habitation': habitation,
            'niveau': niveau,
            'Classe' : Classe,
            'Matiere' : Matiere,
            'enfant': enfant,
            'seance': seance,
            'date_limite': date_limite
        })

    # Récupérer les informations depuis la session
    cursor = conn.cursor()
    cursor.execute("SELECT * from NiveauEtudeEleve")
    niveauEtudiant = cursor.fetchall()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    
    cursor.execute("SELECT * FROM ClassePrimaire")
    ClassePrimaire = cursor.fetchall()

    cursor.execute("SELECT * FROM ClasseCollege")
    ClasseCollege = cursor.fetchall()

    cursor.execute("SELECT * FROM ClasseLycee")
    ClasseLycee = cursor.fetchall()

    cursor.execute("SELECT * FROM MatiereSciences")
    MatiereSciences = cursor.fetchall()

    cursor.execute("SELECT * FROM MatiereLitteraire")
    MatiereLitteraire = cursor.fetchall()
    cursor.commit()

    return render_template("Parents/Postes/Modif_recap.html",
                           usersParent=usersParent,
                           data_recap=data_recap,
                           niveauEtudiant=niveauEtudiant, 
                           ClassePrimaire=ClassePrimaire, 
                           ClasseCollege=ClasseCollege, 
                           ClasseLycee=ClasseLycee,
                           MatiereSciences=MatiereSciences,
                           MatiereLitteraire=MatiereLitteraire)


# @app.route("/recapitulatif_validation", methods=["POST"])
# def recapitulatif_validation():
#     IdUser = session.get('IdUser')
#     data_recap = session.get('data_recap', {})
#     # print(data_recap)
#     # Obtenez la date actuelle au format YYYY-MM-DD HH:MM:SS
#     date_publication = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # print(date_publication)

#     cursor = conn.cursor()
#     cursor.execute("SELECT P.IdParent FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
#     usersParent = cursor.fetchone()
#     cursor.execute(f"INSERT INTO Poste (NbreEnfant, NbresJours, lieu_habitation, NiveauEnfant, DateLimte, DatePublication, IdParent) VALUES ('{data_recap['enfant']}','{data_recap['seance']}','{data_recap['habitation']}','{data_recap['niveau']}','{data_recap['date_limite']}','{date_publication}','{usersParent[0]}')")

#     conn.commit()
#     return redirect(url_for("historique_des_postes"))

@app.route("/recapitulatif_validation", methods=["POST"])
def recapitulatif_validation():
    IdUser = session.get('IdUser')
    data_recap = session.get('data_recap', {})
    # print(data_recap)
    # Obtenez la date actuelle au format YYYY-MM-DD HH:MM:SS

    date_publication = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # print(date_publication)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.IdParent FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.execute(f"INSERT INTO Poste (NbreEnfant, NbresJours, lieu_habitation, NiveauEnfant, DateLimte, DatePublication, IdParent, Classe, Matiere) VALUES ('{data_recap['enfant']}','{data_recap['seance']}','{data_recap['habitation']}','{data_recap['niveau']}','{data_recap['date_limite']}','{date_publication}','{usersParent[0]}','{data_recap['Classe']}','{data_recap['Matiere']}')")

    cursor.execute("SELECT SCOPE_IDENTITY()")
    IdPoste = cursor.fetchone()
    cursor.execute(
        f"INSERT INTO HistoriquePoste (IdPoste) VALUES ('{IdPoste[0]}')")

    conn.commit()
    flash("Poste enrégistré avec succès ! Consultez l'historique de vos dans ""Mes Postes""", 'success')
    return redirect(url_for("poste"))


@app.route("/poste_sucess")
@login_required
def poste_sucess():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()
    # cursor.execute(
    #     "SELECT * FROM Poste PO JOIN Parent PA ON PO.IdParent=PA.IdParent join HistoriquePoste Hi ON Hi.IdPoste = PO.IdPoste  WHERE PA.IdParent = ?", usersParent[0])
    # poste_data = cursor.fetchall()

    # SELECT * FROM Poste PO
    # 		JOIN Parent PA ON PO.IdParent=PA.IdParent
    # 		join HistoriquePoste Hi ON Hi.IdPoste = PO.IdPoste
    # 		WHERE PA.IdParent =  usersParent[0]
    # print(poste_data[0])
    # print(poste_data[0][5])
    # print(date_seule)

    return render_template("Parents/Postes/poste_sucess.html", usersParent=usersParent)


@app.route("/liste_cadidature")
@login_required
def liste_cadidature():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()
    cursor.execute(
        "SELECT * FROM Candidature C JOIN HistoriquePoste H on C.IdHistoriquePoste = H.IdHistoriquePoste JOIN Poste P ON H.IdPoste=P.IdPoste JOIN Repetiteur R ON C.IdRepetiteur=R.IdRepetiteur join Competence Cpt ON (R.IdCompetence = Cpt.IdCompetence) JOIN users U ON R.IdUser=U.IdUser WHERE P.IdParent= ?", usersParent[0])
    ListeCandidature = cursor.fetchall()
    # cursor.execute(
    #     "SELECT * FROM Candidature C JOIN Poste P ON C.IdPoste=P.IdPoste ")
    # ListeCandidature = cursor.fetchall()
    
    return render_template("Parents/Postes/liste_cadidature.html", usersParent=usersParent, ListeCandidature=ListeCandidature)

# @app.route("/historique_des_postes")
# @login_required
# def historique_des_postes():
#     IdUser = session.get('IdUser')
#     cursor = conn.cursor()
#     cursor.execute(
#         "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
#     usersParent = cursor.fetchone()
#     cursor.commit()
#     cursor.execute(
#         "SELECT * FROM Poste PO JOIN Parent PA ON PO.IdParent=PA.IdParent WHERE PA.IdParent = ?", usersParent[0])
#     poste_data = cursor.fetchall()
#     # print(poste_data[0])
#     # print(poste_data[0][5])
#     # print(date_seule)

#     return render_template("Parents/Postes/historique_des_postes.html", usersParent=usersParent, poste_data=poste_data)


@app.route("/Mes_postes")
@login_required
def Mes_postes():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM Poste PO JOIN Parent PA ON PO.IdParent=PA.IdParent join HistoriquePoste Hi ON Hi.IdPoste = PO.IdPoste  WHERE PA.IdParent = ?", usersParent[0])
    poste_data = cursor.fetchall()

    cursor.commit()
    return render_template("Parents/Postes/Mes_postes.html", usersParent=usersParent, poste_data=poste_data)


# @app.route("/poster_maintenant")
# @login_required
# def poster_maintenant():
#     IdUser = session.get('IdUser')
#     cursor = conn.cursor()
#     cursor.execute(
#         "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
#     usersParent = cursor.fetchone()
#     cursor.commit()
#     return render_template("Parents/Postes/poster_maintenant.html", usersParent=usersParent)


@app.route("/Supprimer_poste/<int:IdHistPoste>", methods=['GET', 'POST'])
@login_required
def Supprimer_poste(IdHistPoste):
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()

    cursor.execute(
        "DELETE FROM HistoriquePoste WHERE IdHistoriquePoste = ?", IdHistPoste)

    cursor.commit()

    return redirect(url_for("Mes_postes"))
    # return render_template("Parents/Postes/Mes_postes.html", usersParent=usersParent)

# FIN POSTE
# DEBUT RECHERCHE
# @app.route("/recherche")
# def recherche():
#     return render_template("Parents/Recherches/recherche.html")
# FIN POSTE
# DEBUT RECHERCHE


#  Back-End Recherche
# ? Fonction pour récupérer les options depuis la base de données

def get_options_from_db(column_name, table_name):

    cursor = conn.cursor()

    if table_name == "Competence":
        # Si la table est specialite_matiere, on doit joindre avec la table Matiere pour obtenir le nom de la matière
        query = f"SELECT {table_name}.*, Competence.NomCompetence " \
            f"FROM {table_name} " \
            f"JOIN Competence ON {table_name}.IdCompetence = Competence.IdCompetence"
    else:
        # Pour les autres tables, la requête reste la même sans jointure avec la table Matiere
        query = f"SELECT * FROM {table_name}"

    query = f"SELECT DISTINCT {column_name} FROM {table_name}"
    # options = cursor.execute(query)
    options = cursor.execute(query).fetchall()

    return options


# ? Recherche
@app.route("/recherche", methods=["GET"])
@login_required
def recherche():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()
    datalist_habitation = get_options_from_db(
        "lieu_hab_rep", "Repetiteur")
    datalist_niveau = get_options_from_db("NiveauRepetiteur", "Repetiteur")
    datalist_experience = get_options_from_db("AnneeExperience", "Repetiteur")
    datalist_competence = get_options_from_db(
        "*", "Competence")

    # return render_template("Parents/Recherches/recherche.html", usersParent=usersParent)
    return render_template("Parents/Recherches/recherche.html", datalist_habitation=datalist_habitation, datalist_niveau=datalist_niveau, datalist_experience=datalist_experience, datalist_competence=datalist_competence, usersParent=usersParent)


# ? Liste Recherche
# @app.route("/liste_recherche", methods=["GET", "POST"])
# @login_required
# def liste_recherche():
#     IdUser = session.get('IdUser')
#     cursor = conn.cursor()
#     cursor.execute(
#         "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
#     usersParent = cursor.fetchone()

#     # cursor = conn.cursor()
#     # Récupérez les données du formulaire
#     habitation = request.form.get("habitation")
#     niveau = request.form.get("niveau")
#     experience = request.form.get("experience")
#     specialite = request.form.get("specialite")

#     # print(habitation)
#     # print(niveau)
#     # print(experience)
#     # print(specialite)

#     query = """SELECT  * FROM Repetiteur r join Competence c ON (r.IdCompetence = c.IdCompetence)


#             WHERE
#             lieu_hab_rep = ? OR
#             NiveauRepetiteur = ? OR
#             AnneeExperience = ? OR
#             c.NomCompetence = ?
#             """
#     # r.IdRepetiteur = c.IdRepetiteur AND

#     cursor.execute(query, (habitation, niveau, experience, specialite))
#     repetiteurs = cursor.fetchall()
#     etat_repetiteur = repetiteurs[0][7]
#     cursor.commit()

#     # return render_template("Parents/Recherches/liste_recherche.html", usersParent=usersParent)
#     return render_template("Parents/Recherches/liste_recherche.html", repetiteurs=repetiteurs, usersParent=usersParent,etat_repetiteur=etat_repetiteur)

# ? Liste Recherche
@app.route("/liste_recherche", methods=["GET", "POST"])
@login_required
def liste_recherche():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.execute("SELECT * FROM ClassePrimaire")
    ClassePrimaire = cursor.fetchall()

    cursor.execute("SELECT * FROM ClasseCollege")
    ClasseCollege = cursor.fetchall()

    cursor.execute("SELECT * FROM ClasseLycee")
    ClasseLycee = cursor.fetchall()

    cursor.execute("SELECT * FROM MatiereSciences")
    MatiereSciences = cursor.fetchall()

    cursor.execute("SELECT * FROM MatiereLitteraire")
    MatiereLitteraire = cursor.fetchall()
    # cursor = conn.cursor()
    # Récupérez les données du formulaire
    habitation = request.form.get("habitation")
    niveau = request.form.get("niveau")
    experience = request.form.get("experience")
    specialite = request.form.get("specialite")

    # cursor.execute("SELECT * FROM Repetiteur")
    # usersRepetiteur = cursor.fetchall()

    cursor.execute(
        "SELECT R.EstActif FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence")
    bouton_etat = cursor.fetchone()[0]
    # print(bouton_etat)
    # print(habitation)
    # print(niveau)
    # print(experience)
    # print(specialite)

    query = """SELECT  * FROM Repetiteur r JOIN users u ON r.IdUser=u.IdUser JOIN Dispense d ON r.IdRepetiteur=d.IdRepetiteur join Competence c ON (r.IdCompetence = c.IdCompetence)
            

            WHERE
            lieu_hab_rep = ? OR
            NiveauRepetiteur = ? OR 
            AnneeExperience = ? OR
            c.NomCompetence = ? AND
            r.EstActif = ?
            """
    # r.IdRepetiteur = c.IdRepetiteur AND
    # cursor.execute("SELECT * FROM Repetiteur R JOIN Dispense D ON R.IdRepetiteur=D.IdRepetiteur JOIN Competence C ON R.IdCompetence=C.IdCompetence")
    # info_rep = cursor.fetchall()

    cursor.execute(query, (habitation, niveau,
                   experience, specialite, bouton_etat))
    repetiteurs = cursor.fetchall()
    # print(repetiteurs)
    if repetiteurs:
        etat_repetiteur = repetiteurs[0][7]
    else:
        etat_repetiteur = None

    cursor.commit()

    # return render_template("Parents/Recherches/liste_recherche.html", usersParent=usersParent)
    return render_template("Parents/Recherches/liste_recherche.html",
                           specialite=specialite, 
                           repetiteurs=repetiteurs, 
                           usersParent=usersParent, 
                           MatiereSciences=MatiereSciences, 
                           MatiereLitteraire=MatiereLitteraire, 
                           ClassePrimaire=ClassePrimaire, 
                           ClasseCollege=ClasseCollege, 
                           ClasseLycee=ClasseLycee, 
                           etat_repetiteur=etat_repetiteur)



@app.route('/filtre', methods=['GET', 'POST'])
def filtre():
    cursor = conn.cursor()
    IdUser = session.get('IdUser')
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()

    if request.method == 'POST':
        classe_primaire = request.form.getlist('classe_primaire')
        classe_college = request.form.getlist('classe_college')
        classe_lycee = request.form.getlist('classe_lycee')
        matiere_sciences = request.form.getlist('matiere_sciences')
        matiere_litterature = request.form.getlist('matiere_litterature')

        print("Classes sélectionnées (primaire):", classe_primaire)
        print("Classes sélectionnées (collège):", classe_college)
        print("Classes sélectionnées (lycée):", classe_lycee)
        print("Matieres Sciences sélectionnées:", matiere_sciences)
        print("Matieres Littérature sélectionnées:", matiere_litterature)

        # Nettoyer les valeurs en enlevant les guillemets
        cleaned_classes_primaire = [classe.strip("'") for classe in classe_primaire]
        cleaned_classes_college = [classe.strip("'") for classe in classe_college]
        cleaned_classes_lycee = [classe.strip("'") for classe in classe_lycee]
        cleaned_matieres_sciences = [matiere.strip("'") for matiere in matiere_sciences]
        cleaned_matieres_litterature = [matiere.strip("'") for matiere in matiere_litterature]

        # Initialiser un ensemble pour stocker les IdRepetiteur correspondants (un ensemble ne permet pas de doublons)
        id_repetiteurs_set = set()

        for classe in cleaned_classes_primaire:
            # Requête pour récupérer les IdRepetiteur correspondants à chaque classe du primaire
            query_get_id_repetiteur = "SELECT IdRepetiteur FROM Dispense WHERE Classe LIKE ?"
            cursor.execute(query_get_id_repetiteur, '%' + classe + '%')

            # Ajouter les IdRepetiteur à l'ensemble
            id_repetiteurs_set.update([row[0] for row in cursor.fetchall()])

        for classe in cleaned_classes_college:
            # Requête pour récupérer les IdRepetiteur correspondants à chaque classe du collège
            query_get_id_repetiteur_college = "SELECT IdRepetiteur FROM Dispense WHERE Classe LIKE ?"
            cursor.execute(query_get_id_repetiteur_college, '%' + classe + '%')

            # Ajouter les IdRepetiteur à l'ensemble
            id_repetiteurs_set.update([row[0] for row in cursor.fetchall()])

        for classe in cleaned_classes_lycee:
            # Requête pour récupérer les IdRepetiteur correspondants à chaque classe du lycée
            query_get_id_repetiteur_lycee = "SELECT IdRepetiteur FROM Dispense WHERE Classe LIKE ?"
            cursor.execute(query_get_id_repetiteur_lycee, '%' + classe + '%')

            # Ajouter les IdRepetiteur à l'ensemble
            id_repetiteurs_set.update([row[0] for row in cursor.fetchall()])

        for matiere in cleaned_matieres_sciences:
            # Requête pour récupérer les IdRepetiteur correspondants à la matière Sciences
            query_get_id_repetiteur_sciences = "SELECT IdRepetiteur FROM Dispense WHERE Matiere LIKE ?"
            cursor.execute(query_get_id_repetiteur_sciences, '%' + matiere + '%')

            # Ajouter les IdRepetiteur à l'ensemble
            id_repetiteurs_set.update([row[0] for row in cursor.fetchall()])

        for matiere in cleaned_matieres_litterature:
            # Requête pour récupérer les IdRepetiteur correspondants à la matière Littérature
            query_get_id_repetiteur_litterature = "SELECT IdRepetiteur FROM Dispense WHERE Matiere LIKE ?"
            cursor.execute(query_get_id_repetiteur_litterature, '%' + matiere + '%')

            # Ajouter les IdRepetiteur à l'ensemble
            id_repetiteurs_set.update([row[0] for row in cursor.fetchall()])

        # Convertir l'ensemble en liste
        id_repetiteurs = list(id_repetiteurs_set)

        # Liste pour stocker les informations des répétiteurs
        repetiteurs_info = []

        # Parcourir la liste des IdRepetiteur
        for id_repetiteur in id_repetiteurs:
            # Requête pour récupérer les informations du répétiteur
            query_get_repetiteur_info = "SELECT * FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Dispense D ON R.IdRepetiteur=D.IdRepetiteur join Competence C ON (R.IdCompetence = C.IdCompetence) WHERE D.IdRepetiteur = ?"
            cursor.execute(query_get_repetiteur_info, id_repetiteur)
            
            # Récupérer les informations du répétiteur
            repetiteur = cursor.fetchone()

            # Ajouter les informations du répétiteur à la liste
            repetiteurs_info.append(repetiteur)
            print(repetiteur)
        if repetiteurs_info:
            etat_repetiteur = repetiteurs_info[0][7]
        else:
            etat_repetiteur = None
        # Vérifier si des répétiteurs ont été trouvés
        if repetiteurs_info:
            # Utiliser la fonction flash pour afficher le message
            flash(f"Félicitations ! Vous avez trouvé {len(repetiteurs_info)} répétiteur(s).", 'success')
            return render_template("Parents/Recherches/liste_recherche.html", repetiteurs=repetiteurs_info, usersParent=usersParent, etat_repetiteur=etat_repetiteur)
        else:
            flash("Aucun répétiteur trouvé pour les classes et matières sélectionnées.", 'warning')
            return render_template("Parents/Recherches/liste_recherche.html", usersParent=usersParent)

    
    # Ajoutez une instruction return pour les requêtes de type GET
    return render_template("Parents/Recherches/liste_recherche.html", usersParent=usersParent)


@app.route("/liste_repetiteurchoix")
@login_required
def liste_repetiteurchoix():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()
    return render_template("Parents/Recherches/liste_repetiteurchoix.html", usersParent=usersParent)


@app.route('/choose_repetiteur', methods=['POST'])
@login_required
def choose_repetiteur():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    try:
        data = request.json
        IdRepetiteur = data.get('repetiteurId')
        IdParent = usersParent[0]

        # Check if the parent has already selected this répétiteur
        cursor.execute(
            "SELECT * FROM ContratTemporaire WHERE IdParent = ? AND IdRepetiteur = ?", (IdParent, IdRepetiteur))
        existing_contract = cursor.fetchone()

        if existing_contract:
            # flash('Vous avez déjà sélectionné ce répétiteur.', 'warning')
            return jsonify(result='AlreadySelected', IdRepetiteur=IdRepetiteur, contractExists=True)

        # Get the current time
        current_time = datetime.now()

        # Format the time as HH:MM:SS
        heure_actuelle = current_time.strftime("%H:%M:%S")

        # Print the répétiteur's ID in the terminal

        cursor = conn.cursor()
        query_insert = """
                        INSERT INTO ContratTemporaire 
                        (StatutContratTemporaire, tempsContratTemporaire, IdParent, IdRepetiteur)
                        VALUES (?, ?, ?, ?)
                        """
        cursor.execute(
            query_insert, (1, heure_actuelle, IdParent, IdRepetiteur))
        cursor.commit()
        # flash('Le répétiteur a été choisi avec succès.', 'success')
        return jsonify(result='Success', IdRepetiteur=IdRepetiteur, contractExists=False)

        # Perform any necessary operations with the chosen tutor (e.g., store in the database)
        # ...

        # return jsonify(result='Success', IdRepetiteur=IdRepetiteur)
    except Exception as e:
        return jsonify(result='Error', message=str(e))


@app.route('/Mes_choix_rer')
@login_required
def Mes_choix_rer():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()

    # Check if the parent has already selected this répétiteur
    cursor.execute(
        "SELECT * FROM ContratTemporaire Co JOIN Parent P ON Co.IdParent=P.IdParent JOIN Repetiteur R ON Co.IdRepetiteur=R.IdRepetiteur JOIN users U ON R.IdUser=U.IdUser WHERE Co.IdParent= ?",usersParent[0])
    listContratTemp = cursor.fetchall()
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')
    return render_template("Parents/Recherches/Mes_choix_rer.html", usersParent=usersParent, listContratTemp=listContratTemp, photo_path=photo_path)


@app.route("/Supprimer_choix/<int:IdContratTemporaire>", methods=['GET', 'POST'])
@login_required
def Supprimer_choix(IdContratTemporaire):
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()

    cursor.execute(
        "DELETE FROM ContratTemporaire WHERE IdContratTemporaire = ?", IdContratTemporaire)

    cursor.commit()
    flash('Choix retiré avec succès.', 'danger')
    return redirect(url_for("Mes_choix_rer"))

# Debut profil


@app.route("/profil_parent")
@login_required
def profil_parent():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersParent = cursor.fetchone()


    # Pas besoin de cursor.commit() ici car vous n'effectuez que des sélections

    return render_template("Profil/profil_parent.html", usersParent=usersParent)


@app.route("/ModifProfil_par")
@login_required
def ModifProfil_par():
    user_id = session.get('IdUser')
    cursor = conn.cursor()
    # Sélectionner les informations existantes de l'utilisateur
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (user_id,))
    user_data = cursor.fetchone()
    return render_template("Profil/ModifProfil_par.html", usersParent=user_data)


@app.route("/SucessModifProfil_par", methods=['POST'])
@login_required
def SucessModifProfil_par():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()
    if request.method == "POST":
        Email = request.form["Email"]
        # confirm_mot_de_passe = request.form["confirm_mot_de_passe"]
        Roles = request.form["Roles"]
        NomParent = request.form.get("NomParent", "")
        PrenomParent = request.form.get("PrenomParent", "")
        TelephoneParent1 = request.form.get("TelephoneParent1", "")
        LieuHabitation = request.form.get("LieuHabitation", "")
        TelephonePparent2 = request.form.get("TelephonePparent2", "")
        if not all([Email, Roles, NomParent, PrenomParent, LieuHabitation, TelephoneParent1, TelephonePparent2]):
            flash('Veuillez remplir tous les champs du formulaire.', 'danger')
            return redirect(url_for('ModifProfil_par'))
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET Email=?, Roles=? WHERE IdUser = ?", (Email, Roles, IdUser))
        # cursor.execute("SELECT SCOPE_IDENTITY()")
        # listId = cursor.fetchone()
        cursor.execute("UPDATE Parent SET NomParent=?, PrenomParent=?, LieuHabitation=?, TelephoneParent1=?, TelephonePparent2=? WHERE IdParent = ?",
                       (NomParent, PrenomParent, LieuHabitation, TelephoneParent1, TelephonePparent2, usersParent[0]))

        # Commit des modifications
        conn.commit()
        flash('Votre profil à été mis à jour', 'success')
        return redirect(url_for('profil_parent'))
    return render_template("Profil/ModifProfil_par.html", usersParent=usersParent)


# @app.route('/upload', methods=['POST'])
# def upload():
#     if 'file' not in request.files:
#         return "Aucun fichier sélectionné"

#     file = request.files['file']

#     if file.filename == '':
#         return "Aucun fichier sélectionné"

#     folder_name = request.form.get('folder', DEFAULT_FOLDER)
#     upload_folder = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)

#     if not os.path.exists(upload_folder):
#         os.makedirs(upload_folder)

#     filepath = os.path.join(upload_folder, secure_filename(file.filename))
#     file.save(filepath)

#     # Ajoutez ici la logique pour insérer le chemin vers l'image dans la base de données
#     # Remplacez cela par la logique pour obtenir l'ID de l'utilisateur
#     IdUser = session.get('IdUser')

#     # Obtenez le chemin relatif en supprimant la partie "../Static"
#     relative_filepath = os.path.relpath(filepath, app.config['UPLOAD_FOLDER']).replace(
#         "\\", "/").replace("../Static", "")

#     cursor = conn.cursor()
#     cursor.execute("UPDATE users SET path_PhotoProfil=? WHERE IdUser=?",
#                    (relative_filepath, IdUser))
#     cursor.commit()
#     flash('Modification réussie! Vous avez changé votre photo de profil.', 'success')

#     return redirect(url_for('profil_parent'))


@app.route("/profil_repetiteur")
@login_required
def profil_repetiteur():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    cursor.execute("SELECT R.*, NomCompetence, U.*, D.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence JOIN Dispense D on D.IdRepetiteur=R.IdRepetiteur WHERE U.IdUser = ?", IdUser)
    userRepetiteur = cursor.fetchone()
    cursor.commit()

    cursor = conn.cursor()
    cursor.execute("SELECT R.EstActif FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    bouton_etat = cursor.fetchone()[0]

    conn.commit()
    return render_template("Profil/profil_repetiteur.html",userRepetiteur=userRepetiteur, usersRepetiteur=usersRepetiteur, bouton_etat=bouton_etat)


@app.route("/ModifProfil_rep", methods=['GET', 'POST'])
def ModifProfil_rep():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    cursor.commit()

    cursor = conn.cursor()
    cursor.execute(
        "SELECT R.EstActif FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE R.IdRepetiteur = ?", usersRepetiteur[0])
    bouton_etat = cursor.fetchone()[0]
    conn.commit()
    cursor = conn.cursor()
    cursor.execute("SELECT * from Competence")
    Competence = cursor.fetchall()
    cursor.execute("SELECT * FROM ClassePrimaire")
    ClassePrimaire = cursor.fetchall()

    cursor.execute("SELECT * FROM ClasseCollege")
    ClasseCollege = cursor.fetchall()

    cursor.execute("SELECT * FROM ClasseLycee")
    ClasseLycee = cursor.fetchall()

    cursor.execute("SELECT * FROM MatiereSciences")
    MatiereSciences = cursor.fetchall()

    cursor.execute("SELECT * FROM MatiereLitteraire")
    MatiereLitteraire = cursor.fetchall()
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    return render_template("Profil/ModifProfil_rep.html", usersRepetiteur=usersRepetiteur, bouton_etat=bouton_etat, Competence=Competence, ClassePrimaire=ClassePrimaire, ClasseCollege=ClasseCollege, ClasseLycee=ClasseLycee, MatiereSciences=MatiereSciences, MatiereLitteraire=MatiereLitteraire, photo_path=photo_path)


@app.route("/SuccesModifProfil_rep", methods=['GET', 'POST'])
def SuccesModifProfil_rep():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    cursor.commit()
    if request.method == 'POST':
        Email = request.form["Email"]
        Roles = request.form["Roles"]
        NomRepetiteur = request.form["NomRepetiteur"]
        PrenomRepetiteur = request.form["PrenomRepetiteur"]
        lieu_hab_rep = request.form["lieu_hab_rep"]
        DateNaissance = request.form["DateNaissance"]
        AnneeExperience = request.form["AnneeExperience"]
        NiveauRepetiteur = request.form["NiveauRepetiteur"]
        EstActif = request.form["EstActif"]
        IdCompetence = request.form["IdCompetence"]
        Classe = ', '.join(request.form.getlist("Classe[]"))
        Matiere = ', '.join(request.form.getlist("Matiere[]"))
        # Vérifier si tous les champs sont remplis
        if not all([Email, Roles, NomRepetiteur, PrenomRepetiteur, lieu_hab_rep, DateNaissance, AnneeExperience, NiveauRepetiteur, EstActif, IdCompetence, Classe, Matiere]):
            flash('Veuillez remplir tous les champs du formulaire.', 'danger')
            return redirect(url_for('ModifProfil_rep'))

        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET Email=?, Roles=? WHERE IdUser = ?", (Email, Roles, IdUser))
        cursor.execute("UPDATE Repetiteur SET NomRepetiteur=?, PrenomRepetiteur=?, DateNaissance=?, lieu_hab_rep=?, AnneeExperience=?, NiveauRepetiteur=?, EstActif=?, IdCompetence=? WHERE IdRepetiteur = ?",
                       (NomRepetiteur, PrenomRepetiteur, DateNaissance, lieu_hab_rep, AnneeExperience, NiveauRepetiteur, EstActif, IdCompetence, usersRepetiteur[0]))
        cursor.execute(
            "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
        result = cursor.fetchone()

        if result and result[0]:
            photo_path = result[0]
        else:
            photo_path = url_for(
                'static', filename='/img/user_img/user_avatar.jpg')

        # cursor.execute("SELECT SCOPE_IDENTITY()")
        # listId = cursor.fetchone()
        cursor.execute(
            "SELECT * FROM Dispense D join Repetiteur R on D.IdRepetiteur=R.IdRepetiteur WHERE R.IdRepetiteur = ?", usersRepetiteur[0])
        Dispense = cursor.fetchone()
        if Dispense is None:
            cursor.execute(f"INSERT INTO Dispense (IdRepetiteur, Matiere, Classe) VALUES ('{usersRepetiteur[0]}','{Matiere}','{Classe}')")
        # Commit des modifications
            conn.commit()
        else:
            cursor.execute(
                "UPDATE Dispense SET Matiere=?, Classe=? WHERE IdDispense = ?", (Matiere, Classe, Dispense[0]))

        flash('Votre profil à été mis à jour', 'success')
        return redirect(url_for('profil_repetiteur'))
    return render_template("Profil/ModifProfil_rep.html", usersRepetiteur=usersRepetiteur, Dispense=Dispense, photo_path=photo_path)


# # bouton disponibilité


@app.route('/changer_etat', methods=['POST'])
@login_required
def changer_etat():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.EstActif FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    bouton_etat = cursor.fetchone()[0]
    nouveau_etat = not bouton_etat
    a = cursor.execute(
        'UPDATE Repetiteur SET EstActif = ? WHERE IdUser = ?', nouveau_etat, IdUser)
    conn.commit()
    return redirect(url_for('profil_repetiteur'))

# fin profil

# FIN RECHERCHE
# FIN RECHERCHE
# FIN PARENT
# DEBUT COMMANDE

# Panier


@app.route("/panier")
def panier_parent():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()
    return render_template("Panier/panier.html", usersParent=usersParent)

# FIN COMMANDE
# DEBUT LIBRAIRIE
#  MES REPETITEURS
# ? Mes Repetiteurs


@app.route("/mes_repetiteurs")
@login_required
def mes_repetiteurs():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    
    cursor.execute("SELECT * FROM ContratPar_Rep Co JOIN  Repetiteur R ON Co.IdRepetiteur= R.IdRepetiteur JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence JOIN Dispense D on D.IdRepetiteur=R.IdRepetiteur WHERE Co.IdParent = ?", usersParent[0])
    ContractPar_Rep = cursor.fetchall()

    cursor.commit()
    return render_template("Parents/mes_repetiteurs/mes_repetiteurs.html", usersParent=usersParent, ContractPar_Rep=ContractPar_Rep)


# ? Attribuer Note
@app.route("/attribuer_note")
@login_required
def attribuer_note():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    cursor.commit()
    return render_template("Parents/mes_repetiteurs/attribuer_note.html", usersParent=usersParent, photo_path=photo_path)


# ? Choix Operateur
@app.route("/choix_operateur")
@login_required
def choix_operateur():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')
    cursor.commit()
    return render_template("Parents/mes_repetiteurs/choix_operateur.html", usersParent=usersParent, photo_path=photo_path)

# ? Choix Operateur


@app.route("/form_paiement")
@login_required
def form_paiement():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()
    return render_template("Parents/mes_repetiteurs/form_paiement.html", usersParent=usersParent)


#  BACK-END LIBRAIRIE
@app.route("/librairie")
def librairie_parent():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
    usersParent = cursor.fetchone()
    cursor.commit()
    return render_template("librairie/librairie.html", usersParent=usersParent)


# FIN LIBRAIRIE
# DEBUT REPETITEUR


@app.route("/accueil_repetiteur")
@login_required
def accueil_repetiteur():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    
    query = """SELECT  * FROM HistoriquePoste H join Poste P on H.IdPoste=P.IdPoste order by DatePublication desc"""
    # r.IdRepetiteur = c.IdRepetiteur AND
    # cursor.execute("SELECT * FROM Repetiteur R JOIN Dispense D ON R.IdRepetiteur=D.IdRepetiteur JOIN Competence C ON R.IdCompetence=C.IdCompetence")
    # info_rep = cursor.fetchall()

    cursor.execute(query)
    poste = cursor.fetchall()
    if usersRepetiteur:
        # Assurez-vous de remplacer l'indice par celui approprié dans votre résultat SQL
        prenom_repetiteur = usersRepetiteur[1]
        # Assurez-vous de remplacer l'indice par celui approprié dans votre résultat SQL
        nom_repetiteur = usersRepetiteur[2]

        flash(f'Bienvenue, cher répétiteur {prenom_repetiteur} {nom_repetiteur}!', 'success')
        return render_template("Repetiteur/accueil_repetiteur.html", usersRepetiteur=usersRepetiteur, poste=poste)
    else:
        flash('Répétiteur non trouvé.', 'danger')
        return redirect(url_for('connexion'))
    # return render_template("Repetiteur/accueil_repetiteur.html")
# DEBUT RECHERCHE_REPETITEUR


@app.route("/recherche_repetiteur", methods=["GET"])
@login_required
def recherche_repetiteur():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    datalist_habitation = get_options_from_db(
        "lieu_habitation", "Poste")
    datalist_niveau = get_options_from_db("NiveauEnfant", "Poste")
    datalist_NbreEnfant = get_options_from_db("NbreEnfant", "Poste")
    datalist_NbresJours = get_options_from_db("NbresJours", "Poste")
    datalist_Classe = get_options_from_db("Classe", "Poste")
    datalist_Matiere = get_options_from_db("Matiere", "Poste")
    cursor.commit()
    
    cursor.execute("SELECT DISTINCT lieu_habitation from Poste")
    Listelieu_habitation = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT NiveauEnfant from Poste")
    ListeNiveauEnfant = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT NbreEnfant from Poste order by NbreEnfant")
    ListeNbreEnfant = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT NbresJours from Poste order by NbresJours")
    ListeNbresJours = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT Classe from Poste")
    ListeClasse = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT Matiere from Poste")
    ListeMatiere = cursor.fetchall()
    return render_template("Repetiteur/Recherche/recherche_repetiteur.html",
                           Listelieu_habitation=Listelieu_habitation,
                           ListeNiveauEnfant=ListeNiveauEnfant, 
                           ListeNbreEnfant=ListeNbreEnfant, ListeNbresJours=ListeNbresJours,
                           ListeClasse=ListeClasse, ListeMatiere=ListeMatiere,
                           usersRepetiteur=usersRepetiteur,
                           datalist_habitation=datalist_habitation,
                           datalist_niveau=datalist_niveau,
                           datalist_NbreEnfant=datalist_NbreEnfant,
                           datalist_NbresJours=datalist_NbresJours,
                           datalist_Classe=datalist_Classe,
                           datalist_Matiere=datalist_Matiere)


@app.route("/liste_rech_rep", methods=["GET", "POST"])
@login_required
def liste_rech_rep():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    cursor.commit()
    # cursor = conn.cursor()
    # Récupérez les données du formulaire
    if request.method == "POST":
        lieu_habitation = request.form.get("lieu_habitation")
        NiveauEnfant = request.form.get("NiveauEnfant")
        NbreEnfant = request.form.get("NbreEnfant")
        NbresJours = request.form.get("NbresJours")
        Classe = request.form.get("Classe")
        Matiere = request.form.get("Matiere")
        if not all([lieu_habitation, NiveauEnfant, NbreEnfant, NbresJours, Classe, Matiere]):
            flash('Veuillez remplir tous les champs du formulaire.', 'danger')
            return redirect(url_for('recherche_repetiteur'))
        # cursor.execute("SELECT * FROM Repetiteur")
        # usersRepetiteur = cursor.fetchall()

        query = """SELECT  * FROM HistoriquePoste H join Poste P on H.IdPoste=P.IdPoste WHERE lieu_habitation = ? AND (NiveauEnfant = ? or NbreEnfant = ? or NbresJours = ? or Classe = ? or Matiere = ?)  """
    # r.IdRepetiteur = c.IdRepetiteur AND
    # cursor.execute("SELECT * FROM Repetiteur R JOIN Dispense D ON R.IdRepetiteur=D.IdRepetiteur JOIN Competence C ON R.IdCompetence=C.IdCompetence")
    # info_rep = cursor.fetchall()

        cursor.execute(query, (lieu_habitation, NiveauEnfant,
                    NbreEnfant, NbresJours, Classe, Matiere))
        poste = cursor.fetchall()
    

    # return render_template("Parents/Recherches/liste_recherche.html", usersParent=usersParent)
    # return render_template("Parents/Recherches/liste_recherche.html", specialite=specialite, repetiteurs=repetiteurs, usersParent=usersParent, MatiereSciences=MatiereSciences, MatiereLitteraire=MatiereLitteraire, ClassePrimaire=ClassePrimaire, ClasseCollege=ClasseCollege, ClasseLycee=ClasseLycee, etat_repetiteur=etat_repetiteur)

    return render_template("Repetiteur/Recherche/liste_rech_rep.html", usersRepetiteur=usersRepetiteur,poste=poste)



@app.route('/candidature_rep', methods=['POST'])
@login_required
def candidature_rep():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    try:
        data = request.json
        IdHistoriquePoste = data.get('HistoriquePosteId')
        IdParent = data.get('ParentId')
        IdRepetiteur = usersRepetiteur[0]
        print(IdParent)
        print(IdHistoriquePoste)
        print(IdRepetiteur)
        # Check if the parent has already selected this répétiteur
        cursor.execute(
            "SELECT * FROM Candidature C JOIN HistoriquePoste H on C.IdHistoriquePoste = H.IdHistoriquePoste WHERE C.IdRepetiteur= ? AND H.IdHistoriquePoste = ? AND C.IdParent = ?", (IdRepetiteur,IdHistoriquePoste,IdParent ))
        existing_candidature = cursor.fetchone()

        if existing_candidature:
            # flash('Vous avez déjà sélectionné ce répétiteur.', 'warning')
            return jsonify(result='AlreadySelected', IdHistoriquePoste=IdHistoriquePoste, contractExists=True)

        # Obtenez la date actuelle au format YYYY-MM-DD HH:MM:SS

        date_publication = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        # Print the répétiteur's ID in the terminal

        cursor = conn.cursor()
        query_insert = """
                        INSERT INTO Candidature 
                        (DateCandidature,IdRepetiteur, IdHistoriquePoste, IdParent)
                        VALUES (?, ?, ?,?)
                        """
        cursor.execute(
            query_insert, (date_publication,IdRepetiteur, IdHistoriquePoste, IdParent ))
        cursor.commit()
        # flash('Le répétiteur a été choisi avec succès.', 'success')
        return jsonify(result='Success', IdHistoriquePoste=IdHistoriquePoste, contractExists=False)

        # Perform any necessary operations with the chosen tutor (e.g., store in the database)
        # ...

        # return jsonify(result='Success', IdRepetiteur=IdRepetiteur)
    except Exception as e:
        return jsonify(result='Error', message=str(e))

@app.route("/Mes_candidature")
@login_required
def Mes_candidature():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    
    cursor.execute(
        "SELECT * FROM Candidature C JOIN HistoriquePoste H on C.IdHistoriquePoste = H.IdHistoriquePoste JOIN Poste P ON H.IdPoste=P.IdPoste WHERE C.IdRepetiteur= ?",usersRepetiteur[0])
    listCandidature = cursor.fetchall()
    cursor.commit()
    return render_template("Repetiteur/Recherche/candidature_rep.html", usersRepetiteur=usersRepetiteur, listCandidature=listCandidature)

@app.route("/Supprimer_Candidature/<int:IdCandidature>", methods=['GET', 'POST'])
@login_required
def Supprimer_Candidature(IdCandidature):
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    cursor.execute(
        "DELETE FROM Candidature WHERE IdCandidature = ?", IdCandidature)

    cursor.commit()

    return redirect(url_for("Mes_candidature"))


@app.route("/mes_parent")
@login_required
def mes_parents():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    
    cursor.execute("SELECT * FROM ContratPar_Rep Co JOIN  Parent P ON Co.IdParent= P.IdParent JOIN users U ON P.IdUser=U.IdUser WHERE Co.IdRepetiteur = ?", usersRepetiteur[0])
    ContractPar_Rep = cursor.fetchall()

    cursor.commit()
    return render_template("Repetiteur/Mes_parent/mes_parent.html", usersRepetiteur=usersRepetiteur, ContractPar_Rep=ContractPar_Rep)

@app.route("/info_repetiteur")
@login_required
def info_repetiteur():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    cursor.commit()
    return render_template("Repetiteur/info_repetiteur.html", usersRepetiteur=usersRepetiteur)

# DEFIN RECHERCHE_REPETITEUR
# FIN REPETITEUR


@app.route('/deconnexion')
@login_required
def deconnexion():
    # Supprimer l'ID de l'utilisateur de la session lors de la déconnexion
    session.pop('user_id', None)
    flash("Vous avez été déconnecté.", "success")
    return redirect(url_for('connexion'))

# Route du mot de passe oublié


@app.route('/mot_de_passe_oublie')
def mot_de_passe_oublie():
    return render_template('Authentification/mot_de_passe_oublie.html')


@app.route('/mot_de_passe_oublie_traitement', methods=['POST'])
def mot_de_passe_oublie_traitement():
    if request.method == 'POST':
        email = request.form['Email']

        cursor = conn.cursor()
        cursor.execute("SELECT IdUser FROM users WHERE email = ?", (email,))

        # Récupérer les résultats de la requête
        result = cursor.fetchone()

        cursor.close()

        if result:
            #             # Si l'e-mail existe, rediriger vers la page de réinitialisation avec l'ID associé
            # flash('E-mail trouvé. Redirection vers la page "/grace".')
            return redirect(url_for('réinitialiser', user_id=result[0]))
        else:
            # Si l'e-mail n'existe pas, afficher un message d'erreur
            flash('E-mail non trouvé. Veuillez réessayer.', 'danger')
            # Assurez-vous d'ajuster la route de redirection
            return redirect(url_for('mot_de_passe_oublie'))

    # Si la requête n'est pas POST ou si l'e-mail n'existe pas, rester sur la même page
    # Assurez-vous d'ajuster le nom du template
    return render_template("mot_de_passe_oublie.html")


@app.route('/réinitialiser/<int:user_id>')
def réinitialiser(user_id):
    # Traitez l'ID de l'utilisateur comme nécessaire dans cette route
    return render_template('Authentification/réinitialiser.html', user_id=user_id)


@app.route("/réinitialiser_traitement/<int:user_id>",  methods=["GET", "POST"])
def réinitialiser_traitement(user_id):
    if request.method == 'POST':
        mot_de_passe = request.form["mot_de_passe"]

        mot_de_passe_hache = bcrypt.generate_password_hash(
            mot_de_passe).decode('utf-8')

        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET mot_de_passe = ? WHERE IdUser = ?",
                       (mot_de_passe_hache, user_id))
        conn.commit()

        flash('Modification réussie! Connectez-vous maintenant.', 'success')

    return render_template('Authentification/connexion.html')


@app.route("/dashboard_admin")
def dashboard_admin():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM users')
    TotalUsers = cursor.fetchone()[0]
    # Remplacez 'nom_table_utilisateurs' par le nom réel de votre table d'utilisateurs
    cursor.execute('SELECT COUNT(*) FROM Parent P join users U on U.IdUser=P.IdUser')
    TotalParent = cursor.fetchone()[0]
    poucentageParent=(TotalParent*100)/TotalUsers
    
    cursor.execute('SELECT COUNT(*) FROM Repetiteur R join users U on U.IdUser=R.IdUser')
    TotalRepetiteur = cursor.fetchone()[0]
    poucentageRepetiteur=(TotalRepetiteur*100)/TotalUsers
    
    cursor.execute('SELECT COUNT(*) FROM Personnel_Eveil Pe join users U on U.IdUser=Pe.IdUser')
    TotalPersonnel = cursor.fetchone()[0]
    poucentagePersonnel=(TotalPersonnel*100)/TotalUsers
    
    cursor.execute('SELECT COUNT(*) FROM ContratPar_Rep')
    TotalContrat = cursor.fetchone()[0]
    
    

    
    return render_template("PersonnelEveil+/accueil/dahs_acceuil.html",
                           usersPersoEveil=usersPersoEveil,
                           TotalParent=TotalParent,
                           TotalRepetiteur=TotalRepetiteur,
                           TotalContrat=TotalContrat,
                           TotalPersonnel=TotalPersonnel,
                           poucentagePersonnel=poucentagePersonnel,
                           poucentageRepetiteur=poucentageRepetiteur,
                           poucentageParent=poucentageParent,
                           TotalUsers=TotalUsers)

@app.route("/profil_persoEveil")
@login_required
def profil_persoEveil():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()


    # Pas besoin de cursor.commit() ici car vous n'effectuez que des sélections

    return render_template("Profil/profil_persoEveil.html", usersPersoEveil=usersPersoEveil)


@app.route("/messagerie")
def messagerie():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    return render_template("PersonnelEveil+/messagerie/msg_dash.html", usersPersoEveil=usersPersoEveil)


@app.route("/accueil_parent_dash")
def accueil_parent_dash():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    
    cursor.execute("SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser")
    data = cursor.fetchall()
    return render_template("PersonnelEveil+/parent/accueil_parent_dash.html",data=data, usersPersoEveil=usersPersoEveil)

@app.route("/Ajout_parent", methods=['GET', 'POST'])
def Ajout_parent():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    
    return render_template("PersonnelEveil+/parent/Ajout_par.html", usersPersoEveil=usersPersoEveil)


@app.route("/Succes_ajout_parent", methods=['GET', 'POST'])
def Succes_ajout_parent():
    if request.method == 'POST':
        Email = request.form["Email"]
        mot_de_passe = request.form["mot_de_passe"]
        confirm_mot_de_passe = request.form["confirm_mot_de_passe"]
        Roles = request.form["Roles"]
        NomParent = request.form["NomParent"]
        PrenomParent = request.form["PrenomParent"]
        # LieuHabitation = request.form["LieuHabitation"]
        TelephoneParent1 = request.form["TelephoneParent1"]
        # TelephonePparent2 = request.form["TelephonePparent2"]
        if not all([Email, mot_de_passe, confirm_mot_de_passe, Roles, NomParent, PrenomParent, TelephoneParent1]):
            flash('Veuillez remplir tous les champs du formulaire.', 'danger')
            return redirect(url_for('Ajout_parent'))

        mot_de_passe_hache = bcrypt.generate_password_hash(mot_de_passe).decode('utf-8')
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*)  FROM users WHERE Email = '{Email}'")
        # Récupérer le résultat
        row_count = cursor.fetchone()[0]
        if row_count != 0:
            print()
            flash(f"L'utilisateur {Email} existe déjà.", 'danger')
            return redirect(url_for('Ajout_parent'))
        else:

            cursor.execute(f"INSERT INTO users (Email, mot_de_passe, Roles, path_PhotoProfil) VALUES ('{Email}','{mot_de_passe_hache}','{Roles}', 'default_profil.png')")
            cursor.execute("SELECT SCOPE_IDENTITY()")
            listId = cursor.fetchone()
            cursor.execute(f"INSERT INTO Parent (NomParent, PrenomParent,TelephoneParent1, IdUser) VALUES ('{NomParent}', '{PrenomParent}', '{TelephoneParent1}', '{listId[0]}')")
            # Commit des modifications
            conn.commit()
            flash('Inscription réussie!', 'success')
            return redirect(url_for('accueil_parent_dash'))
    return render_template("PersonnelEveil+/parent/accueil_parent_dash.html")

@app.route("/Supprimer_parent/<int:IdParent>", methods=['GET', 'POST'])
@login_required
def Supprimer_parent(IdParent):
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    
    cursor.execute(
        "DELETE P FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE P.IdParent = ?", IdParent)

    cursor.commit()
    flash('Suppression éffectuée avec succès', 'success')
    return redirect(url_for("accueil_parent_dash"))

@app.route("/accueil_repetiteur_dash")
def accueil_repetiteur_dash():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    
    cursor.execute("SELECT R.*, NomCompetence, U.*, D.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence JOIN Dispense D on D.IdRepetiteur=R.IdRepetiteur")
    data = cursor.fetchall()
    return render_template("PersonnelEveil+/repetiteur/accueil_repetiteur_dash.html", usersPersoEveil=usersPersoEveil, data=data)

@app.route("/Ajout_repetiteur", methods=['GET', 'POST'])
def Ajout_repetiteur():
    cursor = conn.cursor()
    IdUser = session.get('IdUser')
    # cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    
    cursor.execute("SELECT * from Competence")
    Competence = cursor.fetchall()
    conn.commit()
    return render_template("PersonnelEveil+/repetiteur/Ajout_rep.html", usersPersoEveil=usersPersoEveil, Competence=Competence)



@app.route("/Succes_ajout_repetiteur", methods=['GET', 'POST'])
def Succes_ajout_repetiteur():
    if request.method == 'POST':
        Email = request.form["Email"]
        mot_de_passe = request.form["mot_de_passe"]
        # confirm_mot_de_passe = request.form["confirm_mot_de_passe"]
        Roles = request.form["Roles"]
        NomRepetiteur = request.form["NomRepetiteur"]
        PrenomRepetiteur = request.form["PrenomRepetiteur"]
        # lieu_hab_rep = request.form["lieu_hab_rep"]
        # DateNaissance = request.form["DateNaissance"]
        # AnneeExperience = request.form["AnneeExperience"]
        # NiveauRepetiteur = request.form["NiveauRepetiteur"]
        EstActif = request.form["EstActif"]
        IdCompetence = request.form["IdCompetence"]
        # Vérifier si tous les champs sont remplis
        if not all([Email, mot_de_passe, Roles, NomRepetiteur, PrenomRepetiteur, EstActif, IdCompetence]):
            flash('Veuillez remplir tous les champs du formulaire.', 'danger')
            return redirect(url_for('Ajout_repetiteur'))

        mot_de_passe_hache = bcrypt.generate_password_hash(
            mot_de_passe).decode('utf-8')
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*)  FROM users WHERE Email = '{Email}'")
        # Récupérer le résultat
        row_count = cursor.fetchone()[0]
        if row_count != 0:
            print()
            flash(f"L'utilisateur {Email} existe déjà.", 'danger')
            return redirect(url_for('Ajout_repetiteur'))
        else:
            cursor.execute(f"INSERT INTO users (Email, mot_de_passe, Roles, path_PhotoProfil) VALUES ('{Email}','{mot_de_passe_hache}','{Roles}', 'default_profil.png')")
            cursor.execute("SELECT SCOPE_IDENTITY()")
            listId = cursor.fetchone()

            # Définir le nom de l'image par défaut (à personnaliser selon votre structure de dossiers)
            # default_image = 'default_profil.png'

            cursor.execute(f"INSERT INTO Repetiteur (NomRepetiteur, PrenomRepetiteur, EstActif, IdCompetence, IdUser) VALUES ('{NomRepetiteur}','{PrenomRepetiteur}','{EstActif}','{IdCompetence}','{listId[0]}')")
            # Commit des modifications
            conn.commit()
            flash('Inscription réussie!', 'success')
            return redirect(url_for('accueil_repetiteur_dash'))
    return render_template("PersonnelEveil+/repetiteur/Ajout_rep.html")


#
@app.route("/Supprimer_repetiteur/<int:IdRepetiteur>", methods=['GET', 'POST'])
@login_required
def Supprimer_repetiteur(IdRepetiteur):
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    
    cursor.execute(
        "DELETE R FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Dispense D on D.IdRepetiteur=R.IdRepetiteur WHERE R.IdRepetiteur = ?", IdRepetiteur)
    cursor.commit()
    flash('Suppression éffectuée avec succès', 'success')
    return redirect(url_for("accueil_repetiteur_dash"))


@app.route("/List_contract")
def List_contract():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    cursor.close()
    
    cursor = conn.cursor()
    # cursor.execute(
    #     "select * from ContratPar_Rep C join Parent P on C.IdParent= P.IdParent join Repetiteur R on C.IdRepetiteur= R.IdRepetiteur JOIN Dispense D ON R.IdRepetiteur=D.IdRepetiteur join Competence Co ON R.IdCompetence = Co.IdCompetence")
    # InfoUser = cursor.fetchall()
    
    cursor.execute(
        "SELECT	* FROM ContratPar_Rep C  join Parent P on C.IdParent= P.IdParent join Repetiteur R on C.IdRepetiteur= R.IdRepetiteur")
    ListContrats = cursor.fetchall()
    cursor.execute(
        "select * from Parent P join  users U on P.IdUser= U.IdUser")
    ListParent = cursor.fetchall()
    
    cursor.execute(
        "select distinct * from Repetiteur R JOIN Dispense D ON R.IdRepetiteur=D.IdRepetiteur join Competence Co ON R.IdCompetence = Co.IdCompetence join users U on R.IdUser= U.IdUser")
    ListRepetiteur = cursor.fetchall()
    
    cursor.execute("SELECT * FROM ClassePrimaire")
    ClassePrimaire = cursor.fetchall()

    cursor.execute("SELECT * FROM ClasseCollege")
    ClasseCollege = cursor.fetchall()

    cursor.execute("SELECT * FROM ClasseLycee")
    ClasseLycee = cursor.fetchall()

    cursor.execute("SELECT * FROM MatiereSciences")
    MatiereSciences = cursor.fetchall()

    cursor.execute("SELECT * FROM MatiereLitteraire")
    MatiereLitteraire = cursor.fetchall()
    # StatusContract = cursor.fetchall()[0][1]
    # print(ListContracts)
    # print(StatusContract)
    cursor.close()
    return render_template("PersonnelEveil+/Contract/List_contract.html",
                           usersPersoEveil=usersPersoEveil,
                           ListContrats=ListContrats, 
                           ListParent=ListParent,
                           ListRepetiteur=ListRepetiteur,
                           MatiereSciences=MatiereSciences, 
                           MatiereLitteraire=MatiereLitteraire, 
                           ClassePrimaire=ClassePrimaire, 
                           ClasseCollege=ClasseCollege, 
                           ClasseLycee=ClasseLycee
                           )

@app.route("/Success_ajout_contract", methods=['GET','POST'])
def Success_ajout_contract():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    cursor.close()
    if request.method == "POST":
        # Récupérer les données modifiées du formulaire
        IdParent = request.form.get("IdParent")
        IdRepetiteur = request.form.get("IdRepetiteur")
        StatutContrat = request.form.get("StatutContrat")
        DateDebutContrat = request.form.get("DateDebutContrat")
        DateFinContrat = request.form.get("DateFinContrat")
        Classe = ', '.join(request.form.getlist("Classe[]"))
        Matiere = ', '.join(request.form.getlist("Matiere[]"))
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*)  FROM ContratPar_Rep C  join Parent P on C.IdParent= P.IdParent join Repetiteur R on C.IdRepetiteur= R.IdRepetiteur WHERE C.IdParent =? AND C.IdRepetiteur =?",(IdParent,IdRepetiteur))
        # Récupérer le résultat
        ContractExiste = cursor.fetchone()[0]
        if ContractExiste != 0:
            print()
            flash(f"Il existe déjà un contract entre ce parent et ce répétiteur", 'danger')
            return redirect(url_for('List_contract'))
        else:
            cursor.execute(f"INSERT INTO ContratPar_Rep (StatutContrat,DateDebutContrat, IdParent,IdRepetiteur, DateFinContrat,Classe,Matiere) VALUES ('{StatutContrat}','{DateDebutContrat}', '{IdParent}', '{IdRepetiteur}', '{DateFinContrat}','{Classe}','{Matiere}')")
            # Commit des modifications
            conn.commit()
            flash(f'Le parent et le répétiteur ont été mis en relation.', 'success')
            return redirect(url_for('List_contract'))   
    return render_template("PersonnelEveil+/Contract/List_contract.html", usersPersoEveil=usersPersoEveil)

@app.route("/Modif_contrat/<int:IdContrat>", methods=['GET', 'POST'])
@login_required
def Modif_contrat(IdContrat):
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    if request.method == "POST":
        # Récupérer les données modifiées du formulaire
        IdParent = request.form.get("IdParent")
        IdRepetiteur = request.form.get("IdRepetiteur")
        # StatutContrat = request.form.get("StatutContrat")
        DateDebutContrat = request.form.get("DateDebutContrat")
        DateFinContrat = request.form.get("DateFinContrat")
        Classe = ', '.join(request.form.getlist("Classe[]"))
        Matiere = ', '.join(request.form.getlist("Matiere[]"))
        
        cursor.execute(
            "UPDATE ContratPar_Rep SET DateDebutContrat=?, IdParent=?, IdRepetiteur=?, DateFinContrat=?,Classe=?, Matiere=?  WHERE IdContrat = ?", 
                (DateDebutContrat,IdParent,IdRepetiteur,DateFinContrat,Classe,Matiere,IdContrat))
        cursor.commit()
        flash('Modification éffectuée avec succès', 'success')
        return redirect(url_for("List_contract"))

@app.route("/Supprimer_contrat/<int:IdContrat>", methods=['GET', 'POST'])
@login_required
def Supprimer_contrat(IdContrat):
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Personnel_Eveil P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersPersoEveil = cursor.fetchone()
    
    cursor.execute(
        "DELETE FROM ContratPar_Rep WHERE IdContrat = ?", IdContrat)
    cursor.commit()
    flash('Suppression éffectuée avec succès', 'success')
    return redirect(url_for("List_contract"))

if __name__ == "__main__":
    app.secret_key = 'admin123'
    socketio.run(app, debug=True)
    # app.run(debug=True)
