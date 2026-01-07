// GenerateContentBar.js
import React from "react";

export default function GenerateContentBar({
  totalSelected,
  onGenerate,
}) {
  const isEnabled = totalSelected === 6;
  
  return (
    <div style={{ marginTop: 20 }}>
      <div className="row spread footer-bar">
        <div className="badge">
          {totalSelected} selected {totalSelected !== 6 && `(need exactly 6)`}
        </div>
        <button
          className="btn"
          disabled={!isEnabled}
          onClick={onGenerate}
        >
          Generate Content
        </button>
      </div>
    </div>
  );
}
