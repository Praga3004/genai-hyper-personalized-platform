import React, { useMemo, useState } from "react";
import "./App.css";
import FilterBar from "./components/FilterBar";
import PeopleTable from "./components/PeopleTable";
import GenerateContentBar from "./components/GenerateContentBar";
import ResultTable from "./components/ResultTable";
import { readExcelFile } from "./utils/excel";

function App() {
  const [rows, setRows] = useState([]);
  const [filters, setFilters] = useState({
    location: "ALL",
    category: "ALL",
    gender: "ALL",
    age: "ALL",
    q: "",
  });
  const [page, setPage] = useState(1);
  const [selectedIds, setSelectedIds] = useState(new Set());

  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);       // Excel uploading
  const [isGenerating, setIsGenerating] = useState(false); // Campaign generation
  const [isUploaded, setIsUploaded] = useState(false);

  const locations = useMemo(
    () =>
      Array.from(new Set(rows.map((r) => r.location).filter(Boolean))).sort(),
    [rows]
  );

  const goBack = () => setPage(1);
  const goNext = () => setPage(2);

  // FILTER LOGIC
  const filteredRows = useMemo(() => {
    return rows.filter((r) => {
      if (filters.location !== "ALL" && r.location !== filters.location)
        return false;
      if (filters.category !== "ALL" && r.category !== filters.category)
        return false;
      if (filters.gender !== "ALL" && r.gender !== filters.gender) return false;

      if (filters.age !== "ALL") {
        const age = parseInt(r.age, 10);
        const [min, max] =
          filters.age === "51+" ? [51, 200] : filters.age.split("-").map(Number);
        if (age < min || age > max) return false;
      }

      if (
        filters.q &&
        !(`${r.name} ${r.relative}`.toLowerCase().includes(filters.q.toLowerCase()))
      )
        return false;

      return true;
    });
  }, [rows, filters]);

  const handleFileUpload = (file) => {
    setIsLoading(true);
    setResults([]);

    readExcelFile(file)
      .then((parsed) => {
        const parsedWithIds = parsed.map((v, i) => ({
          ...v,
          id: v.id || `local-${i + 1}`,
        }));

        return fetch("https://genai-hyper-personalized-platform-vxg3-8elra46mz-a-xtr-labs.vercel.app:8000/api/classify-voter", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ voters: parsedWithIds }),
        });
      })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Backend error: ${res.statusText}`);
        }
        return res.json();
      })
      .then((classified) => {
        const finalRows = (
          Array.isArray(classified) ? classified : classified?.results || []
        ).map((v, i) => ({
          ...v,
          id: v.id || `classified-${i + 1}`,
        }));

        setRows(finalRows);
        setIsUploaded(true);
      })
      .catch((err) => {
        console.error("❌ Upload/classify error:", err);
        alert("Failed to process file.");
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  // GENERATE CAMPAIGN (no async keyword)
  const handleGenerate = () => {
    const selectedRows = rows.filter((r) => selectedIds.has(r.id));

    if (selectedRows.length === 0) {
      alert("Please select at least one voter before generating.");
      return;
    }

    setIsGenerating(true);
    setResults([]);

    fetch("https://genai-hyper-personalized-platform-vxg3-8elra46mz-a-xtr-labs.vercel.app:8000/api/generate-campaign", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ voters: selectedRows }),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Backend error: ${res.statusText}`);
        }
        return res.json();
      })
      .then((data) => {
        setResults(Array.isArray(data) ? data : data?.results || []);
      })
      .catch((err) => {
        console.error("❌ Generate error:", err);
        alert("Failed to generate campaign.");
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

      {/* UPLOAD SECTION */}
      {!isUploaded && !isLoading && (
        <div className="card pad" style={{ marginBottom: 16 }}>
          <div className="row spread">
            <div>
              <div style={{ fontWeight: 700, marginBottom: 6 }}>Load Excel</div>
              <div className="badge">
                Columns: S.No, ID, Name, Age, Gender, Location, Ward, Category,
                Interests, Voter History
              </div>
            </div>
            <label className="btn" style={{ cursor: "pointer" }}>
              Upload
              <input
                type="file"
                hidden
                accept=".xlsx,.xls,.csv"
                onChange={(e) => {
                  const f = e.target.files?.[0];
                  if (!f) return;
                  handleFileUpload(f);
                  e.target.value = "";
                }}
              />
            </label>
          </div>
        </div>
      )}

      {/* MAIN LOADER FOR EXCEL */}
      {isLoading && (
        <div className="card pad" style={{ textAlign: "center" }}>
          <div className="spinner" />
          <p>Processing Excel...</p>
        </div>
      )}

      {/* UPLOAD AGAIN */}
      {isUploaded && !isLoading && !isGenerating && (
        <div className="card pad" style={{ textAlign: "center" }}>
          <button
            className="btn"
            onClick={() => {
              setIsUploaded(false);
              setRows([]);
              setResults([]);
              setSelectedIds(new Set());
              setPage(1);
            }}
          >
            Upload Again
          </button>
        </div>
      )}

      {/* PAGE 1 */}
      {page === 1 && rows.length > 0 && (
        <>
          <FilterBar
            rows={rows}
            filters={filters}
            setFilters={setFilters}
            locations={locations}
          />

          <PeopleTable
            rows={filteredRows}
            selectedIds={selectedIds}
            setSelectedIds={setSelectedIds}
          />

          <GenerateContentBar
            totalSelected={selectedRowsList.length}
            selectedRows={selectedRowsList}
            setResults_={setResults}
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
