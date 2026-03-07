import { useEffect, useState } from "react";
import axios from "axios";

export default function App() {

  const [summary, setSummary] = useState({
    total_devices: 0,
    online_devices: 0,
    offline_devices: 0,
    alerts: 0
  });

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/dashboard/summary")
      .then(res => {
        setSummary(res.data);
      })
      .catch(err => {
        console.error(err);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white p-10">

      <h1 className="text-5xl font-bold mb-10">
        Nucleus Network Automation Platform
      </h1>

      <div className="grid grid-cols-4 gap-6">

        <div className="bg-gray-800 p-6 rounded-xl shadow-lg">
          <h2 className="text-lg text-gray-400">Total Devices</h2>
          <p className="text-3xl font-bold">{summary.total_devices}</p>
        </div>

        <div className="bg-green-700 p-6 rounded-xl shadow-lg">
          <h2 className="text-lg">Online</h2>
          <p className="text-3xl font-bold">{summary.online_devices}</p>
        </div>

        <div className="bg-red-700 p-6 rounded-xl shadow-lg">
          <h2 className="text-lg">Offline</h2>
          <p className="text-3xl font-bold">{summary.offline_devices}</p>
        </div>

        <div className="bg-yellow-600 p-6 rounded-xl shadow-lg">
          <h2 className="text-lg">Alerts</h2>
          <p className="text-3xl font-bold">{summary.alerts}</p>
        </div>

      </div>

    </div>
  );
}