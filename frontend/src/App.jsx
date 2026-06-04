import React, { useState, useEffect, useRef } from 'react';
import './index.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef(null);

  const scrollToBottom = () => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    
    const userMessage = input.trim();
    setInput('');
    
    // Add user message to state
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      let answerText = data.answer;
      let sourceUrl = "";
      
      const urlMatch = answerText.match(/Source URL:\s*(https?:\/\/[^\s]+)/i);
      if (urlMatch && urlMatch[1]) {
          sourceUrl = urlMatch[1];
      }
      
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: answerText,
        date: new Date().toISOString().split('T')[0],
        url: sourceUrl
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: "Sorry, I am unable to connect to the server at the moment.", 
        isError: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="h-screen bg-[#111116] text-gray-200 flex flex-col font-sans selection:bg-blue-500/30">
      
      {/* Header */}
      <header className="border-b border-[#2A2B32] py-4 px-6 flex items-center justify-between sticky top-0 bg-[#111116] z-10">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 rounded-lg p-2 text-white flex items-center justify-center">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          </div>
          <div>
            <h1 className="text-xl font-semibold text-white tracking-tight">Tata Mutual Fund FAQ</h1>
            <p className="text-sm text-gray-400">Facts-only assistant for five Groww scheme pages</p>
          </div>
        </div>
        
        <div className="border border-[#4B3B2E] text-[#C48C5B] px-3 py-1.5 rounded-full text-xs font-bold tracking-wider uppercase bg-[#201813]/50">
          Facts-Only. No Investment Advice.
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto" ref={scrollRef}>
        <div className="max-w-3xl mx-auto py-8 px-4 flex flex-col gap-6">
          
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} gap-1 w-full`}>
              
              <span className="text-xs font-bold text-gray-500 uppercase tracking-widest px-1">
                {msg.role === 'user' ? 'You' : 'Assistant'}
              </span>
              
              <div className={`p-4 rounded-xl text-sm leading-relaxed max-w-[85%] ${
                msg.role === 'user' 
                  ? 'bg-[#1E1F29] text-gray-200 border border-[#2A2B32]' 
                  : 'bg-[#1E1F29] text-gray-200 border border-[#2A2B32]'
              }`}>
                {msg.content}
                
                {msg.role === 'assistant' && !msg.isError && (
                  <div className="mt-4 pt-4 border-t border-[#2A2B32]/50 text-xs text-gray-500 font-bold uppercase tracking-wider">
                    Last updated from sources: {msg.date || "2024-05-31"}
                  </div>
                )}
              </div>
              
              {msg.role === 'assistant' && !msg.isError && msg.url && (
                <a href={msg.url} target="_blank" rel="noopener noreferrer" className="mt-1 flex w-fit items-center gap-1.5 bg-[#172520] border border-[#1F3E30] text-[#4ADE80] hover:bg-[#1C3328] transition-colors rounded-full px-3 py-1 text-xs font-semibold cursor-pointer">
                  Groww scheme page
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M7 17l9.2-9.2M17 17V7H7"/></svg>
                </a>
              )}

            </div>
          ))}

          {isLoading && (
            <div className="flex flex-col items-start gap-1 w-full animate-pulse">
              <span className="text-xs font-bold text-gray-500 uppercase tracking-widest px-1">Assistant</span>
              <div className="p-4 rounded-xl bg-[#1E1F29] border border-[#2A2B32] text-gray-400 text-sm">
                Thinking...
              </div>
            </div>
          )}

        </div>
      </main>

      {/* Input Area */}
      <footer className="p-6 bg-[#111116] border-t border-[#2A2B32]">
        <div className="max-w-3xl mx-auto flex flex-col gap-2">
          <div className="flex items-center gap-3">
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              placeholder="Ask a question..."
              className="flex-1 bg-[#1A1C23] border border-[#2A2B32] rounded-xl px-4 py-3.5 text-gray-200 focus:outline-none focus:border-[#4B5563] transition-colors disabled:opacity-50"
            />
            <button 
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="bg-[#3B82F6] hover:bg-[#2563EB] disabled:bg-blue-900 disabled:text-blue-400 text-white font-medium px-6 py-3.5 rounded-xl transition-colors"
            >
              Send
            </button>
          </div>
          <p className="text-xs text-gray-500">
            Do not enter PAN, Aadhaar, bank account numbers, OTP, email, or phone numbers.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
