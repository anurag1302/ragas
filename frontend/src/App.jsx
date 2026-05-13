import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

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
      alert(response.data);
    } catch (error) {
      console.log(error);
      alert("Upload Failed");
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
    </>
  );
}

export default App;
