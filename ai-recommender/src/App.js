// import { useState } from "react";

// function App() {
//   const [query, setQuery] = useState("");
//   const [products, setProducts] = useState([]);
//   const [answer, setAnswer] = useState("");

//   const handleSearch = async () => {
//     const res = await fetch(`http://127.0.0.1:8000/recommend?query=${query}`);
//     const data = await res.json();

//     setProducts(data.products);
//     setAnswer(data.answer);
//   };

//   return (
//     <div style={{ padding: "20px" }}>
//       <h1>AI Product Recommender 🤖</h1>

//       <input
//         type="text"
//         placeholder="Enter your need..."
//         value={query}
//         onChange={(e) => setQuery(e.target.value)}
//         style={{ width: "300px", padding: "10px" }}
//       />

//       <button onClick={handleSearch} style={{ marginLeft: "10px" }}>
//         Search
//       </button>

//       <h2>Recommendations:</h2>
//       {products.map((p) => (
//         <div key={p.id}>
//           <h3>{p.name}</h3>
//           <p>{p.description}</p>
//           <p>₹{p.price}</p>
//         </div>
//       ))}

//       <h2>AI Explanation:</h2>
//       <p>{answer}</p>
//     </div>
//   );
// }

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

    const res = await fetch(`http://127.0.0.1:8000/recommend?query=${query}`);
    const data = await res.json();

    setProducts(data.products);
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

      {loading && <p>⏳ Loading...</p>}

      <div className="grid">
        {products.map((p) => (
          <div className="card" key={p.id}>
            <h3>{p.name}</h3>
            <p>{p.description}</p>
            <h4>₹{p.price}</h4>
          </div>
        ))}
      </div>

      {answer && (
        <div className="answer-box">
          <h2>🤖 AI Recommendation</h2>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;