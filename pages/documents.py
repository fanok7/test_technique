"""
Page pour la gestion des documents juridiques - Deuxième Page
"""

import os
import streamlit as st
from utils.documents_manager import delete_documents, upload_documents, get_vectordb  # import de get_vectordb
import random

# Dossier où sont stockés les documents
DOC_DIR = "data/documents"

# Configuration de la page
st.set_page_config(page_title="Gestion des Documents", layout="wide")

# Titre et description de la page
st.title("📁 Gestionnaire de documents")
st.markdown("Uploader, lister et supprimer des documents dans la base de données interne")

# Charger ou créer la base vectorielle
vectordb = get_vectordb()

# Initialiser la liste des documents dans la session si ce n'est pas déjà fait
if "docs" not in st.session_state:
    st.session_state.docs = os.listdir(DOC_DIR)

# Bouton-drag pour upload des documents
st.subheader("📤 Uploader des documents")
# Initialisation du compteur pour uploader
if "uploader_counter" not in st.session_state:
    st.session_state.uploader_counter = 0
# Clé dynamique pour le file_uploader
uploader_key = f"uploader_{st.session_state.uploader_counter}"
# Uploader de documents
uploaded_files = st.file_uploader("Uploader (.txt, .csv, .html)", type=["txt", "csv", "html"],accept_multiple_files=True,key=uploader_key)
if uploaded_files:
    files = []
    for f in uploaded_files:
        files.append(f)
    if files:
        upload_documents(files, vectordb)
        st.session_state.docs = os.listdir(DOC_DIR)
        # Incrémenter le compteur pour générer une nouvelle clé permet le reset du uploader
        st.session_state.uploader_counter += 1
        st.rerun()  # pour reset le file_uploader et actualiser la liste

# Liste de documents
st.subheader("📚 Liste des documents existants")
if st.session_state.docs:
    for doc in st.session_state.docs:
        # Choisir une icône selon le type de fichier
        ext = os.path.splitext(doc)[1].lower()
        icon = "📄"
        if ext == ".csv":
            icon = "📊"
        elif ext == ".html":
            icon = "🌐"
        # Créer deux colonnes : une pour le nom, une pour le bouton
        col1, col2 = st.columns([8, 1])
        with col1:
            st.write(f"{icon} {doc}")
        with col2:
            if st.button("🗑️", key=f"del_{doc}", help="Supprimer ce document"):
                # Supprimer le document de la base et du disque
                delete_documents([doc], vectordb)
                # Mettre à jour la liste
                st.session_state.docs = os.listdir(DOC_DIR)
                # Rafraîchir la page
                st.rerun()
else:
    # Si aucun document n'existe
    st.info("Aucun document pour le moment.")

# Boutons pour supprimer tous les fichiers de la base de données
st.markdown("---")
if st.button("🗑️ Supprimer tous les documents", key="delete_all"):
    # Supprimer tous les fichiers un par un
    for doc in st.session_state.docs:
        delete_documents([doc], vectordb)
    # Mettre à jour la liste
    st.session_state.docs = os.listdir(DOC_DIR)
    # Rafraîchir la page
    st.rerun()