import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import client from "../api/client";

const severityStyles = {
  critical: "bg-red-100 text-red-800 border-red-300",
  high: "bg-orange-100 text-orange-800 border-orange-300",
  medium: "bg-yellow-100 text-yellow-800 border-yellow-300",
  low: "bg-blue-100 text-blue-800 border-blue-300",
  info: "bg-gray-100 text-gray-800 border-gray-300",
};

export default function ScanDetails() {
  const { id } = useParams();
  const [scan, setScan] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let interval;

    const fetchScan = async () => {
      try {
        const response = await client.get(`/scans/${id}`);
        setScan(response.data);
        setError("");

        if (
          response.data.status === "completed" ||
          response.data.status === "failed"
        ) {
          clearInterval(interval);
        }
      } catch (err) {
        setError("Unable to load this scan.");
        clearInterval(interval);
      } finally {
        setLoading(false);
      }
    };

    fetchScan();
    interval = setInterval(fetchScan, 2000);

    return () => clearInterval(interval);
  }, [id]);

  if (loading) {
    return <p className="p-6 text-gray-600">Loading scan details…</p>;
  }

  if (error) {
    return (
      <div className="p-6">
        <p className="text-red-600">{error}</p>
        <Link to="/" className="text-blue-600 underline">
          Back to dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <Link to="/" className="text-blue-600 underline">
        ← Back to Dashboard
      </Link>

      <h1 className="text-3xl font-bold mt-4 mb-2">
        Scan #{scan.id}
      </h1>

      <div className="bg-white rounded-xl shadow p-5 mb-6">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-500">Target</p>
            <p className="font-semibold">{scan.target}</p>
          </div>

          <div>
            <p className="text-sm text-gray-500">Status</p>
            <p className="font-semibold capitalize">{scan.status}</p>
          </div>

          <div>
            <p className="text-sm text-gray-500">Started</p>
            <p className="font-semibold">
              {scan.started_at ? new Date(scan.started_at).toLocaleString() : "—"}
            </p>
          </div>

          <div>
            <p className="text-sm text-gray-500">Finished</p>
            <p className="font-semibold">
              {scan.finished_at ? new Date(scan.finished_at).toLocaleString() : "—"}
            </p>
          </div>
        </div>
      </div>

      <h2 className="text-xl font-bold mb-3">
        Findings ({scan.findings.length})
      </h2>

      {scan.findings.length === 0 ? (
        <div className="bg-white rounded-xl shadow p-5 text-gray-600">
          No findings were generated for this scan.
        </div>
      ) : (
        <div className="space-y-4">
          {scan.findings.map((finding) => (
            <div
              key={finding.id}
              className="bg-white rounded-xl shadow p-5 border-l-4 border-gray-300"
            >
              <div className="flex justify-between items-start gap-4">
                <h3 className="text-lg font-semibold">
                  {finding.title}
                </h3>

                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold border ${
                    severityStyles[finding.severity] ||
                    "bg-gray-100 text-gray-800 border-gray-300"
                  }`}
                >
                  {finding.severity}
                </span>
              </div>

              <p className="text-sm text-gray-500 mt-1">
                Category: {finding.category}
              </p>

              <p className="mt-3">{finding.description}</p>

              {finding.evidence && (
                <div className="mt-3 bg-gray-50 p-3 rounded text-sm">
                  <strong>Evidence:</strong>
                  <pre className="whitespace-pre-wrap mt-1">
                    {finding.evidence}
                  </pre>
                </div>
              )}

              {finding.cve_ids && (
                <p className="mt-3 text-sm">
                  <strong>CVEs:</strong> {finding.cve_ids}
                </p>
              )}

              {finding.remediation && (
                <div className="mt-3 p-3 bg-green-50 rounded text-sm">
                  <strong>Remediation:</strong> {finding.remediation}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}