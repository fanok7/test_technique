
# Import des modules nécessaires pour LangChain, embeddings et gestion des variables d'environnement
from langchain_community.vectorstores import Chroma           # Base vectorielle pour stocker et rechercher les embeddings
from langchain_openai import ChatOpenAI                        # Wrapper LangChain pour utiliser GPT
from langchain_core.runnables import RunnablePassthrough       # Passe la donnée telle quelle
from langchain_core.output_parsers import StrOutputParser      # Transforme la sortie GPT en texte simple
from langchain_core.prompts.chat import ChatPromptTemplate     # Pour créer des prompts dynamiques
from langchain_openai import OpenAIEmbeddings                  # Pour générer les embeddings avec OpenAI
from dotenv import load_dotenv

# Chargement des variables d'environnement (ex : OPENAI_API_KEY)
load_dotenv()

def load_rag_chain(db_path="data/vectordb"):
    # Création du modèle d'embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    # Création du retriever Chroma
    # Va chercher les chunks les plus pertinents depuis la base vectorielle
    # k=4 signifie qu'on récupère les 4 meilleurs chunks pour chaque question
    retriever = Chroma(persist_directory=db_path,embedding_function=embeddings).as_retriever(search_kwargs={"k": 4})
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