import { useEffect, useState } from "react";
import axios from "axios";

export default function Devices() {

  const [devices, setDevices] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/devices")
      .then(res => {
        setDevices(res.data);
      });
  }, []);

  return (
    <div className="p-10 text-white bg-gray-900 min-h-screen">

      <h1 className="text-4xl font-bold mb-6">Devices</h1>

      <table className="w-full bg-gray-800 rounded-lg overflow-hidden">

        <thead className="bg-gray-700">
          <tr>
            <th className="p-3 text-left">Name</th>
            <th className="p-3 text-left">IP</th>
            <th className="p-3 text-left">Status</th>
            <th className="p-3 text-left">Location</th>
          </tr>
        </thead>

        <tbody>
          {devices.map(device => (
            <tr key={device.id} className="border-t border-gray-700">

              <td className="p-3">{device.name}</td>
              <td className="p-3">{device.ip_address}</td>

              <td className="p-3">
                {device.status === "online" ?
                  <span className="text-green-400">● Online</span> :
                  <span className="text-red-400">● Offline</span>
                }
              </td>

              <td className="p-3">{device.location}</td>

            </tr>
          ))}
        </tbody>

      </table>

    </div>
  );
}