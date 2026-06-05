import React, { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Loader2, Sparkles, ShoppingBag } from 'lucide-react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import SafeImage from './SafeImage';

const ChatBot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'bot',
      text: "Hi! I'm Suggestify's AI Shopping Assistant. What are you looking for today? 🛍️",
      products: []
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  const handleSend = async (e) => {
    if (e) e.preventDefault();
    if (!input.trim()) return;
    
    const userText = input.trim();
    setInput('');
    
    // Add user message to UI immediately
    const userMsg = { id: Date.now(), role: 'user', text: userText };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);
    
    try {
      // Build history format for backend
      const history = messages.map(m => ({ role: m.role, text: m.text }));
      
      const response = await axios.post('http://localhost:5000/api/chat', {
        message: userText,
        history: history
      });
      
      const botMsg = {
        id: Date.now() + 1,
        role: 'bot',
        text: response.data.response,
        products: response.data.products || []
      };
      
      setMessages(prev => [...prev, botMsg]);
    } catch (error) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'bot',
        text: "Sorry, I'm having trouble connecting to my servers right now. Please try again later.",
        error: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const QuickAction = ({ text, onClick }) => (
    <button 
      onClick={onClick}
      className="text-xs bg-white border-2 border-black px-2 py-1 uppercase font-bold tracking-wider hover:bg-[#ed7844] hover:text-white transition-colors"
    >
      {text}
    </button>
  );

  const ProductCard = ({ product }) => (
    <Link to={`/product/${product.id}`} className="block mt-2">
      <div className="flex border-2 border-black p-2 bg-white hover:bg-gray-50 transition-colors shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]">
        <div className="w-16 h-16 border-2 border-black flex-shrink-0 bg-gray-100 overflow-hidden">
          <SafeImage 
            src={product.image_url} 
            alt={product.name} 
            category={product.category}
            productName={product.name}
            className="w-full h-full object-cover mix-blend-multiply"
          />
        </div>
        <div className="ml-3 flex flex-col justify-center">
          <p className="font-bold text-sm line-clamp-1">{product.name}</p>
          <div className="flex items-center gap-2 mt-1">
            <span className="bg-[#ed7844] text-white px-1.5 py-0.5 text-xs font-bold border border-black">
              ${product.price.toFixed(2)}
            </span>
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">
              ★ {product.rating}
            </span>
          </div>
        </div>
      </div>
    </Link>
  );

  return (
    <>
      {/* Chat Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`fixed bottom-6 right-6 w-14 h-14 bg-[#ed7844] text-white rounded-full flex items-center justify-center border-4 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:translate-y-[-2px] hover:shadow-[4px_6px_0px_0px_rgba(0,0,0,1)] transition-all z-50 ${isOpen ? 'scale-0' : 'scale-100'}`}
      >
        <MessageSquare size={24} />
      </button>

      {/* Chat Window */}
      <div 
        className={`fixed bottom-6 right-6 w-[380px] max-w-[calc(100vw-48px)] h-[550px] max-h-[calc(100vh-48px)] bg-white border-4 border-black shadow-[8px_8px_0px_0px_rgba(0,0,0,1)] flex flex-col z-50 transition-transform origin-bottom-right duration-300 ${isOpen ? 'scale-100 opacity-100' : 'scale-90 opacity-0 pointer-events-none'}`}
      >
        {/* Header */}
        <div className="h-14 border-b-4 border-black bg-[#ed7844] text-white flex items-center justify-between px-4 shrink-0">
          <div className="flex items-center gap-2">
            <Sparkles size={20} />
            <h3 className="font-bold tracking-widest uppercase text-sm mt-1">AI Assistant</h3>
          </div>
          <button 
            onClick={() => setIsOpen(false)}
            className="w-8 h-8 flex items-center justify-center hover:bg-black hover:text-[#ed7844] border-2 border-transparent hover:border-black transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 bg-[#f8f9fa]">
          <div className="flex flex-col space-y-4">
            {messages.map((msg) => (
              <div 
                key={msg.id} 
                className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}
              >
                <div 
                  className={`max-w-[85%] border-2 border-black p-3 text-sm font-medium ${
                    msg.role === 'user' 
                      ? 'bg-black text-white shadow-[2px_2px_0px_0px_rgba(237,120,68,1)]' 
                      : msg.error
                        ? 'bg-red-100 text-red-900 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]'
                        : 'bg-white shadow-[2px_2px_0px_0px_rgba(0,0,0,1)]'
                  }`}
                  style={{ whiteSpace: 'pre-line' }}
                >
                  {msg.text}
                </div>
                
                {/* Render Recommended Products if any */}
                {msg.products && msg.products.length > 0 && (
                  <div className="w-full max-w-[90%] mt-2 flex flex-col gap-2 pl-2">
                    {msg.products.map(p => (
                      <ProductCard key={p.id} product={p} />
                    ))}
                  </div>
                )}
              </div>
            ))}
            
            {isLoading && (
              <div className="flex items-start">
                <div className="bg-white border-2 border-black p-3 shadow-[2px_2px_0px_0px_rgba(0,0,0,1)] flex items-center gap-2">
                  <Loader2 size={16} className="animate-spin text-[#ed7844]" />
                  <span className="text-xs font-bold uppercase tracking-wider text-gray-500">Thinking...</span>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Quick Actions (only show if no messages besides greeting) */}
        {messages.length === 1 && (
          <div className="px-4 py-2 border-t-2 border-black bg-gray-50 flex flex-wrap gap-2">
            <QuickAction text="Recommend Laptops" onClick={() => { setInput("Can you recommend a good laptop?"); handleSend(); }} />
            <QuickAction text="Best Running Shoes" onClick={() => { setInput("What are the best running shoes?"); handleSend(); }} />
            <QuickAction text="Gifts under $50" onClick={() => { setInput("I need a gift under $50."); handleSend(); }} />
          </div>
        )}

        {/* Input */}
        <form 
          onSubmit={handleSend}
          className="h-16 border-t-4 border-black bg-white flex p-2 gap-2 shrink-0"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="ASK ABOUT PRODUCTS..."
            className="flex-1 border-2 border-black px-3 py-2 font-bold text-sm uppercase placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-[#ed7844]"
          />
          <button 
            type="submit"
            disabled={!input.trim() || isLoading}
            className="h-full px-4 bg-[#ed7844] border-2 border-black text-white font-bold flex items-center justify-center hover:bg-black transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={18} />
          </button>
        </form>
      </div>
    </>
  );
};

export default ChatBot;
