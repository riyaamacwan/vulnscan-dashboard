import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function NewScan() {
  const [host, setHost] = useState("");
  const [ports, setPorts] = useState("1-1000");
  const [authorized, setAuthorized] = useState(false);
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const startScan = async (event) => {
    event.preventDefault();

    try {
      const response = await client.post("/scans", {
        host,
        ports,
        authorized,
      });

      navigate(`/scans/${response.data.scan_id}`);
    } catch (error) {
      setMessage(error.response?.data?.error || "Scan failed to start");
    }
  };

  return (
    <form onSubmit={startScan} className="p-6 max-w-lg space-y-4">
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
        />
        I own this system or have written authorization to scan it.
      </label>

      <button className="bg-blue-600 text-white px-4 py-2 rounded">
        Start Scan
      </button>

      {message && <p className="text-red-600">{message}</p>}
    </form>
  );
}