"""
Programme principal et chatbot RAG - Première page
"""

import streamlit as st
import os
from utils.documents_manager import vectorize_all_documents, reset_vectordb
from utils.rag_chain import load_rag_chain
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page 
st.set_page_config(
    page_title="Collaborateur IA Juridique",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# On détecte la première exécution 
if "initialized" not in st.session_state:
    reset_vectordb()     # 💥 Supprime complètement l'ancienne base
    # Vectorise automatiquement les documents actuels
    vectorize_all_documents() 
    st.session_state.initialized = True
   
# Titre de la page
st.title("💼 Collaborateur Juridique RAG")
st.markdown("Poser des questions au chatbot basé sur les documents internes")

# Initialisation de l'historique
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Charger la chaîne RAG
chain = load_rag_chain()

# Affichage de l'historique
for msg in st.session_state.chat_history:
    role, content = msg["role"], msg["content"]
    st.chat_message(role).write(content)

# Entrée utilisateur
if prompt := st.chat_input("Posez votre question..."):
    # Ajouter message utilisateur à l'historique
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # Générer la réponse
    with st.spinner("L'assistant cherche..."):
        response = chain.invoke(prompt)
    # Ajouter réponse à l'historique
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

# Bouton reset
if st.button("Effacer l'historique de conversation", type="secondary"):
    st.session_state.chat_history = []
    st.rerun()