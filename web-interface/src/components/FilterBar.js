import React, { useMemo } from "react";

export default function FilterBar({ rows, filters, setFilters, locations, categories }) {
  // Derive dropdown values dynamically from data
  const availableLocations = useMemo(() => {
    return Array.from(new Set(rows.map((r) => r.location).filter(Boolean))).sort();
  }, [rows]);

  const availableCategories = useMemo(() => {
    return Array.from(new Set(rows.map((r) => r.category).filter(Boolean))).sort();
  }, [rows]);

  const availableGenders = useMemo(() => {
    return Array.from(new Set(rows.map((r) => r.gender).filter(Boolean))).sort();
  }, [rows]);

  return (
    <div className="card pad" style={{ marginBottom: 16 }}>
      <div className="filters">
        {/* 🏙️ Location */}
        <div>
          <label>Location</label>
          <select
            value={filters.location}
            onChange={(e) =>
              setFilters((f) => ({ ...f, location: e.target.value }))
            }
          >
            <option value="ALL">All Locations</option>
            {availableLocations.map((loc) => (
              <option key={loc} value={loc}>
                {loc}
              </option>
            ))}
          </select>
        </div>

        {/* 🧩 Category */}
        <div>
          <label>Category</label>
          <select
            value={filters.category}
            onChange={(e) =>
              setFilters((f) => ({ ...f, category: e.target.value }))
            }
          >
            <option value="ALL">All Categories</option>
            {availableCategories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>

        {/* 👤 Gender */}
        <div>
          <label>Gender</label>
          <select
            value={filters.gender}
            onChange={(e) =>
              setFilters((f) => ({ ...f, gender: e.target.value }))
            }
          >
            <option value="ALL">All</option>
            {availableGenders.map((g) => (
              <option key={g} value={g}>
                {g}
              </option>
            ))}
          </select>
        </div>

        {/* 🎂 Age */}
        <div>
          <label>Age Range</label>
          <select
            value={filters.age}
            onChange={(e) =>
              setFilters((f) => ({ ...f, age: e.target.value }))
            }
          >
            <option value="ALL">All</option>
            <option value="18-21">18-21 (First-time voters)</option>
            <option value="22-35">22-35</option>
            <option value="36-50">36-50</option>
            <option value="51+">51+</option>
          </select>
        </div>

        {/* 🔍 Search */}
        <div>
          <label>Search (Name / Relative)</label>
          <input
            type="text"
            value={filters.q}
            onChange={(e) =>
              setFilters((f) => ({ ...f, q: e.target.value }))
            }
            placeholder="Type to search..."
          />
        </div>
      </div>
    </div>
  );
}
