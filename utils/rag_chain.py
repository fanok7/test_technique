"""
Création de la chaîne RAG (Retrieval-Augmented Generation) pour l'assistant juridique
"""

from langchain_community.vectorstores import Chroma          
from langchain_openai import ChatOpenAI                       
from langchain_core.runnables import RunnablePassthrough       
from langchain_core.output_parsers import StrOutputParser     
from langchain_core.prompts.chat import ChatPromptTemplate     
from langchain_openai import OpenAIEmbeddings                  
from dotenv import load_dotenv
from utils.documents_manager import get_vectordb

# Chargement des variables d'environnement
load_dotenv()

def load_rag_chain():
    # Création du modèle d'embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    # Création du retriever Chroma
    vectordb = get_vectordb()
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    # Définition du template de prompt pour le LLM
    template = """Tu es un assistant juridique. Répond à la QUESTION uniquement selon le CONTEXTE.
    Si l'information n'est pas présente, dis : "information non trouvée".

    CONTEXTE:
    {context}

    QUESTION:
    {question}
    """

    # Création d’un objet prompt dynamique LangChain
    prompt = ChatPromptTemplate.from_template(template)
    # Initialisation du LLM (chatGPT)
    llm = ChatOpenAI(model="gpt-5.1", temperature=0)
    # Construction de la chaîne RAG
    chain = (
        {"context": retriever, "question": RunnablePassthrough()} # Le retriever fournit les chunks pertinents
        | prompt   # Injecte context + question dans le template de base
        | llm     # Envoie le prompt au modèle GPT
        | StrOutputParser()  # Transforme la sortie en texte simple
    )

    return chain