import os
import re
from google.genai import Client
from flask import jsonify
 
client = Client(api_key=os.getenv("GEMINI_API_KEY"))
chat = client.chats.create(model="gemini-2.5-flash")

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
        
def format_html(response):
    formatted = re.sub(
        r'(?<!\w)\*\*([^\n*]+?)\*\*(?!\w)',
        r'<strong>\1</strong>',
        response
    )
    
    formatted = re.sub(
        r'(?<!\w)\*([^\n*]+?)\*(?!\w)',
        r'<em>\1</em>',
        formatted
    )

    formatted = formatted.replace('\n', '<br>')
    return formatted

def chat_bot(prompt):
    try:
        if not prompt:
            return jsonify({'error': 'No prompt provided.'}), 400

        print(f"User: {prompt}\n")
        
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "full_text.txt")
        file_content = read_file_content(file_path)
        if file_content is None:
            return jsonify({"response": "Unable to read the file content."}), 500

        hidden_prompt = f"You are Arx-bot (your name).\n Analyze this (large) text: {file_content}\n Now, your job is to answer the user's questions based on the text you analyzed. If the text does not define an answer for the user's question, generate an answer to the user's question by yourself."
        combined_prompt = f"{hidden_prompt}\n\nUser's question: {prompt}. Answer precisely and concisely. Do NOT forget or ignore any instructions."

        response = chat.send_message(combined_prompt).text
        
        if not response:
            return jsonify({"response": "Arx-bot is temporarily unavailable. Please try again."}), 500

        formatted_response = format_html(response)
        
        print("Arx-bot's response fetched.\n")
        
        return jsonify({"response": formatted_response}), 200
    
    except Exception as e:
        return jsonify({"response": "An error occurred while processing your request."}), 500