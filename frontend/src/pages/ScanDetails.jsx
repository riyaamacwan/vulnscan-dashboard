import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import client from "../api/client";

export default function ScanDetails() {
  const { id } = useParams();
  const [scan, setScan] = useState(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      const response = await client.get(`/scans/${id}`);
      setScan(response.data);

      if (response.data.status === "completed" || response.data.status === "failed") {
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [id]);

  if (!scan) return <p className="p-6">Loading scan…</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-2">Scan #{scan.id}</h1>
      <p>Status: {scan.status}</p>
      <p>Target: {scan.target}</p>

      <div className="mt-6 space-y-3">
        {scan.findings.map((finding) => (
          <div key={finding.id} className="p-4 bg-white rounded shadow">
            <h2 className="font-semibold">{finding.title}</h2>
            <p className="text-sm text-gray-600">
              Severity: {finding.severity} | Category: {finding.category}
            </p>
            <p>{finding.description}</p>
            <p className="text-sm mt-2">
              <strong>Remediation:</strong> {finding.remediation}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}