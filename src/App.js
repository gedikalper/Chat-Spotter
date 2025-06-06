import React, { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");

  function addMustfymanMessage(text) {
    if (text.trim() === "") return;
    setMessages(prev => [...prev, { username: "mustfyman", text }]);
    setInputText(""); // Mesaj gönderilince input temizlensin
  }

  // Demo mesajlar (ilk yüklemede)
  React.useEffect(() => {
    addMustfymanMessage("Merhaba, bu ilk mesajım!");
    addMustfymanMessage("React ile chat ekranı yapıyoruz.");
    addMustfymanMessage("Mesajlar burada görünecek.");
  }, []);

  // Gönder butonuna veya Enter tuşuna basınca mesaj ekle
  function handleSubmit(e) {
    e.preventDefault();
    addMustfymanMessage(inputText);
  }

  return (
    <div style={styles.page}>
      <aside style={styles.sidebar}>
        <h3>Sol Kenar</h3>
        <button style={styles.dummyButton}>Button 1</button>
        <button style={styles.dummyButton}>Button 2</button>
        <img
          style={styles.dummyImage}
          src="https://via.placeholder.com/100"
          alt="dummy"
        />
      </aside>

      <main style={styles.chatArea}>
        <h2>Mustfyman Chat</h2>
        <div style={styles.chatBox}>
          {messages.map((msg, i) => (
            <div key={i} style={styles.chatMessage}>
              <strong>{msg.username}: </strong>
              <span>{msg.text}</span>
            </div>
          ))}
        </div>
        
        {/* Mesaj gönderme formu */}
        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            type="text"
            placeholder="Mesaj yaz..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            style={styles.input}
          />
          <button type="submit" style={styles.sendButton}>Gönder</button>
        </form>
      </main>

      <aside style={styles.sidebar}>
        <h3>Sağ Kenar</h3>
        <button style={styles.dummyButton}>Button A</button>
        <button style={styles.dummyButton}>Button B</button>
        <img
          style={styles.dummyImage}
          src="https://via.placeholder.com/100"
          alt="dummy"
        />
      </aside>
    </div>
  );
}

const styles = {
  page: {
    display: "flex",
    height: "100vh",
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    backgroundColor: "#f0f2f5",
  },
  sidebar: {
    flex: "0 0 15%",
    backgroundColor: "#fff",
    borderRight: "1px solid #ddd",
    padding: 20,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  dummyButton: {
    margin: "10px 0",
    padding: "10px 20px",
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
    backgroundColor: "#007bff",
    color: "#fff",
    fontWeight: "bold",
  },
  dummyImage: {
    marginTop: 20,
    borderRadius: 12,
  },
  chatArea: {
    flex: 1,
    padding: 30,
    backgroundColor: "#e5e7eb",
    display: "flex",
    flexDirection: "column",
    borderRadius: "0 12px 12px 0",
  },
  chatBox: {
    flex: 1,
    overflowY: "auto",
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 20,
    boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
    marginBottom: 15,
  },
  chatMessage: {
    marginBottom: 12,
    padding: "8px 12px",
    backgroundColor: "#d1e7dd",
    borderRadius: 10,
    maxWidth: "70%",
  },
  form: {
    display: "flex",
  },
  input: {
    flex: 1,
    padding: 10,
    borderRadius: 10,
    border: "1px solid #ccc",
    fontSize: 16,
  },
  sendButton: {
    marginLeft: 10,
    padding: "10px 20px",
    borderRadius: 10,
    border: "none",
    backgroundColor: "#28a745",
    color: "#fff",
    fontWeight: "bold",
    cursor: "pointer",
  },
};

export default App;
