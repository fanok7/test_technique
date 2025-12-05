# Collaborateur Juridique RAG

Cette application est une preuve de concept d’assistant juridique interne, conçue pour exploiter des documents provenant d’un cabinet d’avocats.
Elle combine une interface de chat alimentée par un modèle GPT et un système de gestion de documents vectorisés, permettant de fournir des réponses contextualisées directement issues des documents internes.

L’application utilise Streamlit pour l’interface web, Chroma pour la base vectorielle, et LangChain pour la mise en place d’une chaîne RAG

Installation :

1. Cloner le dépôt : `git clone https://github.com/fanok7/test_technique` puis `cd test_technique`
2. Créer un environnement Python : `python -m venv venv` puis `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac)
3. Installer les dépendances : `pip install -r requirements.txt`
4. Créer un fichier .env à la racine du projet et ajouter : `OPENAI_API_KEY=sk-votre_cle_openai`
5. Lancer l'application : `streamlit run chatbot.py`

