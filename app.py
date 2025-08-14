import os
import subprocess
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, abort, jsonify
from features.arxiv_client import search_arxiv
from features.chatbot import chat_bot

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        query = request.form.get('query', '').strip()
        num_results = int(request.form.get('num_results', 5))
        if not query:
            return render_template('index.html', error="Please enter a valid query.")
        print(f"Received query: {query}")
        print(f"Number of results requested: {num_results}\n")

        top_documents = search_arxiv(query, num_results)
        return render_template('result.html', query=query, results=top_documents)
    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template('index.html', error="An error occurred. Please try again.")

@app.route('/chat', methods=['POST'])
def chat_route():
    data = request.get_json()
    prompt = data.get('prompt')
    return chat_bot(prompt)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':
    try:
        result = subprocess.run(
            ['python', 'desktop_ui.py'],
            capture_output=True,
            text=True,
            check=True
        )
        print("desktop_ui.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        pass

    Timer(1,open_browser).start()
    app.run(debug=False)