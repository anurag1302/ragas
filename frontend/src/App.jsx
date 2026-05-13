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
      console.log(file);
      console.log(formData);
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
      let data = { question: question };
      const response = await axios.post("http://localhost:8000/chat", data);
      console.log(response.data.answer);

      const userMessage = {
        role: "user",
        content: question,
      };
      const assistantMessage = {
        role: "assistant",
        content: response.data.answer,
      };
      setMessages((previous) => [...previous, userMessage, assistantMessage]);
    } catch (error) {
      console.log(error);
      alert("Chat failed");
    }
    setLoading(false);
  };

  return (
    <>
      <h1>RAG Frontend</h1>
      <h2>Upload text file</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Upload</button>
      <h2>Ask Question</h2>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        style={{ width: 400 }}
      />
      <button onClick={askQuestion}>Ask</button>
      {loading && <p>Loading...</p>}
      <h2>Chat</h2>
      {messages.map((message, index) => (
        <div
          key={index}
          style={{ marginBottom: 20, padding: 10, border: "1px solid gray" }}
        >
          <h3>{message.role}</h3>
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>
      ))}
    </>
  );
}

export default App;
