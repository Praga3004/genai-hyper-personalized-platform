import React, { useState } from "react";
import "./CampaignSlideshow.css";

export default function CampaignSlideshow({ results }) {
  const [index, setIndex] = useState(0);

  if (!results || results.length === 0) return null;

  const current = results[index];

  const nextSlide = () => setIndex((i) => (i + 1) % results.length);
  const prevSlide = () => setIndex((i) => (i - 1 + results.length) % results.length);

  return (
    <div className="slideshow-container">
      <div className="slide-card" key={current.id}>
        <h2>{current.name}</h2>
        <p><strong>Category:</strong> {current.category}</p>
        <p><strong>Base Message:</strong> {current.base_message}</p>
        <p><strong>Final Message:</strong> {current.final_message}</p>
        <p><strong>Slogan:</strong> {current.slogan}</p>

        <div className="tooltip">
          <span className="tooltiptext">
            📢 <b>{current.name}</b> ({current.category})<br />
            🗣 {current.final_message}<br />
            💬 <i>{current.slogan}</i>
          </span>
          Touch / Hover to view message
        </div>
      </div>

      

      <div className="slide-indicator">
        {index + 1} / {results.length}
      </div>
    </div>
  );
}
