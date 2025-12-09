"""
Gestion des documents et de la base vectorielle pour le chatbot juridique
"""

import os
import logging
import pandas as pd
import re
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Dossiers
DOC_DIR = "data/documents"
DB_DIR = "data/vectordb"

# Supprime HTML et normalise les espaces
def clean_text(raw_text: str) -> str:
    clean = BeautifulSoup(raw_text, "html.parser").get_text()
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()

# Lit un fichier txt, csv ou html et renvoie le texte nettoyé
def load_and_preprocess(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(file_path, dtype=str).fillna("")
        return " ".join(df.apply(lambda row: " ".join(row), axis=1))
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            raw = f.read()
        if ext in [".html", ".htm"]:
            return clean_text(raw)
        return raw.strip()

# Charger ou créer la base vectorielle
def get_vectordb():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    os.makedirs(DB_DIR, exist_ok=True)
    return Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

# Vectorise tous les documents du dossier DOC_DIR qui ne sont pas encore indexés
def vectorize_all_documents(vectordb):
    os.makedirs(DOC_DIR, exist_ok=True)
    # Fichiers déjà indexés
    existing_docs = {meta['source'] for meta in vectordb._collection.get()['metadatas'] if 'source' in meta}
    docs_to_add = []
    for file_name in os.listdir(DOC_DIR):
        if file_name in existing_docs:
            continue
        path = os.path.join(DOC_DIR, file_name)
        raw = load_and_preprocess(path)
        if not raw.strip():
            logging.warning(f"Document {file_name} vide, ignoré")
            continue
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        file_docs = splitter.create_documents([raw])
        for doc in file_docs:
            doc.metadata['source'] = file_name
        docs_to_add.extend(file_docs)
    if docs_to_add:
        vectordb.add_documents(docs_to_add)
        vectordb.persist()
        logging.info(f"{len(docs_to_add)} documents vectorisés en batch")
    else:
        logging.info("Aucun nouveau document à vectoriser")

# Upload d’un fichier 
def upload_documents(uploaded_files, vectordb):
    os.makedirs(DOC_DIR, exist_ok=True)
    for uploaded_file in uploaded_files:
        file_path = os.path.join(DOC_DIR, uploaded_file.name)
        if os.path.exists(file_path):
            logging.warning(f"Fichier {uploaded_file.name} déjà présent, ignoré")
            continue
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        logging.info(f"Fichier {uploaded_file.name} ajouté au dossier")

# Suppression d’un ou plusieurs fichier
def delete_documents(filenames, vectordb):
    for file_name in filenames:
        path = os.path.join(DOC_DIR, file_name)
        if os.path.exists(path):
            os.remove(path)
            logging.info(f"Fichier {file_name} supprimé du dossier")
