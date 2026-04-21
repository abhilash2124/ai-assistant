// export default App;
import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [products, setProducts] = useState([]);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);

    const res = await fetch(`http://127.0.0.1:8000/agent?query=${query}`);
    const data = await res.json();

    // setProducts(data.products);
    setProducts(data.products || []);
    setAnswer(data.answer);
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>AI Product Recommender 🤖</h1>

      <div className="search-box">
        <input
          type="text"
          placeholder="Search for products..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {loading && <div className="loader"></div>}


      <div className="grid">
        {products.map((p, index) => (
          <div className="card" key={p.id}>

            {index === 0 && <span className="badge">🏆 Best Match</span>}

            <h3 className="title">{p.name}</h3>

            <p className="desc">{p.description}</p>

            <div className="price-row">
              <span className="price">₹{p.price}</span>
              <span className="category">{p.category}</span>
            </div>

          </div>
        ))}
      </div>


      {answer && (
        <div className="ai-box">
          <div className="ai-header">
            <span>🤖</span>
            <h2>AI Recommendation</h2>
          </div>

          <div className="ai-content">
            {answer.split("\n").map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;