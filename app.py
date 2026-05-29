from rag import *
from flask import Flask, render_template, request, session, redirect, url_for
import os
from config import Config
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors
import bcrypt

app = Flask(__name__)

# ---------------- MYSQL CONFIG ---------------- #

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '200404'
app.config['MYSQL_DB'] = 'smartdoc_ai'

mysql = MySQL(app)

# ---------------- APP CONFIG ---------------- #

app.secret_key = os.getenv("SECRET_KEY")
app.config.from_object(Config)
UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not app.secret_key:
    raise ValueError("SECRET_KEY not found in .env")


# ---------------- SIGNUP ---------------- #

@app.route("/signup", methods=["GET", "POST"])
def signup():

    message = ""
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )

        cursor = mysql.connection.cursor(
            MySQLdb.cursors.DictCursor
        )

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()
        if existing_user:
            message = "Email already exists."
        else:
            cursor.execute(
                """
                INSERT INTO users(username, email, password)
                VALUES(%s, %s, %s)
                """,
                (
                    username,
                    email,
                    hashed_password
                )
            )

            mysql.connection.commit()
            message = "Signup successful."

        cursor.close()

    return render_template(
        "signup.html",
        message=message
    )


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor = mysql.connection.cursor(
            MySQLdb.cursors.DictCursor
        )

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()
        cursor.close()

        if user:
            stored_password = user['password']

            if bcrypt.checkpw(
                password.encode('utf-8'),
                stored_password.encode('utf-8')
            ):

                session['loggedin'] = True
                session['id'] = user['id']
                session['username'] = user['username']
                session['chat_history'] = []

                # -------- LOAD USER FILES -------- #

                user_folder = os.path.join(
                    UPLOAD_FOLDER,
                    str(user['id'])
                )

                all_chunks = []

                if os.path.exists(user_folder):
                    for filename in os.listdir(user_folder):

                        path = os.path.join(
                            user_folder,
                            filename
                        )

                        text = read_file(path)
                        if text and text != "Unsupported file format":
                            file_chunks = chunk_text(text)
                            all_chunks.extend(file_chunks)

                if all_chunks:
                    build_index(all_chunks)
                    session['has_files'] = True
                else:
                    session['has_files'] = False
                return redirect(url_for('home'))

            else:
                message = "Incorrect password."

        else:
            message = "User not found."

    return render_template(
        "login.html",
        message=message
    )


# ---------------- HOME ---------------- #

@app.route("/", methods=["GET", "POST"])
def home():

    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if "chat_history" not in session:
        session["chat_history"] = []

    answer = ""

    message = ""

    if request.method == "POST":

        # -------- FILE UPLOAD -------- #

        if 'file' in request.files:
            files = request.files.getlist("file")

            user_folder = os.path.join(
                UPLOAD_FOLDER,
                str(session['id'])
            )

            os.makedirs(user_folder, exist_ok=True)

            # SAVE FILES

            for file in files:
                if file.filename == "":
                    continue

                filename = secure_filename(file.filename)

                path = os.path.join(
                    user_folder,
                    filename
                )

                file.save(path)

            # REBUILD ALL USER FILES

            all_chunks = []

            for filename in os.listdir(user_folder):

                path = os.path.join(
                    user_folder,
                    filename
                )

                text = read_file(path)

                if text and text != "Unsupported file format":
                    file_chunks = chunk_text(text)
                    all_chunks.extend(file_chunks)

            if all_chunks:
                build_index(all_chunks)
                session['has_files'] = True
                message = "Files uploaded successfully."

            else:
                message = "Could not process files."

        # -------- ASK QUESTION -------- #

        elif request.form.get('query'):
            query = request.form.get('query')

            if not session.get('has_files'):
                message = "Upload files first."

            else:
                try:
                    context = search_chunks(query)

                    answer = ask_llm(
                        context,
                        query,
                        session["chat_history"]
                    )

                except Exception as e:
                    answer = f"Error: {str(e)}"

                session["chat_history"].append({
                    "user": query,
                    "ai": answer
                })

                if len(session["chat_history"]) > 20:
                    session["chat_history"].pop(0)
                session.modified = True

    return render_template(
        'index.html',
        answer=answer,
        message=message
    )


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('chat_history', None)
    session.pop('has_files', None)
    return redirect(url_for('login'))


# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    app.run(debug=False)