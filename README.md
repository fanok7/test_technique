# Collaborateur IA Juridique Interne

Cette application est un test d'un assistant juridique interne basé sur des documents issue d0un cabinet d'avocat. Elle combine une interface de chat alimentée par un modèle GPT et une gestion de documents vectorisés pour permettre des réponses contextuelles issues de documents donnés. L'application utilise Streamlit pour l'interface web, Chroma pour la base vectorielle, et LangChain pour la chaîne RAG (Retrieval-Augmented Generation).

Installation :

1. Cloner le dépôt : `git clone <votre-repo>` puis `cd <nom-du-repo>`
2. Créer un environnement Python : `python -m venv venv` puis `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux/Mac)
3. Installer les dépendances : `pip install -r requirements.txt`
4. Configurer les variables d'environnement dans un fichier .env : par exemple `OPENAI_API_KEY=sk-...`
5. Lancer l'application : `streamlit run app_chat.py` pour le chat ou `streamlit run app_documents.py` pour la gestion des documents

Utilisation :

- Chatbot : tapez votre question dans le champ "Posez votre question". L'assistant répond selon les documents existants. L'historique de la session est affiché. Bouton disponible pour effacer l'historique.
- Gestion des documents : uploader de nouveaux fichiers (.txt, .csv, .html), visualiser les documents existants, supprimer des fichiers avec mise à jour automatique de la base vectorielle.
- Mise à jour manuelle : si des fichiers sont ajoutés directement dans `data/documents` sans passer par l'interface Streamlit, exécutez le code suivant pour vectoriser automatiquement les nouveaux documents :

