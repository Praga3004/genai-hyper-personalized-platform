// src/components/ResultTable.js
import React from "react";
import "./ResultTable.css";

export default function ResultTable({ results = [] }) {
  if (!results || results.length === 0) return null;

  return (
    <div className="card pad">
      <div className="card table-shell">
      <div className="table-scroll">
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Category</th>
            <th>Location</th>
            {/* <th>Base Message</th> */}
            <th>Message</th>
            {/* <th>Slogan</th> */}
            <th>Image</th>
            <th>Audio</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r, i) => (
            <tr key={r.id || i}>
              <td>{r.id || i + 1}</td>
              <td>{r.name}</td>
              <td>{r.category}</td>
              <td>{r.location}</td>
              {/* <td style={{ whiteSpace: "pre-wrap" }}>{r.base_message}</td> */}
              <td style={{ whiteSpace: "pre-wrap" }}>{r.final_message_tamil}</td>
              {/* <td><b>{r.slogan}</b></td> */}
              <td>
                    {r.image_url ? (
                      <img
                        src={`https://genai-hyper-personalized-platform-v.vercel.app/${r.image_url}`}
                        alt="Generated"
                        style={{
                          width: "120px",
                          height: "120px",
                          objectFit: "cover",
                          borderRadius: "8px",
                          boxShadow: "0 2px 6px rgba(0,0,0,0.2)",
                        }}
                      />
                    ) : (
                      <span style={{ opacity: 0.5 }}>No image</span>
                    )}
                  </td>
              <td>
                    {r.audio_url ? (
                      <audio 
                        controls 
                        style={{ width: "160px" }}
                        src={`https://genai-hyper-personalized-platform-v.vercel.app/${r.audio_url}`}
                      >
                        Your browser does not support audio playback.
                      </audio>
                    ) : (
                      <span style={{ opacity: 0.5 }}>No audio</span>
                    )}
                  </td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
      </div>
    </div>
  );
}
