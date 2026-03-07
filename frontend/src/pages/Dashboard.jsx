import { useEffect, useState } from "react";
import axios from "axios";

export default function Dashboard() {

  const [summary, setSummary] = useState({
    total_devices: 0,
    online_devices: 0,
    offline_devices: 0,
    alerts: 0
  });

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/dashboard/summary")
      .then((res) => {
        setSummary(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  return (
    <div>

      <h1 className="text-4xl font-bold mb-8">
        Dashboard
      </h1>

      <div className="grid grid-cols-4 gap-6">

        <div className="bg-gray-800 p-6 rounded-xl">
          <h2 className="text-gray-400 text-sm">
            Total Devices
          </h2>

          <p className="text-3xl font-bold">
            {summary.total_devices}
          </p>
        </div>

        <div className="bg-green-700 p-6 rounded-xl">
          <h2 className="text-sm">
            Online Devices
          </h2>

          <p className="text-3xl font-bold">
            {summary.online_devices}
          </p>
        </div>

        <div className="bg-red-700 p-6 rounded-xl">
          <h2 className="text-sm">
            Offline Devices
          </h2>

          <p className="text-3xl font-bold">
            {summary.offline_devices}
          </p>
        </div>

        <div className="bg-yellow-600 p-6 rounded-xl">
          <h2 className="text-sm">
            Alerts
          </h2>

          <p className="text-3xl font-bold">
            {summary.alerts}
          </p>
        </div>

      </div>

    </div>
  );
}