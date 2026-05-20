from rag import *
from flask import Flask, render_template, request, session
import os
from config import Config
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = app.config["MAX_CONTENT_LENGTH"]
UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not app.secret_key:
    raise ValueError("SECRET_KEY not found in .env")


chunks = []


@app.route("/", methods = ["GET", "POST"])
def home():
    global chunks

    if "chat_history" not in session:
        session["chat_history"] = []

    answer = ''
    message = ''

    if request.method == 'POST':
        if 'file' in request.files:
            files = request.files.getlist("file")
            all_chunks = []
            for file in files:
                if file.filename == "":
                    continue

                filename = secure_filename(file.filename)
                path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(path)
                text = read_file(path)
                if text and text != "Unsupported file format":
                    file_chunks = chunk_text(text)
                    all_chunks.extend(file_chunks)
            if all_chunks:

                chunks = all_chunks

                build_index(chunks)

                message = "Files uploaded and indexed successfully."

            else:
                message = "Could not read files."

        elif request.form.get('query'):
            query = request.form.get('query')
            if not chunks:
                message = 'Upload a file first.'
            else:
                try:
                    context = search_chunks(query)
                    answer = ask_llm(context, query, session["chat_history"])
                except Exception as e:
                    answer = f"Error: {str(e)}"

                session["chat_history"].append({
                    "user": query,
                    "ai": answer
                })

                if len(session["chat_history"]) > 20:
                    session["chat_history"].pop(0)

                session.modified = True
                
    return render_template('index.html', answer=answer, message=message)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)