import { useState } from "react";
import "./styles.css";

function App() {
  const [topic, setTopic] = useState("");
  const [language, setLanguage] = useState("English");
  const [post, setPost] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPost("");

    try {
      const res = await fetch("http://127.0.0.1:8000/generate-post", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, language }),
      });

      const data = await res.json();
      setPost(data.post);
    } catch (err) {
      console.error(err);
      setPost("Error generating post. Try again.");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>LinkedIn Post Generator</h1>
      <form onSubmit={handleSubmit}>
        <label>Topic:</label>
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter topic..."
          required
        />

        <label>Language:</label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          <option value="English">English</option>
          <option value="Bengali">Bengali</option>
          <option value="Spanish">Spanish</option>
        </select>

        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Post"}
        </button>
      </form>

      {post && (
        <div className="output">
          <h2>Generated LinkedIn Post:</h2>
          <p>{post}</p>
        </div>
      )}
    </div>
  );
}

export default App;
