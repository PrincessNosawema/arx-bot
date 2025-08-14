document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector('form');
    const resultsDiv = document.querySelector('.results');
    const searchButton = document.getElementById('search-button');
    const loadingText = document.getElementById('loading-text');
    const chatOutput = document.getElementById('chat-output');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatContainer = document.getElementById('chat-container');
    const chatbotButton = document.getElementById('chatbot-button');
    const closeChatbot = document.getElementById('close-chatbot');

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            if (resultsDiv) {
                resultsDiv.innerHTML = ''; 
            }
            searchButton.style.display = 'none'; 
            loadingText.style.display = 'block'; 
            setTimeout(() => {
                event.target.submit();
            }, 1000);
        });
    }

    const resultItems = document.querySelectorAll('.result-item');
    resultItems.forEach(item => {
        item.addEventListener('mouseover', () => {
            item.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.3)';
        });
        item.addEventListener('mouseout', () => {
            item.style.boxShadow = 'none';
        });
    });


    chatbotButton.addEventListener('click', function () {
        chatContainer.style.display = 'flex';
        chatbotButton.style.display = 'none';
    });

    closeChatbot.addEventListener('click', function () {
        chatContainer.style.display = 'none';
        chatbotButton.style.display = 'block';
    });

    const sendMessage = async () => {
        const prompt = chatInput.value;
        if (!prompt) return;

        chatInput.value = '';
        chatOutput.innerHTML += `<p><strong class="you-text">You:</strong> ${prompt}</p>`;
        chatOutput.innerHTML += `<p><strong class="bot-text">Arx-bot:</strong> Loading response... </p>`;

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt })
            });

            const data = await response.json();
            chatOutput.innerHTML = chatOutput.innerHTML.replace('Loading response...', ` ${data.response}`);

        } catch (error) {
            console.error("Error:", error);
            chatOutput.innerHTML = chatOutput.innerHTML.replace('Loading response...', 'An error occurred.');
        }
    };

    chatSend.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });
});