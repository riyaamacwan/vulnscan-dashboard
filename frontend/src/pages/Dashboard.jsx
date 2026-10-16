import { useEffect, useState } from "react";
import client from "../api/client";
import SeverityCard from "../components/SeverityCard";

export default function Dashboard() {
  const [findings, setFindings] = useState([]);

  useEffect(() => {
    client
      .get("/findings")
      .then((response) => setFindings(response.data))
      .catch((error) => console.error(error));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Security Dashboard</h1>
      <SeverityCard findings={findings} />

      <div className="mt-8 bg-white rounded-xl shadow p-4">
        <h2 className="font-semibold mb-3">Recent Findings</h2>
        <ul>
          {findings.map((finding) => (
            <li key={finding.id} className="border-b py-2">
              <strong>{finding.title}</strong> — {finding.severity}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}