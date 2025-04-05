from . import app
from flask import request
import os

@app.route("/get-document/<filename>")
def read_document(filename):
    path_to_document = os.path.join("Documents", filename)
    try:
        with open(path_to_document, "r") as file:
            content = file.read()
        return {"content": content}
    except FileNotFoundError:
        return {"error": "File not found"}, 404

@app.route("/submit-response", methods=["POST"])
def submit_response():
    data = request.data.decode()
    return {"response": f"IA response to {data}"}
