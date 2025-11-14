import React from "react";

export default function PersonRow({ person, isSelected, onToggle }) {
  return (
    <tr>
      <td>
        <input type="checkbox" checked={isSelected} onChange={onToggle} />
      </td>
      <td style={{ fontWeight: 600 }}>{person.id}</td>
      <td>{person.name}</td>
      <td>{person.age}</td>
      <td>{person.gender}</td>
      <td>{person.location}</td>
      <td>{person.ward}</td>
      <td>{person.category}</td>
      <td>{Array.isArray(person.interests) ? person.interests.join(", ") : person.interests}</td>
      <td>{Array.isArray(person.pain_points) ? person.pain_points.join(", ") : person.pain_points}</td>
      <td>{person.voter_history}</td>

    </tr>
  );
}
