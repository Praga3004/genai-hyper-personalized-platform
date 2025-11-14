import * as XLSX from "xlsx";

// npm install xlsx
export async function readExcelFile(file) {
  const data = await file.arrayBuffer();
  const wb = XLSX.read(data, { type: "array" });
  const ws = wb.Sheets[wb.SheetNames[0]];
  const raw = XLSX.utils.sheet_to_json(ws, { defval: "" });

  // Map Excel headers to normalized keys
  const keyMap = {
    "s.no": "sno",
    sno: "sno",
    id: "id",
    name: "name",
    age: "age",
    gender: "gender",
    location: "location",
    ward: "ward",
    category: "category",
    interests: "interests",
    "pain points": "painPoints",
    "pain_points": "painPoints",
    voter_history: "voterHistory",
    "preferred_language": "preferredLanguage",
    phone: "phone",
    email: "email",
  };

  return raw.map((row, idx) => {
    const norm = {};

    // Normalize each cell key
    Object.entries(row).forEach(([k, v]) => {
      const key = String(k).trim().toLowerCase();
      const mapped = keyMap[key];
      if (mapped) norm[mapped] = String(v).trim();
    });

    // Split comma-separated interests and pain points
    const interests = norm.interests
      ? norm.interests.split(",").map((s) => s.trim())
      : [];

    const pain_points = norm.painPoints
      ? norm.painPoints.split(",").map((s) => s.trim())
      : [];

    return {
      id: norm.id || `TNAV${String(idx + 1).padStart(3, "0")}`,
      name: norm.name || "",
      age: Number(norm.age) || 0,
      gender: norm.gender || "",
      location: norm.location || "",
      ward: norm.ward || "",
      category: norm.category || "Unclassified",
      interests,
      pain_points,
      voter_history: norm.voterHistory || "Unknown",
      preferred_language: norm.preferredLanguage || "Tamil",
      contact: {
        phone: norm.phone || "",
        email: norm.email || "",
      },
    };
  });
}
