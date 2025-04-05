# tools.py
import os
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from cachetools import cached, TTLCache
import json # Pour une éventuelle sérialisation plus robuste

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Définir le répertoire des documents (ajuste si nécessaire)
# Utilise un chemin relatif pour la portabilité
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')
logger.info(f"Répertoire des documents configuré : {DOCUMENTS_DIR}")

# --- Chargement et Vectorisation (avec cache) ---
# Cache pour 1 heure
cache = TTLCache(maxsize=10, ttl=3600)

@cached(cache)
def load_documents():
    """Charge les documents .txt depuis DOCUMENTS_DIR. Retourne un dict {filename: content}."""
    documents_content = {}
    logger.info(f"Tentative de chargement des documents depuis : {DOCUMENTS_DIR}")
    if not os.path.exists(DOCUMENTS_DIR) or not os.path.isdir(DOCUMENTS_DIR):
        logger.error(f"Le répertoire des documents n'existe pas ou n'est pas un dossier : {DOCUMENTS_DIR}")
        return {}
    try:
        filenames = [f for f in os.listdir(DOCUMENTS_DIR) if f.endswith('.txt') and os.path.isfile(os.path.join(DOCUMENTS_DIR, f))]
        logger.info(f"Fichiers .txt trouvés : {filenames}")
        for filename in filenames:
            file_path = os.path.join(DOCUMENTS_DIR, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    documents_content[filename] = f.read()
            except Exception as e:
                logger.error(f"Erreur lors de la lecture du fichier {filename}: {e}")
        logger.info(f"{len(documents_content)} documents chargés avec succès.")
        if not documents_content:
             logger.warning("Aucun document .txt n'a pu être chargé.")
        return documents_content
    except Exception as e:
        logger.error(f"Erreur lors du listage du répertoire {DOCUMENTS_DIR}: {e}")
        return {}

@cached(cache)
def get_vectorizer_and_matrix():
    """
    Initialise/Récupère le vectoriseur TF-IDF et la matrice à partir des documents chargés.
    Retourne (vectorizer, tfidf_matrix, list_of_doc_names).
    Retourne (None, None, []) si aucun document n'est chargé.
    """
    documents_content = load_documents()
    if not documents_content:
        logger.warning("Aucun document chargé, impossible d'initialiser le vectoriseur.")
        return None, None, []

    doc_names = list(documents_content.keys())
    doc_texts = list(documents_content.values())

    try:
        logger.info("Initialisation/Calcul du Vectoriseur TF-IDF...")
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(doc_texts)
        logger.info(f"Vectoriseur TF-IDF prêt pour {len(doc_names)} documents.")
        return vectorizer, tfidf_matrix, doc_names
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation TF-IDF : {e}")
        return None, None, []

# --- Fonctions Outils (appelables par FastAPI via l'orchestration LLM) ---

def search_relevant_documents(query: str) -> str:
    """
    Recherche les documents pertinents pour une requête en utilisant TF-IDF.
    Retourne une chaîne JSON d'une liste de dictionnaires [{'name': doc_name, 'score': similarity_score}]
    triée par pertinence, ou un message d'erreur/informatif.
    """
    logger.info(f"Recherche de documents pour la requête : '{query}'")
    vectorizer, tfidf_matrix, doc_names = get_vectorizer_and_matrix()

    if not doc_names or vectorizer is None:
        logger.warning("Recherche impossible : Vectoriseur non initialisé (aucun document?).")
        return json.dumps([{"message": "Le système de recherche n'est pas prêt (aucun document chargé)."}])

    try:
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

        # Créer une liste de résultats avec scores
        results = [
            {"name": name, "score": float(score)}
            for name, score in zip(doc_names, similarities)
        ]

        # Filtrer et trier
        # Garder seulement les documents avec un score > seuil (ajuster si nécessaire)
        relevant_docs = [doc for doc in results if doc['score'] > 0.05]
        sorted_docs = sorted(relevant_docs, key=lambda x: x['score'], reverse=True)

        if not sorted_docs:
            logger.info("Aucun document pertinent trouvé pour cette requête.")
            return json.dumps([{"message": "Aucun document pertinent trouvé pour cette requête."}])

        logger.info(f"Documents pertinents trouvés : {[d['name'] for d in sorted_docs]}")
        # Retourner le résultat sous forme de chaîne JSON pour l'IA
        return json.dumps(sorted_docs)

    except Exception as e:
        logger.error(f"Erreur pendant la recherche TF-IDF pour '{query}': {e}", exc_info=True)
        return json.dumps([{"error": f"Erreur interne pendant la recherche: {e}"}])


def get_document_content_by_name(document_name: str) -> str:
    """
    Obtient le contenu complet d'un document spécifique par son nom.
    Retourne une chaîne JSON {'name': doc_name, 'content': content} ou {'error': message}.
    """
    logger.info(f"Tentative de récupération du contenu pour : {document_name}")
    documents_content = load_documents() # Utilise le cache
    content = documents_content.get(document_name)

    if content is not None:
        logger.info(f"Contenu de {document_name} trouvé.")
        # Optionnel: tronquer si trop long pour le contexte de l'IA ?
        # MAX_CONTENT_LENGTH = 5000
        # if len(content) > MAX_CONTENT_LENGTH:
        #     content = content[:MAX_CONTENT_LENGTH] + "\n... [Contenu tronqué]"
        #     logger.warning(f"Contenu de {document_name} tronqué car trop long.")
        return json.dumps({'name': document_name, 'content': content})
    else:
        logger.warning(f"Document '{document_name}' non trouvé dans les documents chargés.")
        # Vérifier si le fichier existe physiquement pour aider au debug
        file_path = os.path.join(DOCUMENTS_DIR, document_name)
        if os.path.exists(file_path):
             logger.warning(f"Le fichier {document_name} existe mais n'a pas été chargé. Vérifier l'extension ou les logs de chargement.")
             return json.dumps({'error': f"Document '{document_name}' existe mais n'a pas été chargé correctement."})
        else:
             logger.warning(f"Le fichier {document_name} n'existe pas dans {DOCUMENTS_DIR}.")
             return json.dumps({'error': f"Document '{document_name}' non trouvé."})


def generate_simplified_checklist(topic: str) -> str:
    """
    Génère une checklist simplifiée pour une démarche administrative donnée.
    NOTE POUR LE HACKATHON : Ceci est une maquette. Retourne une checklist prédéfinie.
    Retourne une chaîne JSON {'topic': topic, 'checklist': list_of_steps} ou {'message': ...}.
    """
    logger.info(f"Génération de checklist demandée pour : {topic}")
    topic_lower = topic.lower()
    checklist = [] # Initialise une liste vide

    # Logique de maquette pour le hackathon
    if "prime toiture" in topic_lower or ("fernelmont" in topic_lower and "toiture" in topic_lower):
        checklist = [
            "1. Vérifier l'éligibilité sur le site officiel de la Wallonie.",
            "2. Rassembler les devis détaillés d'entrepreneurs agréés.",
            "3. Si requis, obtenir le rapport d'audit logement.",
            "4. Compléter le formulaire de demande officiel (en ligne ou papier).",
            "5. Joindre toutes les annexes demandées (devis, audit, preuves photos...).",
            "6. Soumettre le dossier complet à l'administration compétente.",
            "7. Conserver une copie et suivre l'avancement du dossier."
        ]
        logger.info(f"Checklist 'Prime Toiture' générée pour '{topic}'.")
        return json.dumps({"topic": topic, "checklist": checklist})
    elif "carte d'identité" in topic_lower or "eid" in topic_lower:
         checklist = [
              "1. Prendre rendez-vous auprès de votre administration communale.",
              "2. Se munir de sa convocation (si reçue) et de l'ancienne carte.",
              "3. Apporter une photo d'identité récente et conforme.",
              "4. Payer la redevance communale.",
              "5. Enregistrer les empreintes digitales.",
              "6. Récupérer la nouvelle carte et les codes PIN/PUK après convocation."
         ]
         logger.info(f"Checklist 'Carte d'identité' générée pour '{topic}'.")
         return json.dumps({"topic": topic, "checklist": checklist})
    else:
        logger.info(f"Aucune checklist prédéfinie trouvée pour '{topic}'.")
        return json.dumps({"message": f"Je n'ai pas de checklist spécifique prédéfinie pour '{topic}'."})


def request_human_escalation(user_query: str, reason: str) -> str:
    """
    Signale qu'une requête utilisateur nécessite une intervention humaine.
    NOTE POUR LE HACKATHON : Logue simplement la demande.
    Retourne une chaîne JSON {'status': 'success', 'message': confirmation}.
    """
    logger.warning(f"ESCALADE HUMAINE DEMANDÉE")
    logger.warning(f"  Requête Utilisateur: '{user_query}'")
    logger.warning(f"  Raison: '{reason}'")
    # Ici, on pourrait envoyer un email, créer un ticket dans un système, etc.
    confirmation_message = f"Votre demande concernant '{user_query}' a été transmise à un agent pour examen. Raison: {reason}. Nous vous recontacterons si nécessaire."
    return json.dumps({"status": "success", "message": confirmation_message})