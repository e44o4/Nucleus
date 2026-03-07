export default function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-10">

      <h1 className="text-5xl font-bold mb-10">
        Nucleus Network Automation Platform
      </h1>

      <div className="grid grid-cols-4 gap-6">

        <div className="bg-gray-800 p-6 rounded-xl">
          <h2 className="text-lg">Total Devices</h2>
          <p className="text-3xl font-bold">0</p>
        </div>

        <div className="bg-green-800 p-6 rounded-xl">
          <h2 className="text-lg">Online</h2>
          <p className="text-3xl font-bold">0</p>
        </div>

        <div className="bg-red-800 p-6 rounded-xl">
          <h2 className="text-lg">Offline</h2>
          <p className="text-3xl font-bold">0</p>
        </div>

        <div className="bg-yellow-700 p-6 rounded-xl">
          <h2 className="text-lg">Alerts</h2>
          <p className="text-3xl font-bold">0</p>
        </div>

      </div>

    </div>
  )
}