import { useEffect, useState } from "react";
import axios from "axios";

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


  const fetchDevices = () => {
    axios.get("http://127.0.0.1:8000/devices?tenant_id=1")
      .then((res) => {
        setDevices(res.data);
      })
      .catch((err) => {
        console.error("Error fetching devices:", err);
      });
  };


  useEffect(() => {
    fetchDevices();
  }, []);


  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };


  const addDevice = () => {

    const payload = {
      tenant_id: 1,
      name: form.name,
      ip_address: form.ip_address,
      username: form.username,
      password: form.password,
      device_type: form.device_type,
      location: form.location
    };

    console.log("Sending device:", payload);

    axios
      .post("http://127.0.0.1:8000/devices", payload)
      .then(() => {

        fetchDevices();

        setForm({
          name: "",
          ip_address: "",
          username: "",
          password: "",
          device_type: "",
          location: ""
        });

      })
      .catch((err) => {
        console.error("Error creating device:", err);
      });
  };


  return (
    <div className="text-white">

      <h1 className="text-4xl font-bold mb-6">
        Devices
      </h1>


      {/* Add Device Form */}

      <div className="bg-gray-800 p-6 rounded-lg mb-8 max-w-4xl">

        <h2 className="text-xl mb-4">
          Add Device
        </h2>

        <div className="grid grid-cols-2 gap-4">

          <input
            name="name"
            placeholder="Device Name"
            value={form.name}
            onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded"
          />

          <input
            name="ip_address"
            placeholder="IP Address"
            value={form.ip_address}
            onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded"
          />

          <input
            name="username"
            placeholder="Username"
            value={form.username}
            onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded"
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded"
          />

          <input
            name="device_type"
            placeholder="Device Type"
            value={form.device_type}
            onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded"
          />

          <input
            name="location"
            placeholder="Location"
            value={form.location}
            onChange={handleChange}
            className="p-2 bg-gray-700 text-white rounded"
          />

        </div>

        <button
          onClick={addDevice}
          className="mt-5 bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded"
        >
          Add Device
        </button>

      </div>


      {/* Devices Table */}

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

          {devices.map((device) => (

            <tr
              key={device.id}
              className="border-t border-gray-700 hover:bg-gray-700"
            >

              <td className="p-3">
                {device.name}
              </td>

              <td className="p-3">
                {device.ip_address}
              </td>

              <td className="p-3">
                {device.status === "online"
                  ? <span className="text-green-400">● Online</span>
                  : <span className="text-red-400">● Offline</span>
                }
              </td>

              <td className="p-3">
                {device.location}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}