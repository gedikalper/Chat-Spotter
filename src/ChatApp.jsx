// ChatApp.jsx
import { useEffect, useState, useRef } from "react";

export default function ChatApp() {
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:6789");

    ws.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    ws.onopen = () => {
      console.log("WebSocket bağlantısı kuruldu.");
    };

    ws.onerror = (err) => {
      console.error("WebSocket hatası:", err);
    };

    ws.onclose = () => {
      console.warn("WebSocket bağlantısı kapandı.");
    };

    return () => {
      ws.close();
    };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="bg-black text-white min-h-screen p-6">
      <h1 className="text-2xl text-green-400 mb-4">Mustfyman Chat Viewer</h1>
      <div className="bg-zinc-900 p-4 rounded-lg max-h-[80vh] overflow-y-auto space-y-2">
        {messages.map((msg, index) => (
          <div key={index} className="bg-zinc-800 p-2 rounded">
            {msg}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
