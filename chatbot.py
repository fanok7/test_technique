"""
Programme principal et chatbot RAG - Première page
"""

import streamlit as st
import os
from utils.documents_manager import get_vectordb, vectorize_all_documents
from utils.rag_chain import load_rag_chain
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

vectordb = get_vectordb()                   # Charge ou crée la base vectorielle
vectorize_all_documents(vectordb)           # Vectorise automatiquement les nouveaux documents

# Titre de la page
st.title("Collaborateur IA juridique interne")

# Historique du chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("Poser des **questions** au chatbot basé sur vos documents internes")

# Création de la chaîne RAG
chain = load_rag_chain(db_path="data/vectordb")
# Entrée utilisateur
question = st.text_input("Posez votre question :")

# Réponse au prompt
if question:
    with st.spinner("L'IA réfléchit..."):
        response = chain.invoke(question)  # Passe la question dans un dict
    st.session_state.chat_history.append((question, response))

# Afficher l'historique
for q, r in st.session_state.chat_history:
    st.markdown(f"**Vous :** {q}")
    st.markdown(f"**Assistant IA :** {r}")

# Bouton pour réinitialiser l'historique de conversation
if st.button("Effacer l'historique de conversation"):
    st.session_state.chat_history = []
    st.experimental_rerun()

