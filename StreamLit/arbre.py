import streamlit as st

# Initialiser l'état si ce n'est pas déjà fait
if 'etape' not in st.session_state:
    st.session_state.etape = 1
    st.session_state.categorie = None
    st.session_state.besoin = None

# --- Étape 1: Choix de la catégorie ---
if st.session_state.etape == 1:
    st.write("Bonjour ! Quel est le sujet principal de votre demande ?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Déchets & Environnement"):
            st.session_state.categorie = "dechets"
            st.session_state.etape = 2
            st.rerun() # Important pour rafraîchir et passer à l'étape suivante
    with col2:
        if st.button("Urbanisme & Logement"):
            st.session_state.categorie = "urbanisme"
            st.session_state.etape = 2
            st.rerun()
    # Ajouter d'autres boutons de catégorie ici...
    if st.button("Autre question / Problème"):
        st.session_state.categorie = "autre"
        st.session_state.etape = 2 # Ou directement vers l'IA/Escalade
        st.rerun()


# --- Étape 2: Précision du besoin (dépend de la catégorie) ---
elif st.session_state.etape == 2:
    if st.session_state.categorie == "dechets":
        st.write("Concernant les déchets, que cherchez-vous ?")
        if st.button("Calendrier des collectes"):
            st.session_state.besoin = "calendrier"
            st.session_state.etape = 3
            st.rerun()
        if st.button("Infos Recyparc"):
            st.session_state.besoin = "recyparc"
            st.session_state.etape = 3
            st.rerun()
        if st.button("Signaler un dépôt clandestin"):
            st.session_state.besoin = "signalement_depot"
            st.session_state.etape = 3
            st.rerun()
        # Ajouter d'autres boutons ici ...

    elif st.session_state.categorie == "urbanisme":
        st.write("Concernant l'urbanisme ?")
        if st.button("Question spécifique (IA)"):
             st.session_state.besoin = "question_ia_urba"
             st.session_state.etape = 3
             st.rerun()
        # Ajouter d'autres boutons ici ...

    # Gérer les autres catégories...
    elif st.session_state.categorie == "autre":
         # Peut-être aller directement à l'IA ou à l'escalade
         st.write("Veuillez décrire votre problème dans la fenêtre de chat ci-dessous.")
         st.session_state.besoin = "chat_ia_direct"
         st.session_state.etape = 3
         st.rerun()


# --- Étape 3: Affichage du résultat / Lancement Action ---
elif st.session_state.etape == 3:
    if st.session_state.besoin == "calendrier":
        st.write("Voici le lien vers le calendrier des collectes :")
        st.markdown("[Lien vers le calendrier Fernelmont](https://www.example.com/calendrier_dechets_fernelmont.pdf)") # Mettre le vrai lien
        # Ajouter un bouton pour recommencer
        if st.button("Nouvelle demande"):
            # Réinitialiser l'état
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

    elif st.session_state.besoin == "signalement_depot":
        st.write("Ok, nous allons vous aider à préparer un signalement pour l'agent communal.")
        # ICI : Intégrer votre logique d'assistance rédactionnelle (peut appeler le backend)
        # form = st.form("ticket_form")
        # sujet = form.text_input("Sujet", "Signalement dépôt clandestin")
        # ... autres champs ...
        # submitted = form.form_submit_button("Préparer le signalement")
        # if submitted:
        #    # Appeler la fonction backend/logique pour formater
        #    pass

    elif st.session_state.besoin == "question_ia_urba" or st.session_state.besoin == "chat_ia_direct":
        st.write("Posez votre question à notre assistant intelligent :")
        # ICI : Intégrer votre interface de Chat IA (qui appelle le backend avec RAG/LLM/Outils)
        # user_input = st.text_input("Votre question :")
        # if user_input:
        #    # Appeler le backend /chat
        #    response = requests.post("http://localhost:5000/chat", json={"message": user_input}) # Adapter URL
        #    st.write(response.json()["reply"])

    # Gérer les autres 'besoins'...
    # Ne pas oublier le bouton pour recommencer ici aussi