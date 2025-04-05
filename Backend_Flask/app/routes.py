# Définit les routes de ton application Flask



from flask import Flask
import os

app = Flask(__name__)

@app.route("/get-document/<filename>")
def read_document(filename):
    try:
        path_to_document = os.path.join("Documents", filename)
        with open(path_to_document, "r") as file:
            content = file.read()
        return {"content": content}
    except FileNotFoundError:
        return {"error": "File not found"}
