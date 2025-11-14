const API_BASE_URL = "https://your-backend-domain.com"; // change this

export async function classifyVoterProfile(profile) {
  const res = await fetch(`${API_BASE_URL}/classify-voter`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(profile)
  });

  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`API error: ${res.status} ${txt}`);
  }

  return res.json();
}
