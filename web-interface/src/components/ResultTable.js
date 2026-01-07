// src/components/ResultTable.js
import React, { useState } from "react";
import "./ResultTable.css";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

export default function ResultTable({ results = [] }) {
  const [selectedMessage, setSelectedMessage] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [isSendingBulk, setIsSendingBulk] = useState(false);
  
  if (!results || results.length === 0) return null;
  
  if (results.length !== 6) {
    return (
      <div className="card pad">
        <p style={{ color: "#ef4444", textAlign: "center" }}>
          Error: Expected exactly 6 results, but found {results.length}
        </p>
      </div>
    );
  }
  
  const handleMessageClick = (result) => {
    setSelectedMessage(result);
    setShowPopup(true);
  };
  
  const closePopup = () => {
    setShowPopup(false);
    setSelectedMessage(null);
  };

  const handleBulkSendSMS = async () => {
    if (results.length !== 6) {
      alert("Error: Must have exactly 6 results to send messages.");
      return;
    }

    setIsSendingBulk(true);

    try {
      // Prepare messages array
      const messages = results.map((result) => ({
        voter_id: result.id || result.voter_id || "",
        message: result.final_message_tamil || result.message_tamil || ""
      }));

      const response = await fetch(`${API_BASE_URL}/api/send-bulk-sms`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ messages }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Server returned ${response.status}`);
      }

      const data = await response.json();
      const successCount = data.total_sent || 0;
      const failCount = data.total_failed || 0;

      if (failCount === 0) {
        alert(`✓ Successfully sent all 6 messages!`);
      } else {
        alert(`Sent ${successCount} message(s) successfully. ${failCount} failed.`);
      }
    } catch (err) {
      console.error("Error sending bulk SMS:", err);
      alert(`Failed to send messages: ${err.message}`);
    } finally {
      setIsSendingBulk(false);
    }
  };

  return (
    <>
    <div className="card pad">
      <div className="row spread footer-bar" style={{ marginBottom: "15px" }}>
        <div className="badge">{results.length} messages ready</div>
        <button
          className="btn"
          disabled={isSendingBulk}
          onClick={handleBulkSendSMS}
        >
          {isSendingBulk ? "Sending..." : "Send Message"}
        </button>
      </div>
      
      <div className="card table-shell">
      <div className="table-scroll">
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Age</th>
            <th>Gender</th>
            <th>Voter Category</th>
            <th>Issue Category</th>
            <th>Issue Description</th>
            <th>Location</th>
            <th>Message</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r, i) => (
            <tr 
              key={r.id || r.voter_id || i}
              onClick={() => handleMessageClick(r)}
              style={{ cursor: "pointer" }}
            >
              <td>{r.id || r.voter_id || i + 1}</td>
              <td><strong>{r.name || r.voter_name || "N/A"}</strong></td>
              <td>{r.age ? r.age : "N/A"}</td>
              <td>{r.gender || "N/A"}</td>
              <td>{r.voter_category || r.category || "N/A"}</td>
              <td>
                {r.issue_category ? (
                  <span style={{ fontWeight: 500 }}>{r.issue_category}</span>
                ) : (
                  <span style={{ opacity: 0.5, fontStyle: "italic" }}>No category</span>
                )}
              </td>
              <td style={{ whiteSpace: "pre-wrap", maxWidth: "300px", wordWrap: "break-word" }}>
                {r.issue_description ? (
                  r.issue_description
                ) : (
                  <span style={{ opacity: 0.5, fontStyle: "italic" }}>No issue specified</span>
                )}
              </td>
              <td>{r.location || (r.village && r.district ? `${r.village}, ${r.district}` : (r.village || r.district || "N/A"))}</td>
              <td className="message-cell">
                <div className="cell-content">
                  {r.final_message_tamil || r.message_tamil || <span style={{ opacity: 0.5 }}>No message generated</span>}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
      </div>
    </div>
    
    {/* Message Popup Modal */}
    {showPopup && selectedMessage && (
      <div 
        className="message-popup-overlay"
        onClick={closePopup}
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: "rgba(0, 0, 0, 0.5)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 1000,
          padding: "20px"
        }}
      >
        <div 
          className="message-popup-content"
          onClick={(e) => e.stopPropagation()}
          style={{
            backgroundColor: "white",
            borderRadius: "8px",
            padding: "30px",
            maxWidth: "800px",
            maxHeight: "80vh",
            overflowY: "auto",
            boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
            position: "relative"
          }}
        >
          <button
            onClick={closePopup}
            style={{
              position: "absolute",
              top: "10px",
              right: "10px",
              background: "none",
              border: "none",
              fontSize: "24px",
              cursor: "pointer",
              color: "#666"
            }}
          >
            ×
          </button>
          
          <h2 style={{ marginTop: 0, marginBottom: "20px" }}>
            {selectedMessage.name || selectedMessage.voter_name || "Voter Details"}
          </h2>
          
          <div style={{ marginBottom: "20px" }}>
            <strong>Voter ID:</strong> {selectedMessage.id || selectedMessage.voter_id || "N/A"}
          </div>
          
          <div style={{ marginBottom: "20px" }}>
            <strong>Category:</strong> {selectedMessage.voter_category || selectedMessage.category || "N/A"}
          </div>
          
          <div style={{ marginBottom: "20px" }}>
            <strong>Issue Category:</strong> {selectedMessage.issue_category || "N/A"}
          </div>
          
          <div style={{ marginBottom: "20px" }}>
            <strong>Issue Description:</strong> {selectedMessage.issue_description || "N/A"}
          </div>
          
          <div style={{ marginBottom: "20px", padding: "15px", backgroundColor: "#f3f4f6", borderRadius: "4px" }}>
            <h3 style={{ marginTop: 0, marginBottom: "10px" }}>Tamil Message:</h3>
            <div style={{ 
              whiteSpace: "pre-wrap", 
              lineHeight: "1.8", 
              wordWrap: "break-word",
              overflowWrap: "break-word"
            }}>
              {selectedMessage.final_message_tamil || selectedMessage.message_tamil || "No message generated"}
            </div>
          </div>
        </div>
      </div>
    )}
    </>
  );
}
