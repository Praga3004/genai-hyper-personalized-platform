import React, { useState } from "react";

export default function GenerateContentButton({ selectedVoters }) {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!selectedVoters || selectedVoters.length === 0) return;
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/classify-voter", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({ voters: selectedVoters }),
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();
      setResults(data); // expecting a JSON response
    } catch (err) {
      console.error("Error generating content:", err);
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="generate-section">
      <div className="row spread footer-bar">
        <div className="badge">{selectedVoters.length} selected</div>
        <button
          className="btn"
          disabled={!selectedVoters.length || loading}
          onClick={handleGenerate}
        >
          {loading ? "Generating..." : "Generate Content"}
        </button>
      </div>

      {error && (
        <div style={{ color: "red", marginTop: "10px" }}>
          ❌ {error}
        </div>
      )}

      {results && (
        <div className="results" style={{ marginTop: 20 }}>
          <h3>Generated Results:</h3>
          <div className="results-list">
            {Array.isArray(results)
              ? results.map((r, i) => (
                  <div key={i} className="card" style={{ marginBottom: 12 }}>
                    <pre>{JSON.stringify(r, null, 2)}</pre>
                  </div>
                ))
              : <pre>{JSON.stringify(results, null, 2)}</pre>}
          </div>
        </div>
      )}
    </div>
  );
}
