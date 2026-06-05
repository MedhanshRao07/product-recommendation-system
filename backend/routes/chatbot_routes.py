from flask import Blueprint, request, jsonify
from ..services.chatbot_service import chatbot_service
import logging

logger = logging.getLogger('suggestify.chatbot_routes')

chat_bp = Blueprint('chat_bp', __name__)

@chat_bp.route('', methods=['POST'])
def chat():
    """Main chat endpoint. Expects { "message": "string", "history": [...] }"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        user_message = data.get('message')
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
            
        conversation_history = data.get('history', [])
        
        # Process via Chatbot Service
        result = chatbot_service.chat(user_message, conversation_history)
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in chat route: {e}")
        return jsonify({"error": "Internal server error"}), 500
