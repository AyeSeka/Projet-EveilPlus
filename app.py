from datetime import datetime
import os
import pyodbc
from flask import Flask, jsonify, render_template, request,  redirect, sessions, url_for, flash, session
from flask_bcrypt import Bcrypt
from functools import wraps
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
# from flask_sse import sse
from flask_socketio import SocketIO, emit, join_room

# from flask_login import current_user, login_required
app = Flask(__name__)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)


# app.config["REDIS_URL"] = "redis://localhost:6379/0"
# app.register_blueprint(sse, url_prefix='/sse')


conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=Geek_Machine\SQLEXPRESS;"
                       "Database=eveil_plus;"
                       "Trusted_Connection=yes")

# conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
#                        "Server=DESKTOP-QQGKONI\SQLEXPRESS;"
#                        "Database=eveil_plus;"
#                        "Trusted_Connection=yes")

# conn = pyodbc.connect(
#     'Driver={SQL Server};'
#     'Server=HP\\SQLEXPRESS;'
#     'Database=eveil_plus;'
#     'user=HP\\goliy;'

# )

# connection_string = (
#     "Driver={ODBC Driver 17 for SQL Server};"
#     "Server=DESKTOP-K074SIS\SQLEXPRESS;"
#     "Database=ivoryExplore;"
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


app.config['UPLOAD_FOLDER_PARENT'] = UPLOAD_FOLDER_PARENT
app.config['UPLOAD_FOLDER_REPETITEUR'] = UPLOAD_FOLDER_REPETITEUR


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['SESSION_TYPE'] = 'filesystem'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ? Modifier photo de profil du parent
# Route pour la modification du profil (y compris la mise à jour de la photo de profil)
@app.route('/upload_profile_photo_parent', methods=['POST'])
def upload_profile_photo_parent():
    if 'photo' not in request.files:
        return redirect(request.url)

    file = request.files['photo']

    if file.filename == '':
        return redirect(request.url)

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
        return redirect(request.url)

    file = request.files['photo']

    if file.filename == '':
        return redirect(request.url)

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
@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    print(f'Client a rejoint la salle : {room}')


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


# @app.route("/inscriptionParent", methods=['GET', 'POST'])
# def inscriptionParent():
#     return render_template("Authentification/inscriptionParent.html")

# @app.route("/Succes_inscription_parent", methods=['GET', 'POST'])
# def Succes_inscription_parent():
#     if request.method == 'POST':
#         Email = request.form["Email"]
#         mot_de_passe = request.form["mot_de_passe"]
#         confirm_mot_de_passe = request.form["confirm_mot_de_passe"]
#         Roles = request.form["Roles"]
#         NomParent = request.form["NomParent"]
#         PrenomParent = request.form["PrenomParent"]
#         LieuHabitation = request.form["LieuHabitation"]
#         TelephoneParent1 = request.form["TelephoneParent1"]
#         TelephonePparent2 = request.form["TelephonePparent2"]
#         if not all([Email, mot_de_passe, confirm_mot_de_passe, Roles, NomParent, PrenomParent, LieuHabitation, TelephoneParent1, TelephonePparent2]):
#             flash('Veuillez remplir tous les champs du formulaire.', 'danger')
#             return redirect(url_for('inscriptionParent'))

#         mot_de_passe_hache = bcrypt.generate_password_hash(mot_de_passe).decode('utf-8')
#         cursor = conn.cursor()
#         cursor.execute(f"INSERT INTO users (Email, mot_de_passe, Roles) VALUES ('{Email}','{mot_de_passe_hache}','{Roles}')")
#         cursor.execute("SELECT SCOPE_IDENTITY()")
#         listId = cursor.fetchone()
#         cursor.execute(f"INSERT INTO Parent (NomParent, PrenomParent, LieuHabitation, TelephoneParent1, TelephonePparent2, IdUser) VALUES ('{NomParent}', '{PrenomParent}', '{LieuHabitation}', '{TelephoneParent1}', '{TelephonePparent2}', '{listId[0]}')")
#         # Commit des modifications
#         conn.commit()
#         flash('Inscription réussie! Connectez-vous maintenant.', 'success')
#         return redirect(url_for('connexion'))
#     return render_template("Authentification/inscriptionParent.html")

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

        mot_de_passe_hache = bcrypt.generate_password_hash(
            mot_de_passe).decode('utf-8')
        cursor = conn.cursor()
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


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'IdUser' not in session:
            return redirect(url_for('connexion'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/accueil_parent")
@login_required
def Accueil_parent():
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

    if usersParent:
        # Assurez-vous de remplacer l'indice par celui approprié dans votre résultat SQL
        prenom_parent = usersParent[1]
        # Assurez-vous de remplacer l'indice par celui approprié dans votre résultat SQL
        nom_parent = usersParent[2]

        flash(f'Bienvenue, cher parent {prenom_parent} {nom_parent}!', 'success')
        # Ajoutez cette ligne pour indiquer que l'utilisateur vient de se connecter
        session['just_logged_in'] = True

        return render_template("Parents/accueil_parent.html", usersParent=usersParent, photo_path=photo_path)
    else:
        flash('Répétiteur non trouvé.', 'danger')
        return redirect(url_for('connexion'))


@app.route("/poste", methods=["GET", "POST"])
@login_required
def poste():
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
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    # for lieu in lieu_repetiteur:
    #     print(lieu[0])
    # print(lieu_repetiteur)

    # print(niveauEtudiant)
    conn.commit()
    return render_template("Parents/Postes/poste.html", usersParent=usersParent, niveauEtudiant=niveauEtudiant, lieu_repetiteur=lieu_repetiteur, photo_path=photo_path)


@app.route("/recapitulatif", methods=["GET", "POST"])
@login_required
def recapitulatif():
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
            return redirect(url_for('poste'))

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
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    cursor.commit()
    return render_template("Parents/Postes/recapitulatif.html", usersParent=usersParent, data_recap=data_recap, photo_path=photo_path)


@app.route("/Modif_recap", methods=["GET", "POST"])
@login_required
def Modif_recap():
    IdUser = session.get('IdUser')
    data_recap = session.get('data_recap', {})

    if request.method == "POST":
        # Récupérer les données modifiées du formulaire
        habitation = request.form.get("habitation")
        niveau = ', '.join(request.form.getlist("niveau[]"))
        enfant = request.form.get("enfant")
        seance = request.form.get("seance")
        date_limite = request.form.get("date_limite")

        # Mettre à jour les données dans la session
        data_recap.update({
            'habitation': habitation,
            'niveau': niveau,
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
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    cursor.commit()

    return render_template("Parents/Postes/Modif_recap.html", usersParent=usersParent, data_recap=data_recap, niveauEtudiant=niveauEtudiant, photo_path=photo_path)


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
    cursor.execute(f"INSERT INTO Poste (NbreEnfant, NbresJours, lieu_habitation, NiveauEnfant, DateLimte, DatePublication, IdParent) VALUES ('{data_recap['enfant']}','{data_recap['seance']}','{data_recap['habitation']}','{data_recap['niveau']}','{data_recap['date_limite']}','{date_publication}','{usersParent[0]}')")

    cursor.execute("SELECT SCOPE_IDENTITY()")
    IdPoste = cursor.fetchone()
    cursor.execute(
        f"INSERT INTO HistoriquePoste (IdPoste) VALUES ('{IdPoste[0]}')")

    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')
    conn.commit()
    flash("Poste enrégistré avec succès ! Consultez l'historique de vos dans ""Mes Postes""", 'success')
    return redirect(url_for("poste"), photo_path=photo_path)


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
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    return render_template("Parents/Postes/poste_sucess.html", usersParent=usersParent, photo_path=photo_path)

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
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    cursor.commit()
    return render_template("Parents/Postes/Mes_postes.html", usersParent=usersParent, poste_data=poste_data, photo_path=photo_path)


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

    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    cursor.commit()

    return redirect(url_for("Mes_postes"), photo_path=photo_path)
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

    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    # print(datalist_habitation)
    # print(datalist_niveau)
    # print(datalist_experience)

    # print(datalist_competence)

    # for specialite in datalist_specialite:
    #     print(specialite[3])

    # return render_template("Parents/Recherches/recherche.html", usersParent=usersParent)
    return render_template("Parents/Recherches/recherche.html", datalist_habitation=datalist_habitation, datalist_niveau=datalist_niveau, datalist_experience=datalist_experience, datalist_competence=datalist_competence, usersParent=usersParent, photo_path=photo_path)


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

    query = """SELECT  * FROM Repetiteur r JOIN Dispense d ON r.IdRepetiteur=d.IdRepetiteur join Competence c ON (r.IdCompetence = c.IdCompetence)
            

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

    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    cursor.commit()

    # return render_template("Parents/Recherches/liste_recherche.html", usersParent=usersParent)
    return render_template("Parents/Recherches/liste_recherche.html", specialite=specialite, repetiteurs=repetiteurs, usersParent=usersParent, MatiereSciences=MatiereSciences, MatiereLitteraire=MatiereLitteraire, ClassePrimaire=ClassePrimaire, ClasseCollege=ClasseCollege, ClasseLycee=ClasseLycee, etat_repetiteur=etat_repetiteur, photo_path=photo_path)

# @app.route("/liste_repetiteurchoix")
# @login_required
# def liste_repetiteurchoix():
#     IdUser = session.get('IdUser')
#     cursor = conn.cursor()
#     cursor.execute(
#         "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", IdUser)
#     usersParent = cursor.fetchone()
#     cursor.commit()
#     return render_template("Parents/Recherches/liste_repetiteurchoix.html", usersParent=usersParent)


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
        cursor.execute(
            "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
        result = cursor.fetchone()

        if result and result[0]:
            photo_path = result[0]
        else:
            photo_path = url_for(
                'static', filename='/img/user_img/user_avatar.jpg')

        cursor.commit()
        # flash('Le répétiteur a été choisi avec succès.', 'success')
        return jsonify(result='Success', IdRepetiteur=IdRepetiteur, contractExists=False, photo_path=photo_path)

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
        "SELECT * FROM ContratTemporaire Co JOIN Parent P ON Co.IdParent=P.IdParent JOIN Repetiteur R ON Co.IdRepetiteur=R.IdRepetiteur")
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
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    cursor.commit()
    flash('Choix retiré avec succès.', 'danger')
    return redirect(url_for("Mes_choix_rer"), photo_path=photo_path)

# Debut profil


@app.route("/profil_parent")
@login_required
def profil_parent():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (IdUser,))
    usersParent = cursor.fetchone()

    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    # Pas besoin de cursor.commit() ici car vous n'effectuez que des sélections

    return render_template("Profil/profil_parent.html", usersParent=usersParent, photo_path=photo_path)


@app.route("/ModifProfil_par")
@login_required
def ModifProfil_par():
    user_id = session.get('IdUser')
    cursor = conn.cursor()
    # Sélectionner les informations existantes de l'utilisateur
    cursor.execute(
        "SELECT P.*, U.* FROM Parent P JOIN users U ON P.IdUser=U.IdUser WHERE U.IdUser = ?", (user_id,))
    user_data = cursor.fetchone()
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    cursor.close()
    return render_template("Profil/ModifProfil_par.html", usersParent=user_data, photo_path=photo_path)


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
        cursor.execute(
            "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
        result = cursor.fetchone()

        if result and result[0]:
            photo_path = result[0]
        else:
            photo_path = url_for(
                'static', filename='/img/user_img/user_avatar.jpg')

        # Commit des modifications
        conn.commit()
        flash('Votre profil à été mis à jour', 'success')
        return redirect(url_for('profil_parent'))
    return render_template("Profil/ModifProfil_par.html", usersParent=usersParent, photo_path=photo_path)


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
    cursor.commit()

    cursor = conn.cursor()
    cursor.execute("SELECT R.EstActif FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    bouton_etat = cursor.fetchone()[0]
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    conn.commit()
    return render_template("Profil/profil_repetiteur.html", usersRepetiteur=usersRepetiteur, bouton_etat=bouton_etat, photo_path=photo_path)


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
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')

    cursor.commit()
    return render_template("Parents/mes_repetiteurs/mes_repetiteurs.html", usersParent=usersParent, photo_path=photo_path)


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


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'IdUser' not in session:
            return redirect(url_for('connexion'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/accueil_repetiteur")
@login_required
def accueil_repetiteur():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')
    cursor.close()

    if usersRepetiteur:
        # Assurez-vous de remplacer l'indice par celui approprié dans votre résultat SQL
        prenom_repetiteur = usersRepetiteur[1]
        # Assurez-vous de remplacer l'indice par celui approprié dans votre résultat SQL
        nom_repetiteur = usersRepetiteur[2]

        flash(f'Bienvenue, cher répétiteur {prenom_repetiteur} {nom_repetiteur}!', 'success')
        return render_template("Repetiteur/accueil_repetiteur.html", usersRepetiteur=usersRepetiteur, photo_path=photo_path)
    else:
        flash('Répétiteur non trouvé.', 'danger')
        return redirect(url_for('connexion'))
    # return render_template("Repetiteur/accueil_repetiteur.html")
# DEBUT RECHERCHE_REPETITEUR


@app.route("/recherche_repetiteur")
@login_required
def recherche_repetiteur():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    cursor.execute(
        "SELECT path_PhotoProfil FROM users WHERE IdUser=?", (IdUser,))
    result = cursor.fetchone()

    if result and result[0]:
        photo_path = result[0]
    else:
        photo_path = url_for(
            'static', filename='/img/user_img/user_avatar.jpg')
    cursor.commit()
    return render_template("Repetiteur/Recherche/recherche_repetiteur.html", usersRepetiteur=usersRepetiteur, photo_path=photo_path)


@app.route("/liste_rech_rep")
@login_required
def liste_rech_rep():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    cursor.commit()
    return render_template("Repetiteur/Recherche/liste_rech_rep.html", usersRepetiteur=usersRepetiteur)


@app.route("/candidature_rep")
@login_required
def candidature_rep():
    IdUser = session.get('IdUser')
    cursor = conn.cursor()
    cursor.execute("SELECT R.*, NomCompetence, U.* FROM Repetiteur R JOIN users U ON R.IdUser=U.IdUser JOIN Competence C ON R.IdCompetence=C.IdCompetence WHERE U.IdUser = ?", IdUser)
    usersRepetiteur = cursor.fetchone()
    cursor.commit()
    return render_template("Repetiteur/Recherche/candidature_rep.html", usersRepetiteur=usersRepetiteur)


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
    return render_template("PersonnelEveil+/accueil/dahs_acceuil.html")


@app.route("/messagerie")
def messagerie():
    return render_template("PersonnelEveil+/messagerie/msg_dash.html")


@app.route("/accueil_parent_dash")
def accueil_parent_dash():
    return render_template("PersonnelEveil+/parent/accueil_parent_dash.html")


@app.route("/accueil_repetiteur_dash")
def accueil_repetiteur_dash():
    return render_template("PersonnelEveil+/repetiteur/accueil_repetiteur_dash.html")


if __name__ == "__main__":
    app.secret_key = 'admin123'
    socketio.run(app, debug=True)
    # app.run(debug=True)
