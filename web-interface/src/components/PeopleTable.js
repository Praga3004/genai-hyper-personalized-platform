// src/components/PeopleTable.js
import React, { useMemo } from "react";

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
              {/* <th>Ward</th> */}
              <th>Category</th>
              <th>Interests</th>
              <th>Pain Points</th>
              <th>Voter History</th>
            
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
                    <td>{r.name}</td>
                    <td>{r.age}</td>
                    <td>{r.gender}</td>
                    <td>{r.location}</td>
                    {/* <td>{r.ward}</td> */}
                    <td>{r.category}</td>

                    <td>{Array.isArray(r.interests) ? r.interests.join(", ") : r.interests}</td>
                    <td>{Array.isArray(r.pain_points) ? r.pain_points.join(", ") : r.pain_points}</td>

                    <td>{r.voter_history}</td>
                   
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={14} style={{ color: "#9ca3af", padding: 18 }}>
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
