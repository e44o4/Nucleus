import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Devices from "./pages/Devices";

export default function App() {
  return (
    <BrowserRouter>

      <div className="flex min-h-screen bg-gray-900 text-white">

        {/* Sidebar */}
        <div className="w-60 bg-gray-800 p-6">

          <h1 className="text-2xl font-bold mb-10">
            Nucleus
          </h1>

          <nav className="flex flex-col gap-4">

            <Link
              to="/"
              className="hover:bg-gray-700 p-2 rounded"
            >
              Dashboard
            </Link>

            <Link
              to="/devices"
              className="hover:bg-gray-700 p-2 rounded"
            >
              Devices
            </Link>

          </nav>

        </div>

        {/* Main Content */}
        <div className="flex-1 p-8">

          <Routes>

            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/devices"
              element={<Devices />}
            />

          </Routes>

        </div>

      </div>

    </BrowserRouter>
  );
}