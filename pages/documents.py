import os
import streamlit as st
from utils.documents_manager import delete_documents, upload_documents, get_vectordb  # import de get_vectordb
import random

# Dossiers
DOC_DIR = "data/documents"
DB_PATH = "data/vectordb"
# Générer une clé unique à chaque rerun pour "vider" le file_uploader
uploader_key = f"file_uploader_{random.randint(0, 999999)}"
# Titre de la page
st.title("Gestion des documents juridiques")
st.markdown("**gérer** vos fichiers internes (upload et suppression)")

# Charger la base vectorielle
vectordb = get_vectordb()

# Upload d’un document
uploaded = st.file_uploader("Uploader un fichier (.txt, .csv, .html)", type=["txt","csv","html"], accept_multiple_files=True)
if uploaded:
    upload_documents(uploaded, vectordb)# passer vectordb ici

# Liste des documents existants
st.subheader("Documents existants")
docs = os.listdir(DOC_DIR)
st.write(docs if docs else "Aucun document pour le moment.")

# Suppression de documents
st.subheader("Supprimer des documents")
to_delete = st.multiselect("Sélectionnez les documents à supprimer", options=docs)
if st.button("Supprimer la sélection") and to_delete:
    delete_documents(to_delete, vectordb)  # passer vectordb ici
    st.success(f"Documents supprimés : {', '.join(to_delete)}")