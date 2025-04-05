import os
from fastmcp import FastMCP
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Définir le répertoire de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Définir le répertoire des documents
DOCUMENTS_DIR = r"C:\Users\Dell 7420\Documents\ACW\ACW\data"

# Créer le répertoire des documents s'il n'existe pas
if not os.path.exists(DOCUMENTS_DIR):
    os.makedirs(DOCUMENTS_DIR)
    print(f"Répertoire créé : {DOCUMENTS_DIR}")

# Charger les documents une fois au démarrage
documents = {}
for filename in os.listdir(DOCUMENTS_DIR):
    if filename.endswith('.txt'):
        file_path = os.path.join(DOCUMENTS_DIR, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            documents[filename] = f.read()

# Initialiser le vectoriseur TF-IDF avec les contenus des documents
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents.values())

# Créer une instance FastMCP
app = FastMCP(base_url='http://localhost:8000')

# Outil pour lister les documents disponibles
@app.tool('list_documents')
def list_documents():
    """Liste tous les documents .txt dans le répertoire des documents."""
    return [f for f in os.listdir(DOCUMENTS_DIR) if f.endswith('.txt')]

# Outil pour obtenir le contenu d'un document spécifique
@app.tool('get_document_content')
def get_document_content(document_name: str):
    """Obtient le contenu d'un document spécifique."""
    file_path = os.path.join(DOCUMENTS_DIR, document_name)
    if not os.path.exists(file_path):
        return {'error': 'Document non trouvé'}
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return content

# Outil pour rechercher les documents pertinents avec TF-IDF
@app.tool('search_documents')
def search_documents(query: str):
    """Recherche les documents pertinents pour une requête en utilisant TF-IDF et retourne la liste triée par pertinence."""
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    doc_names = list(documents.keys())
    sorted_docs = sorted(zip(doc_names, similarities), key=lambda x: x[1], reverse=True)
    return [doc_name for doc_name, _ in sorted_docs]

# Outil pour répondre à une requête en extrayant des informations des documents pertinents
@app.tool('answer_query')
def answer_query(query: str):
    """Répond à une requête en extrayant des informations des documents pertinents et en structurant la réponse avec des citations."""
    # Trouver les documents pertinents
    relevant_docs = search_documents(query)
    
    # Extraire des informations
    answer_parts = []
    for doc_name in relevant_docs:
        content = get_document_content(doc_name)
        if isinstance(content, dict) and 'error' in content:
            continue
        # Diviser en phrases et chercher celles contenant des mots de la requête
        words = query.lower().split()
        sentences = content.split('.')
        for sentence in sentences:
            if any(word in sentence.lower() for word in words):
                answer_parts.append(f"D'après {doc_name} : {sentence.strip()}")
    
    # Structurer la réponse
    if not answer_parts:
        return "Aucune information pertinente trouvée."
    return "\n".join(answer_parts)

# Lancer le serveur
if __name__ == '__main__':
    app.run()