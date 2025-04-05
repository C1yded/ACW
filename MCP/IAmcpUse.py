import os
from fastmcp import FastMCP

# Définir le répertoire de base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Définir le répertoire des documents
DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")

# Créer le répertoire des documents s'il n'existe pas
if not os.path.exists(DOCUMENTS_DIR):
    os.makedirs(DOCUMENTS_DIR)
    print(f"Répertoire créé : {DOCUMENTS_DIR}")

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

# Outil pour rechercher un mot-clé dans tous les documents
@app.tool('search_documents')
def search_documents(keyword: str):
    """Recherche un mot-clé dans tous les documents et retourne la liste des documents contenant ce mot-clé."""
    matching_documents = []
    for filename in os.listdir(DOCUMENTS_DIR):
        if filename.endswith('.txt'):
            file_path = os.path.join(DOCUMENTS_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if keyword.lower() in content.lower():
                    matching_documents.append(filename)
    return matching_documents

# Lancer le serveur
if __name__ == '__main__':
    app.run()