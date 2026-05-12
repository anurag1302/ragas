import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <>
      <h1>RAG Frontend</h1>
      <h2>Upload text file</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
    </>
  );
}

export default App;
