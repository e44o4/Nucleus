import { BrowserRouter, Routes, Route, Link, useLocation } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Devices from "./pages/Devices";
import Jobs from "./pages/Jobs";

function Sidebar() {
  const location = useLocation();

  const linkClass = (path) => {
    const active = location.pathname === path;
    return `p-2 rounded transition ${active ? "bg-blue-600 text-white" : "hover:bg-gray-700 text-gray-300"}`;
  };

  return (
    <div className="w-60 bg-gray-800 p-6 flex flex-col">

      <h1 className="text-2xl font-bold mb-10 text-white">
        Nucleus
      </h1>

      <nav className="flex flex-col gap-2">

        <Link to="/" className={linkClass("/")}>
          Dashboard
        </Link>

        <Link to="/devices" className={linkClass("/devices")}>
          Devices
        </Link>

        <Link to="/jobs" className={linkClass("/jobs")}>
          Job History
        </Link>

      </nav>

    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-gray-900 text-white">

        {/* Sidebar */}
        <Sidebar />

        {/* Main Content */}
        <div className="flex-1 p-8">
          <Routes>
            <Route path="/"        element={<Dashboard />} />
            <Route path="/devices" element={<Devices />} />
            <Route path="/jobs"    element={<Jobs />} />
          </Routes>
        </div>

      </div>
    </BrowserRouter>
  );
}