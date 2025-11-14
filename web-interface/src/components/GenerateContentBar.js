// GenerateContentBar.js
import React, { useState } from "react";
// import ResultTable from "./ResultTable";   

export default function GenerateContentBar({
  totalSelected,
  selectedRows,
  onGenerate,     
  setResults_,    
}) {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    if (!selectedRows || selectedRows.length === 0) {
      alert("⚠️ Please select at least one voter.");
      return;
    }

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/generate-campaign",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({ voters: selectedRows }),  // Backend expects { voters: [...] }
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error (${response.status}): ${errorText}`);
      }

      const data = await response.json();

      // Backend returns { results: [...] }
      const validResults = data.results || [];

      setResults(validResults);
      setResults_(validResults);

      if (onGenerate) onGenerate(validResults);

    } catch (err) {
      console.error("❌ Error generating content:", err);
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: 20 }}>
      <div className="row spread footer-bar">
        <div className="badge">{totalSelected} selected</div>
        <button
          className="btn"
          disabled={loading || totalSelected === 0}
          onClick={onGenerate}
        >
          {loading ? "Generating..." : "Generate Content"}
        </button>
      </div>

      {/* Error message */}
      {error && (
        <div style={{ color: "red", marginTop: 10 }}>
          ❌ {error}
        </div>
      )}

      {/* Render the result table only when results are available */}
     
    </div>
  );
}
