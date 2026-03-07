import { useEffect, useState } from "react";
import axios from "axios";
import { API, TENANT_ID } from "../config";

export default function Devices() {

  const [devices, setDevices] = useState([]);
  const [form, setForm] = useState({
    name: "",
    ip_address: "",
    username: "",
    password: "",
    device_type: "",
    location: ""
  });

  // Command modal state
  const [commandModal, setCommandModal] = useState(false);
  const [commandInput, setCommandInput] = useState("");
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [commandResult, setCommandResult] = useState(null);
  const [commandLoading, setCommandLoading] = useState(false);


  const fetchDevices = () => {
    axios
      .get(`${API}/devices?tenant_id=${TENANT_ID}`)
      .then(res => setDevices(res.data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    fetchDevices();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };


  // ── Add Device ────────────────────────────────────────────────
  const addDevice = () => {

    if (!form.name || !form.ip_address || !form.username || !form.password) {
      alert("Please fill in Name, IP, Username and Password");
      return;
    }

    axios.post(`${API}/devices`, {
      tenant_id: TENANT_ID,
      name: form.name,
      ip_address: form.ip_address,
      username: form.username,
      password: form.password,
      device_type: form.device_type,
      location: form.location
    })
    .then(() => {
      fetchDevices();
      setForm({ name: "", ip_address: "", username: "", password: "", device_type: "", location: "" });
    })
    .catch(err => {
      console.error(err);
      alert("Failed to add device");
    });
  };


  // ── Open Run Command Modal ────────────────────────────────────
  const openCommandModal = (device) => {
    setSelectedDevice(device);
    setCommandInput("");
    setCommandResult(null);
    setCommandModal(true);
  };


  // ── Run Command ───────────────────────────────────────────────
  const runCommand = () => {

    if (!commandInput.trim()) {
      alert("Please enter a command");
      return;
    }

    setCommandLoading(true);
    setCommandResult(null);

    // ✅ Fixed: use device_ids (array) and correct endpoint
    axios.post(`${API}/devices/${selectedDevice.id}/run-command`, {
      command: commandInput
    })
    .then(res => {
      setCommandResult({ success: true, output: res.data.output || JSON.stringify(res.data) });
    })
    .catch(err => {
      const errorMsg = err.response?.data?.detail || err.message || "Command failed";
      setCommandResult({ success: false, output: errorMsg });
    })
    .finally(() => {
      setCommandLoading(false);
    });
  };


  // ── Push Config ───────────────────────────────────────────────
  const pushConfig = (deviceId) => {

    const configCommand = prompt("Enter config command to push:", "/system identity set name=Nucleus");

    if (!configCommand) return;

    // ✅ Fixed: use device_ids (array)
    axios.post(`${API}/config/push`, {
      device_ids: [deviceId],
      commands: [configCommand]
    })
    .then(res => {
      const result = res.data.results?.[0];
      if (result?.status === "success") {
        alert(`✅ Config pushed successfully!\n\n${result.output}`);
      } else {
        alert(`❌ Config push failed:\n\n${result?.error || "Unknown error"}`);
      }
    })
    .catch(err => {
      console.error(err);
      alert("Config push failed");
    });
  };


  // ── Delete Device ─────────────────────────────────────────────
  const deleteDevice = (deviceId) => {

    if (!confirm("Are you sure you want to delete this device?")) return;

    // ✅ Fixed: include tenant_id in query
    axios.delete(`${API}/devices/${deviceId}?tenant_id=${TENANT_ID}`)
    .then(() => {
      fetchDevices();
    })
    .catch(err => {
      console.error(err);
      alert("Failed to delete device");
    });
  };


  return (
    <div className="text-white">

      <h1 className="text-4xl font-bold mb-6">Devices</h1>

      {/* ── Add Device Form ── */}
      <div className="bg-gray-800 p-6 rounded-lg mb-8 max-w-4xl">

        <h2 className="text-xl mb-4">Add Device</h2>

        <div className="grid grid-cols-2 gap-4">
          <input name="name" placeholder="Device Name" value={form.name} onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded" />
          <input name="ip_address" placeholder="IP Address" value={form.ip_address} onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded" />
          <input name="username" placeholder="Username" value={form.username} onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded" />
          <input type="password" name="password" placeholder="Password" value={form.password} onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded" />
          <input name="device_type" placeholder="Device Type" value={form.device_type} onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded" />
          <input name="location" placeholder="Location" value={form.location} onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded" />
        </div>

        <button onClick={addDevice}
          className="mt-5 bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded">
          Add Device
        </button>

      </div>

      {/* ── Devices Table ── */}
      <table className="w-full bg-gray-800 rounded-lg overflow-hidden">

        <thead className="bg-gray-700">
          <tr>
            <th className="p-3 text-left">Name</th>
            <th className="p-3 text-left">IP</th>
            <th className="p-3 text-left">Status</th>
            <th className="p-3 text-left">Location</th>
            <th className="p-3 text-left">Actions</th>
          </tr>
        </thead>

        <tbody>
          {devices.map(device => (
            <tr key={device.id} className="border-t border-gray-700 hover:bg-gray-700">

              <td className="p-3">{device.name}</td>
              <td className="p-3">{device.ip_address}</td>

              <td className="p-3">
                {device.status === "online"
                  ? <span className="text-green-400">● Online</span>
                  : <span className="text-red-400">● Offline</span>
                }
              </td>

              <td className="p-3">{device.location}</td>

              <td className="p-3 space-x-2">
                <button onClick={() => openCommandModal(device)}
                  className="bg-blue-600 hover:bg-blue-700 px-3 py-1 rounded">
                  Run
                </button>
                <button onClick={() => pushConfig(device.id)}
                  className="bg-yellow-600 hover:bg-yellow-700 px-3 py-1 rounded">
                  Config
                </button>
                <button onClick={() => deleteDevice(device.id)}
                  className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded">
                  Delete
                </button>
              </td>

            </tr>
          ))}
        </tbody>

      </table>

      {/* ── Run Command Modal ── */}
      {commandModal && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg w-2/3 flex flex-col">

            {/* Modal Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
              <div>
                <span className="font-bold text-white">Run Command</span>
                <span className="ml-3 text-blue-300 text-sm">{selectedDevice?.name} ({selectedDevice?.ip_address})</span>
              </div>
              <button onClick={() => setCommandModal(false)}
                className="text-gray-400 hover:text-white text-xl font-bold">✕</button>
            </div>

            {/* Command Input */}
            <div className="p-4 flex gap-2">
              <input
                value={commandInput}
                onChange={(e) => setCommandInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && runCommand()}
                placeholder="e.g. /system identity print"
                className="flex-1 p-2 bg-gray-700 text-white rounded font-mono"
              />
              <button onClick={runCommand} disabled={commandLoading}
                className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded disabled:opacity-50">
                {commandLoading ? "Running..." : "Run"}
              </button>
            </div>

            {/* Command Output */}
            {commandResult && (
              <div className="p-4 pt-0">
                <div className={`rounded p-3 ${commandResult.success ? "bg-gray-900" : "bg-red-900"}`}>
                  <pre className="text-green-400 text-xs font-mono whitespace-pre-wrap">
                    {commandResult.output}
                  </pre>
                </div>
              </div>
            )}

          </div>
        </div>
      )}

    </div>
  );
}