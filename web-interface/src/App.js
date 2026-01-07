import React, { useMemo, useState, useEffect, useCallback } from "react";
import "./App.css";
import FilterBar from "./components/FilterBar";
import PeopleTable from "./components/PeopleTable";
import GenerateContentBar from "./components/GenerateContentBar";
import ResultTable from "./components/ResultTable";

function App() {
  const [rows, setRows] = useState([]);
  const [filters, setFilters] = useState({
    location: "ALL",
    category: "ALL",
    gender: "ALL",
    age: "ALL",
    q: "",
    voter_category: "ALL",
    issue_category: "ALL",
    village: "ALL",
    district: "ALL",
    ward: "ALL",
  });
  const [page, setPage] = useState(1);
  const [selectedIds, setSelectedIds] = useState(new Set());

  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);       // Loading from database
  const [isGenerating, setIsGenerating] = useState(false); // Campaign generation
  const [filterOptions, setFilterOptions] = useState({
    villages: [],
    districts: [],
    wards: [],
    voter_categories: [],
    issue_categories: [],
    genders: [],
  });

  // Use environment variable or fallback to default
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

  // Load filter options on mount
  useEffect(() => {
    fetch(`${API_BASE_URL}/api/voters/filters/options`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Failed to load filter options: ${res.status} ${res.statusText}`);
        }
        return res.json();
      })
      .then((data) => {
        setFilterOptions({
          villages: data.villages || [],
          districts: data.districts || [],
          wards: data.wards || [],
          voter_categories: data.voter_categories || [],
          issue_categories: data.issue_categories || [],
          genders: data.genders || [],
        });
      })
      .catch((err) => {
        console.error("Error loading filter options:", err);
        alert("Failed to load filter options. Please check your API connection.");
      });
  }, [API_BASE_URL]);

  // Load voters based on filters - use useCallback to prevent infinite loops
  const loadVoters = useCallback(() => {
    setIsLoading(true);
    
    const params = new URLSearchParams();
    if (filters.voter_category !== "ALL") {
      params.append("voter_category", filters.voter_category);
    }
    if (filters.issue_category !== "ALL") {
      params.append("issue_category", filters.issue_category);
    }
    if (filters.gender !== "ALL") {
      params.append("gender", filters.gender);
    }
    if (filters.village !== "ALL") {
      params.append("village", filters.village);
    }
    if (filters.district !== "ALL") {
      params.append("district", filters.district);
    }
    if (filters.ward !== "ALL") {
      params.append("ward", filters.ward);
    }
    if (filters.age !== "ALL") {
      const [min, max] = filters.age === "51+" ? [51, 200] : filters.age.split("-").map(Number);
      params.append("age_min", min);
      params.append("age_max", max);
    }
    if (filters.q) {
      params.append("search", filters.q);
    }
    params.append("limit", "500"); // Load up to 500 records

    fetch(`${API_BASE_URL}/api/voters?${params.toString()}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Failed to load voters: ${res.status} ${res.statusText}`);
        }
        return res.json();
      })
      .then((data) => {
        // Transform Supabase data to match VoterProfileIn structure
        const transformedRows = (data.results || []).map((v) => {
          // Construct location from village/area/ward
          let location = "";
          if (v.village) location = v.village;
          else if (v.area) location = v.area;
          if (v.ward) location += (location ? ", " : "") + `Ward ${v.ward}`;
          if (!location) location = "Unknown";

          // Return all fields matching VoterProfileIn structure
          return {
            id: v.voter_id,
            name: v.voter_name || "",
            age: v.age || 0,
            gender: v.gender || "",
            location: location,
            booth_number: v.booth_number || "",
            ward: v.ward || "",
            area: v.area || "",
            street: v.street || "",
            village: v.village || "",
            district: v.district || "",
            voter_category: v.voter_category || "",
            issue_category: v.issue_category || "",
            issue_description: v.issue_description || "",
          };
        });
        
        setRows(transformedRows);
      })
      .catch((err) => {
        console.error("Error loading voters:", err);
        alert(`Failed to load voters from database: ${err.message}`);
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [filters, API_BASE_URL]);

  // Load voters when filters change
  useEffect(() => {
    loadVoters();
  }, [loadVoters]);


  const goBack = () => setPage(1);
  const goNext = () => setPage(2);

  // Client-side filtering for search and other local filters
  const filteredRows = useMemo(() => {
    return rows.filter((r) => {
      if (filters.q && !r.name.toLowerCase().includes(filters.q.toLowerCase())) {
        return false;
      }
      return true;
    });
  }, [rows, filters.q]);


  // GENERATE CAMPAIGN from selected voter IDs
  const handleGenerate = () => {
    const selectedRows = rows.filter((r) => selectedIds.has(r.id));

    if (selectedRows.length !== 6) {
      alert("Please select exactly 6 voters to generate content.");
      return;
    }

    setIsGenerating(true);
    setResults([]);

    // Use the new endpoint that fetches from Supabase by IDs
    const voterIds = selectedRows.map((r) => r.id);
    
    fetch(`${API_BASE_URL}/api/generate-campaign-from-ids`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ voter_ids: voterIds }),
    })
      .then((res) => {
        if (!res.ok) {
          return res.text().then(text => {
            throw new Error(`Backend error (${res.status}): ${text}`);
          });
        }
        return res.json();
      })
      .then((data) => {
        setResults(Array.isArray(data) ? data : data?.results || []);
      })
      .catch((err) => {
        console.error("❌ Generate error:", err);
        alert(`Failed to generate campaign: ${err.message}`);
      })
      .finally(() => {
        setIsGenerating(false);
      });
  };

  const selectedRowsList = useMemo(
    () => rows.filter((r) => selectedIds.has(r.id)),
    [rows, selectedIds]
  );

  return (
    <div className="container">
      <h1 className="h1">TN Voter Targeting Console</h1>

      {/* FULL-SCREEN GENERATE OVERLAY (pure boolean flag) */}
      {isGenerating && (
        <div className="overlay-loading">
          <div className="overlay-box">
            <div className="spinner" />
            <p>Generating campaign content...</p>
          </div>
        </div>
      )}

      {/* LOADING INDICATOR */}
      {isLoading && (
        <div className="card pad" style={{ textAlign: "center" }}>
          <div className="spinner" />
          <p>Loading voters from database...</p>
        </div>
      )}

      {/* PAGE 1 */}
      {page === 1 && !isLoading && (
        <>
          <FilterBar
            rows={rows}
            filters={filters}
            setFilters={setFilters}
            filterOptions={filterOptions}
          />
         
          <PeopleTable
            rows={filteredRows}
            selectedIds={selectedIds}
            setSelectedIds={setSelectedIds}
          />
       

          <GenerateContentBar
            totalSelected={selectedRowsList.length}
            onGenerate={handleGenerate}
          />

          <div style={{ marginTop: 20, textAlign: "center" }}>
            {results.length > 0 && (
              <button className="btn" onClick={goNext}>
                Next →
              </button>
            )}
          </div>
        </>
      )}

      {/* PAGE 2 - RESULTS */}
      {page === 2 && (
        <div style={{ marginTop: 20 }}>
          <h3>Generated Results</h3>

          <ResultTable results={results} />

          <div style={{ marginTop: 20, textAlign: "center" }}>
            <button className="btn" onClick={goBack}>
              ← Back
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
