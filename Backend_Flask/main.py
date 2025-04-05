from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/get-document/{filename}")
async def read_document(filename: str):
    path_to_document = os.path.join("Documents", filename)
    try:
        with open(path_to_document, "r") as file:
            content = file.read()
        return {"content": content}
    except FileNotFoundError:
        return {"error": "File not found"}, 404

@app.post("/submit-response")
async def submit_response(data: str):
    return {"response": f"IA response to {data}"}
