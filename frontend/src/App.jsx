// App.jsx

import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [sources, setSources] = useState([]);

  const uploadFile = async () => {
    if (!file) {
      alert("Please upload a file!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const response = await axios.post(
        "http://localhost:8000/upload",
        formData,
      );

      alert(response.data.message);
    } catch (error) {
      console.log(error);
      alert("Upload failed");
    }

    setLoading(false);
  };

  const askQuestion = async () => {
    if (!question) {
      return;
    }

    const userMessage = {
      role: "user",
      content: question,
    };

    setMessages((previous) => [...previous, userMessage]);

    try {
      setLoading(true);

      const response = await axios.post("http://localhost:8000/chat", {
        question: question,
      });

      const assistantMessage = {
        role: "assistant",
        content: response.data.answer,
      };

      setMessages((previous) => [...previous, assistantMessage]);
      setSources((previous) => [...previous, ...response.data.sources]);

      setQuestion("");
    } catch (error) {
      console.log(error);
      alert("Chat failed");
    }

    setLoading(false);
  };

  return (
    <div className="app">
      {/* LEFT SIDEBAR */}
      <div className="sidebar">
        <div>
          <h1 className="logo">RAG AI</h1>

          <p className="subtitle">Upload files and chat with them.</p>
        </div>

        <div className="upload-section">
          <h2>Upload Document</h2>

          <input type="file" onChange={(e) => setFile(e.target.files[0])} />

          {file && <p className="file-name">{file.name}</p>}

          <button onClick={uploadFile} disabled={loading}>
            Upload
          </button>
        </div>
      </div>

      {/* RIGHT CHAT AREA */}
      <div className="chat-layout">
        {/* HEADER */}
        <div className="chat-header">AI Chat Assistant</div>

        {/* MESSAGES */}
        <div className="messages-container">
          {messages.length === 0 && (
            <div className="empty-state">
              Ask questions about your uploaded documents.
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={
                message.role === "user"
                  ? "message user-message"
                  : "message assistant-message"
              }
            >
              <div className="message-role">
                {message.role === "user" ? "You" : "AI Assistant"}
              </div>

              <div className="message-content">
                <ReactMarkdown>{message.content}</ReactMarkdown>
              </div>
            </div>
          ))}

          {loading && <div className="loading-box">Thinking...</div>}
        </div>
        <div className="sources-panel">
          <h3>Sources</h3>

          {sources.length === 0 ? (
            <p>No sources yet</p>
          ) : (
            sources.map((s, i) => (
              <details key={i} className="source-accordion">
                <summary className="source-summary">
                  📄 {s.file_name} — Chunk #{s.chunk_id}
                </summary>

                <div className="source-content">
                  {s?.text || "No preview available"}
                </div>
              </details>
            ))
          )}
        </div>

        {/* INPUT */}
        <div className="chat-input-section">
          <input
            type="text"
            placeholder="Ask a question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                askQuestion();
              }
            }}
          />

          <button onClick={askQuestion} disabled={loading}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
