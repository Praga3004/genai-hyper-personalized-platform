// src/components/PeopleTable.js
import React, { useMemo } from "react";
import "./PeopleTable.css";

export default function PeopleTable({ rows = [], selectedIds = new Set(), setSelectedIds }) {
  // number selected on current page
  const selectedCount = useMemo(() => {
    let c = 0;
    rows.forEach((r) => {
      if (selectedIds.has(String(r.id))) c++;
    });
    return c;
  }, [rows, selectedIds]);

  const allOnPageSelected = rows.length > 0 && selectedCount === rows.length;

  const toggleOne = (id) => {
    const sid = String(id);
    const next = new Set(selectedIds);
    if (next.has(sid)) next.delete(sid);
    else next.add(sid);
    setSelectedIds(next);
  };

  const toggleAll = () => {
    const next = new Set(selectedIds);
    if (allOnPageSelected) {
      // unselect all visible rows
      rows.forEach((r) => next.delete(String(r.id)));
    } else {
      rows.forEach((r) => next.add(String(r.id)));
    }
    setSelectedIds(next);
  };

  return (
    <div className="card table-shell">
      <div className="table-scroll">
        <table className="table">
          <thead>
            <tr>
              <th style={{ width: 32 }}>
                <input
                  type="checkbox"
                  checked={allOnPageSelected}
                  onChange={toggleAll}
                />
              </th>
              <th>ID</th>
              <th>Name</th>
              <th>Age</th>
              <th>Gender</th>
              <th>Location</th>
              <th>Village</th>
              <th>District</th>
              <th>Ward</th>
              <th>Area</th>
              <th>Street</th>
              <th>Booth Number</th>
              <th>Voter Category</th>
              <th>Issue Category</th>
              <th>Issue Description</th>
            
            </tr>
          </thead>
          <tbody>
            {rows.length > 0 ? (
              rows.map((r) => {
                const rid = String(r.id);
                return (
                  <tr key={rid}>
                    <td>
                      <input
                        type="checkbox"
                        checked={selectedIds.has(rid)}
                        onChange={() => toggleOne(rid)}
                      />
                    </td>

                    <td style={{ fontWeight: 600 }}>{rid}</td>
                    <td><strong>{r.name || "N/A"}</strong></td>
                    <td>{r.age || "N/A"}</td>
                    <td>{r.gender || "N/A"}</td>
                    <td>{r.location || "N/A"}</td>
                    <td>{r.village || "N/A"}</td>
                    <td>{r.district || "N/A"}</td>
                    <td>{r.ward || "N/A"}</td>
                    <td>{r.area || "N/A"}</td>
                    <td>{r.street || "N/A"}</td>
                    <td>{r.booth_number || "N/A"}</td>
                    <td>{r.voter_category || "N/A"}</td>
                    <td>{r.issue_category || <span style={{ opacity: 0.5, fontStyle: "italic" }}>No category</span>}</td>
                    <td style={{ whiteSpace: "pre-wrap", maxWidth: "300px", wordWrap: "break-word" }}>
                      {r.issue_description || <span style={{ opacity: 0.5, fontStyle: "italic" }}>No issue specified</span>}
                    </td>
                   
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={15} style={{ color: "#9ca3af", padding: 18 }}>
                  No rows
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
