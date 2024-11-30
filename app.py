from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Telegram Bot Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'

def send_to_telegram(message):
    """
    Send message to Telegram channel
    """
    endpoint = f'{BASE_URL}/sendMessage'
    payload = {
        'chat_id': CHANNEL_ID,
        'text': message,
        'parse_mode': 'HTML'  # Supports HTML formatting
    }
    
    response = requests.post(endpoint, json=payload)
    return response.json()

@app.route('/webhook/telegram', methods=['POST'])
def webhook():
    """
    Webhook endpoint to receive messages and forward them to Telegram
    Expected JSON format: {"message": "Your message here"}
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Invalid payload'}), 400
        
        message = data['message']
        result = send_to_telegram(message)
        
        if result.get('ok'):
            return jsonify({'status': 'success', 'message': 'Message sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send message', 'details': result}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
