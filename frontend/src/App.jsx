import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import NewScan from "./pages/NewScan";
import ScanDetails from "./pages/ScanDetails";

export default function App() {
  return (
    <BrowserRouter>
      <nav className="p-4 bg-gray-900 text-white flex gap-6">
        <a href="/">Dashboard</a>
        <a href="/new-scan">New Scan</a>
      </nav>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/new-scan" element={<NewScan />} />
        <Route path="/scans/:id" element={<ScanDetails />} />
      </Routes>
    </BrowserRouter>
  );
}