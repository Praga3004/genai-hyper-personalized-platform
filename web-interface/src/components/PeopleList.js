import React from "react";
import PersonRow from "./PersonRow";
export default function PeopleList({ data, selected, toggleSelect }) {
  // ✅ Guarantee safe defaults even if parent sends undefined
  const safeData = Array.isArray(data) ? data : [];
  const safeSelected = selected instanceof Set ? selected : new Set();

  const allSelected =
    safeData.length > 0 && safeData.every((p) => safeSelected.has(p.id));

  const toggleAll = () => {
    const next = new Set(safeSelected);
    if (allSelected) safeData.forEach((p) => next.delete(p.id));
    else safeData.forEach((p) => next.add(p.id));
    toggleSelect(next, true);
  };

  return (
    <div className="card">
      <table className="table">
        <thead>
          <tr>
            <th><input type="checkbox" checked={allSelected} onChange={toggleAll} /></th>
            <th>Name</th><th>Age</th><th>Gender</th><th>Location</th><th>Email</th><th>Phone</th>
          </tr>
        </thead>
        <tbody>
          {safeData.map((person) => (
            <PersonRow
              key={person.id}
              person={person}
              isSelected={safeSelected.has(person.id)}
              onToggle={() => {
                const next = new Set(safeSelected);
                next.has(person.id) ? next.delete(person.id) : next.add(person.id);
                toggleSelect(next);
              }}
            />
          ))}
          {safeData.length === 0 && (
            <tr>
              <td colSpan={7} style={{ color: "#9ca3af", padding: 18 }}>
                No rows
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
