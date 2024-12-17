document.addEventListener("DOMContentLoaded", () => {
    const loader = document.querySelector(".loader");
    if (loader) {
        setTimeout(() => {
            loader.classList.add("hidden");
            document.body.style.overflow = "visible";
        }, 2000);
    }
});

// Fonction pour formater la date et l'heure
function updateDateTime() {
    const now = new Date();
    
    // Format de la date et de l'heure en français
    const optionsDate = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    };
    
    const optionsTime = {
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
        hour12: false
    };

    // Formater la date et l'heure
    const dateString = now.toLocaleDateString('fr-FR', optionsDate); // Date formatée
    const timeString = now.toLocaleTimeString('fr-FR', optionsTime); // Heure formatée
    
    // Ajouter la date et l'heure avec des balises <span> pour styliser différemment
    const dateTimeElement = document.getElementById('date-time');
    dateTimeElement.innerHTML = `
        <span class="time">${timeString}</span>
        <span class="date">${dateString}</span>
    `;

    // Appliquer l'animation en ajoutant la classe 'show' une fois la date/heure mise à jour
    dateTimeElement.classList.add('show');
}

// Mettre à jour toutes les secondes
setInterval(updateDateTime, 1000);

// Mettre à jour la date et l'heure immédiatement lors du chargement
updateDateTime();


document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        } else {
            console.warn(`Aucune cible trouvée pour ${this.getAttribute('href')}`);
        }
    });
});

// Fonction pour basculer l'état de la boîte de chat
function toggleChatBox(event) {
    console.log('toggleChatBox called'); // Vérification
    event.stopPropagation(); // Empêche la propagation pour éviter la fermeture immédiate
    const chatBox = document.getElementById('chat-box');

    if (chatBox) {
        chatBox.classList.toggle('open'); // Ouvre/ferme la boîte
    }
}

// Fermer la boîte de chat via le bouton de fermeture
document.getElementById('chat-close-button').addEventListener('click', function (event) {
    event.stopPropagation(); // Empêche la fermeture immédiate
    const chatBox = document.getElementById('chat-box');
    chatBox.classList.remove('open');
});

// Fermer la boîte de chat en cliquant en dehors
document.addEventListener('click', function (event) {
    const chatBox = document.getElementById('chat-box');
    const chatIcon = document.getElementById('chat-icon');

    // Vérifie si le clic est en dehors de la boîte et de l'icône
    if (!chatBox.contains(event.target) && event.target !== chatIcon) {
        chatBox.classList.remove('open');
    }
});

// Ajouter un événement pour l'icône afin d'ouvrir la boîte de chat
document.getElementById('chat-icon').addEventListener('click', toggleChatBox);


// Fonction pour envoyer un message
function sendMessage() {
    let inputField = document.getElementById('chat-input');
    let userMessage = inputField.value.trim();
    if (userMessage === '') return; // Ignore les messages vides
    inputField.value = '';

    let chatContent = document.getElementById('chat-content');

    // Ajouter le message de l'utilisateur
    chatContent.innerHTML += `
        <div class="user-message">${userMessage}</div>
    `;
    chatContent.scrollTop = chatContent.scrollHeight; // Scroll vers le bas

    // Définir une durée minimale pour l'affichage de l'indicateur
    const minimumTypingTime = 3000; // 3 secondes
    let typingIndicator; // Variable pour l'indicateur de saisie

    // Attendre 3 secondes avant d'afficher l'indicateur
    setTimeout(() => {
        typingIndicator = document.createElement('div');
        typingIndicator.id = 'typing-indicator';
        typingIndicator.style.fontStyle = 'italic';
        typingIndicator.style.color = '#888';
        typingIndicator.innerText = "en train d'écrire...";
        chatContent.appendChild(typingIndicator);
        chatContent.scrollTop = chatContent.scrollHeight; // Scroll vers le bas
    }, 3000);

    // Capturer le moment où l'indicateur aurait été affiché
    let typingStartTime = Date.now() + 3000;

    // Appeler l'API Flask pour obtenir la réponse du bot
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        // Calculer le temps écoulé après l'affichage de l'indicateur
        let elapsedTime = Date.now() - typingStartTime;

        // Attendre que les 3 secondes minimales soient écoulées avant de supprimer l'indicateur
        setTimeout(() => {
            if (typingIndicator) typingIndicator.remove(); // Supprimer l'indicateur

            if (data.bot_response) {
                // Afficher la réponse du bot
                chatContent.innerHTML += `
                <div class="bot-message">
                    <img src="/static/images/profile.png" alt="bot" class="bot-img">
                    <div class="bot-text">${data.bot_response}</div>
                </div>`;
            } else if (data.error) {
                // Afficher les erreurs éventuelles
                chatContent.innerHTML += `
                <div style="text-align: left; margin-bottom: 10px; color: red;">
                    Erreur : ${data.error}
                </div>`;
            }

            chatContent.scrollTop = chatContent.scrollHeight; // Scroll vers le bas
        }, Math.max(0, minimumTypingTime - elapsedTime)); // Attendre le temps restant si nécessaire
    })
    .catch(error => {
        console.error('Erreur API:', error);

        // Supprimer l'indicateur après le délai minimal, même en cas d'erreur
        setTimeout(() => {
            if (typingIndicator) typingIndicator.remove();

            chatContent.innerHTML += `
            <div style="text-align: left; margin-bottom: 10px; color: red;">
                Erreur : Impossible de contacter le serveur.
            </div>`;
            chatContent.scrollTop = chatContent.scrollHeight; // Scroll vers le bas
        }, minimumTypingTime);
    });
}


// Événement pour la touche "Entrée"
document.getElementById('chat-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Événement pour le bouton d'envoi
document.getElementById('chat-send-button').addEventListener('click', sendMessage);


AOS.init({
    startEvent: 'load',
    duration: 1000, 
    easing: 'ease-out', 
    once: false 
});
