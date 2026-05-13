import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([]);

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
      alert("Upload Failed");
    }

    setLoading(false);
  };

  const askQuestion = async () => {
    if (!question) {
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post("http://localhost:8000/chat", {
        question: question,
      });

      const userMessage = {
        role: "user",
        content: question,
      };

      const assistantMessage = {
        role: "assistant",
        content: response.data.answer,
      };

      setMessages((previous) => [...previous, userMessage, assistantMessage]);

      setQuestion("");
    } catch (error) {
      console.log(error);
      alert("Chat failed");
    }

    setLoading(false);
  };

  return (
    <div className="app-container">
      <div className="chat-card">
        <div className="header">
          <h1>RAG AI Assistant</h1>
          <p>Upload TXT files and chat with your documents</p>
        </div>

        <div className="upload-section">
          <h2>Upload Document</h2>

          <div className="upload-row">
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />

            <button onClick={uploadFile} disabled={loading}>
              Upload
            </button>
          </div>

          {file && <p className="file-name">Selected File: {file.name}</p>}
        </div>

        <div className="chat-section">
          <div className="messages-container">
            {messages.length === 0 && (
              <div className="empty-chat">
                <p>Ask questions about your uploaded documents.</p>
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

          <div className="question-section">
            <input
              type="text"
              placeholder="Ask a question about your documents..."
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
    </div>
  );
}

export default App;
