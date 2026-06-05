import os
import json
import logging
from google import genai
from google.genai import types
from ..database.db_connection import get_connection

logger = logging.getLogger('suggestify.chatbot')
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[%(name)s] %(message)s'))
    logger.addHandler(handler)

class ChatbotService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.is_configured = False
        self.client = None
        
        # Explicit initialization logging
        if self.api_key:
            masked = self.api_key[:4] + "*" * 10 + self.api_key[-4:] if len(self.api_key) > 8 else "****"
            logger.info(f"Detected GEMINI_API_KEY: {masked}")
        else:
            logger.warning("GEMINI_API_KEY not found in environment. Chatbot will remain offline.")
            return
            
        try:
            self.client = genai.Client(api_key=self.api_key)
            
            # Simple test request to verify API connection
            logger.info("Testing Gemini API connection...")
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents='Hello'
            )
            
            if response.text:
                self.is_configured = True
                logger.info("Gemini AI Chatbot configured and connected successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {e}")
            self.is_configured = False

    def _get_relevant_products(self, queries):
        """Search the database for products matching the generated queries."""
        if not queries:
            return []
            
        products = []
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            
            for query in queries:
                search_term = f"%{query}%"
                cursor.execute("""
                    SELECT id, name, price, image_url, category, brand, rating, price_range 
                    FROM products 
                    WHERE name LIKE %s OR category LIKE %s OR tags LIKE %s
                    ORDER BY rating DESC 
                    LIMIT 3
                """, (search_term, search_term, search_term))
                
                results = cursor.fetchall()
                products.extend(results)
                
            cursor.close()
            conn.close()
            
            seen_ids = set()
            unique_products = []
            for p in products:
                if p['id'] not in seen_ids:
                    seen_ids.add(p['id'])
                    unique_products.append(p)
                    
            return unique_products[:4]
        except Exception as e:
            logger.error(f"Error fetching products for chat: {e}")
            return []

    def chat(self, user_message, conversation_history=None):
        if not self.is_configured:
            return {
                "response": "I'm sorry, my AI brain is currently offline. Please set the GEMINI_API_KEY environment variable to activate me!",
                "products": [],
                "error": True
            }

        if conversation_history is None:
            conversation_history = []

        try:
            # Build conversation context
            contents = []
            for msg in conversation_history[-6:]:
                role = "user" if msg.get('role') == 'user' else "model"
                contents.append(
                    types.Content(role=role, parts=[types.Part.from_text(text=msg.get('text', ''))])
                )
                
            # Add current user message
            contents.append(
                types.Content(role="user", parts=[types.Part.from_text(text=user_message)])
            )
            
            config = types.GenerateContentConfig(
                system_instruction="""You are the AI Shopping Assistant for Suggestify, an e-commerce platform. 
                Your job is to help users find products, answer shopping questions, compare items, and give recommendations.
                
                RULES:
                1. ONLY answer questions related to shopping, products, retail, style, tech specs, and buying advice.
                2. If a user asks a non-shopping question (e.g., math, coding, history), politely decline and remind them you are a shopping assistant.
                3. If you recommend products, you MUST output a special JSON block at the END of your response containing product queries.
                   Format: ```json\n{"queries": ["search term 1", "search term 2"]}\n```
                4. Keep your responses concise, friendly, and structured. Use bullet points for comparisons.
                5. Be energetic and helpful!"""
            )
            
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents,
                config=config
            )
            
            text_response = response.text
            products = []
            
            if "```json" in text_response:
                try:
                    start_idx = text_response.find("```json") + 7
                    end_idx = text_response.find("```", start_idx)
                    json_str = text_response[start_idx:end_idx].strip()
                    
                    query_data = json.loads(json_str)
                    queries = query_data.get('queries', [])
                    
                    if queries:
                        products = self._get_relevant_products(queries)
                    
                    text_response = text_response[:text_response.find("```json")].strip()
                    
                except Exception as e:
                    logger.warning(f"Failed to parse JSON from AI response: {e}")
            
            return {
                "response": text_response,
                "products": products,
                "error": False
            }
            
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return {
                "response": "I encountered an error trying to process your request. Please try again.",
                "products": [],
                "error": True
            }

chatbot_service = ChatbotService()
