import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function NewScan() {
  const [host, setHost] = useState("");
  const [ports, setPorts] = useState("1-1000");
  const [authorized, setAuthorized] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await client.post("/scans", {
        host,
        ports,
        authorized,
      });

      navigate(`/scans/${response.data.scan_id}`);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to start scan");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-6 max-w-lg mx-auto space-y-4">
      <h1 className="text-2xl font-bold">New Vulnerability Scan</h1>

      <input
        className="w-full border p-2 rounded"
        placeholder="Target host or IP"
        value={host}
        onChange={(event) => setHost(event.target.value)}
        required
      />

      <input
        className="w-full border p-2 rounded"
        placeholder="Port range, e.g. 1-1000"
        value={ports}
        onChange={(event) => setPorts(event.target.value)}
      />

      <label className="flex items-center gap-2">
        <input
          type="checkbox"
          checked={authorized}
          onChange={(event) => setAuthorized(event.target.checked)}
          required
        />
        I own this system or have written authorization to scan it.
      </label>

      <button className="bg-blue-600 text-white px-4 py-2 rounded">
        Start Scan
      </button>

      {error && <p className="text-red-600">{error}</p>}
    </form>
  );
}