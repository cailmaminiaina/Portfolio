from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import json
from datetime import datetime
import requests

app = Flask(__name__)


@app.route('/')
def index():
    projects = [
        {
            'title': 'Site Web en L1',
            'description': 'Un site web vitrine de tourisme pour notre agence de voyage en utilisant Python avec le framework Django. <br>(Décembre 2022)',
            'image': 'project1.png',
            'url': 'https://laicriritravel.onrender.com'
        },
        {
            'title': 'ChatBot 2.0',
            'description': 'Un chatbot d´Intélligence Artificiel sur messenger programmé en Python. <br>(Mars 2023)',
            'image': 'project2.png',
            'url': 'https://facebook.com/share/19VRFDWHMt'
        },
        {
            'title': 'IA pour le service client',
            'description': 'Un chatbot d´Intelligence Artificiel sur messenger pour les entreprises pour automatiser le service client. <br>(Mémoire de Licence - Novembre 2024)',
            'image': 'project3.jpg',
            'url': 'https://github.com/cailmaminiaina/AI-ChatBot-for-Companies'
        },
        {
            'title': 'Portfolio',
            'description': 'Mon portfolio en utilisant Python avec le framework Flask en intégrant une IA qui m´imite. <br>(Décembre 2024)',
            'image': 'project4.png',
            'url': '/'
        }
    ]
    return render_template('index.html', projects=projects)

@app.route('/download-cv')
def download_cv():
    return send_from_directory(
        os.path.join(app.root_path, 'static/images'),
        'Mon CV.pdf',
        as_attachment=True
    )

# Fonction pour générer un identifiant d'utilisateur basé sur son IP
def generate_user_id():
    return f"user_{request.remote_addr.replace('.', '_')}"

# Fonction pour sauvegarder les messages dans un fichier JSON
def save_chat_log(user_id, user_message, bot_response):
    file_name = f"{user_id}.json"  # Fichier de log pour chaque utilisateur
    file_path = os.path.join("chat_logs", file_name)

    # Assurez-vous que le dossier existe
    if not os.path.exists("chat_logs"):
        os.makedirs("chat_logs")

    # Structure du message avec horodatage
    new_message = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_message,
        "bot": bot_response
    }

    # Charger l'historique existant ou initialiser une nouvelle structure
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            chat_history = json.load(file)
    else:
        chat_history = {"messages": []}

    # Ajouter le nouveau message
    chat_history["messages"].append(new_message)

    # Sauvegarder le fichier JSON mis à jour
    with open(file_path, "w") as file:
        json.dump(chat_history, file, indent=4)

# Fonction pour récupérer les messages enregistrés dans le format requis par l'API
def load_chat_history(user_id):
    file_name = f"{user_id}.json"
    file_path = os.path.join("chat_logs", file_name)

    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            chat_history = json.load(file)
            formatted_messages = []
            
            for message in chat_history.get("messages", []):
                formatted_messages.append({"role": "user", "content": message["user"]})
                formatted_messages.append({"role": "assistant", "content": message["bot"]})
            
            return formatted_messages
    return []  # Retourne une liste vide si aucun historique n'existe

# Route pour gérer les conversations
@app.route('/chat', methods=['POST'])
def chat():
    base_url = "https://api.pawan.krd/v1/"
    api_key = "Bearer pk-WFstxMpbfTWDTfcbeaMrrLHcAERcaSAwibZBeALxWpqzKRLJ"

    # Vérifier si la requête contient un JSON valide
    if not request.is_json:
        return jsonify({'error': 'Invalid request format, expected JSON'}), 400

    data = request.json
    user_message = data.get('message', '')

    # Vérifier que le message n'est pas vide
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    user_id = generate_user_id()

    # Charger l'historique des messages
    chat_history = load_chat_history(user_id)

    # Ajouter le message actuel au payload
    chat_history.append({"role": "user", "content": user_message})

    # Construire les données pour l'API
    payload = {
        "model": "pai-001-light-rp",
        "temperature": 0.9,
        "messages": [
            {"role": "system", "content": "Tu es SOLOHERIMALALA Maminiaina Laïc, 21 ans (née le 19/03/03), originaire de Miandrivazo, habites à Antananarivo, étudiant en quatrième année en informatique, passionné par la programmation, l'intelligence artificielle, la cybersécurité et les solutions numériques. Grâce à une formation rigoureuse et des expériences concrètes, tu as développé des compétences solides en création de projets basés sur l'IA, en développement d'applications web et en automatisation, principalement avec Python. Doté d'un esprit analytique et créatif, tu t'intéresses également au marketing digital, notamment à la gestion stratégique des réseaux sociaux et à la création de contenus engageants et à l'entrepreunariat. Ton ambition est de contribuer activement à des projets innovants, de relever des défis techniques ambitieux et d'explorer de nouvelles technologies pour apporter des solutions efficaces et intuitives qui répondent aux besoins des utilisateurs. Tu réponds de manière claire mais aussi de manière un jeune impoli et cool."}
        ] + chat_history  # Fusionner l'historique avec le nouveau message
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': api_key,
    }

    try:
        # Appel à l'API
        response = requests.post(f"{base_url}chat/completions", json=payload, headers=headers)

        # Vérifiez si l'API a répondu correctement
        if response.status_code != 200:
            return jsonify({'error': f"API Error: {response.status_code}, {response.text}"}), 500

        response_data = response.json()

        # Extraire la réponse du bot
        bot_response = response_data['choices'][0]['message']['content']

        # Sauvegarder la conversation
        save_chat_log(user_id, user_message, bot_response)

        # Retourner la réponse
        return jsonify({'user_message': user_message, 'bot_response': bot_response})

    except requests.exceptions.RequestException as e:
        print(f"Erreur de requête : {e}")
        return jsonify({'error': 'An error occurred during processing'}), 500

if __name__ == "__main__":
    app.run(debug=True)
