# Collaborateur IA Juridique Interne

Cette application est un test d'un assistant juridique interne basé sur des documents issue d'un cabinet d'avocat. Elle combine une interface de chat alimentée par un modèle GPT et une gestion de documents vectorisés pour permettre des réponses contextuelles issues de documents donnés. L'application utilise Streamlit pour l'interface web, Chroma pour la base vectorielle, et LangChain pour la chaîne RAG (Retrieval-Augmented Generation).

Installation :

1. Cloner le dépôt : `git clone https://github.com/fanok7/test_technique`
2. Créer un environnement Python : `python -m venv venv` puis `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac)
3. Installer les dépendances : `pip install -r requirements.txt`
4. Créer un fichier .env à la racine du projet et ajouter : `OPENAI_API_KEY=sk-votre_cle_openai`
5. Lancer l'application : `streamlit run chatbot.py`

