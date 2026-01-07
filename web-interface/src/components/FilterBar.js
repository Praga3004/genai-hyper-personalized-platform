import React from "react";

export default function FilterBar({ filters, setFilters, filterOptions = {} }) {
  const {
    villages = [],
    districts = [],
    wards = [],
    voter_categories = [],
    issue_categories = [],
    genders = [],
  } = filterOptions;

  return (
    <div className="card pad" style={{ marginBottom: 16 }}>
      <div className="filters" style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "12px" }}>
        {/* 👤 Voter Category */}
        <div>
          <label>Voter Category</label>
          <select
            value={filters.voter_category || "ALL"}
            onChange={(e) =>
              setFilters((f) => ({ ...f, voter_category: e.target.value }))
            }
          >
            <option value="ALL">All Categories</option>
            {voter_categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>

        {/* 📋 Issue Category */}
        <div>
          <label>Issue Category</label>
          <select
            value={filters.issue_category || "ALL"}
            onChange={(e) =>
              setFilters((f) => ({ ...f, issue_category: e.target.value }))
            }
          >
            <option value="ALL">All Issues</option>
            {issue_categories.map((cat) => (
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
            value={filters.gender || "ALL"}
            onChange={(e) =>
              setFilters((f) => ({ ...f, gender: e.target.value }))
            }
          >
            <option value="ALL">All</option>
            {genders.map((g) => (
              <option key={g} value={g}>
                {g}
              </option>
            ))}
          </select>
        </div>

        {/* 🏘️ Village */}
        <div>
          <label>Village</label>
          <select
            value={filters.village || "ALL"}
            onChange={(e) =>
              setFilters((f) => ({ ...f, village: e.target.value }))
            }
          >
            <option value="ALL">All Villages</option>
            {villages.map((v) => (
              <option key={v} value={v}>
                {v}
              </option>
            ))}
          </select>
        </div>

        {/* 🏙️ District */}
        <div>
          <label>District</label>
          <select
            value={filters.district || "ALL"}
            onChange={(e) =>
              setFilters((f) => ({ ...f, district: e.target.value }))
            }
          >
            <option value="ALL">All Districts</option>
            {districts.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </div>

        {/* 🏢 Ward */}
        <div>
          <label>Ward</label>
          <select
            value={filters.ward || "ALL"}
            onChange={(e) =>
              setFilters((f) => ({ ...f, ward: e.target.value }))
            }
          >
            <option value="ALL">All Wards</option>
            {wards.map((w) => (
              <option key={w} value={w}>
                {w}
              </option>
            ))}
          </select>
        </div>

        {/* 🎂 Age */}
        <div>
          <label>Age Range</label>
          <select
            value={filters.age || "ALL"}
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
          <label>Search (Name / ID)</label>
          <input
            type="text"
            value={filters.q || ""}
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
