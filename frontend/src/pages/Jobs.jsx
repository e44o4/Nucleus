import { useEffect, useState } from "react";
import axios from "axios";
import { API } from "../config";

export default function Jobs() {

  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedJob, setSelectedJob] = useState(null);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${API}/jobs`);
      setJobs(res.data);
    } catch (err) {
      console.error("Failed to fetch jobs", err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusStyle = (status) => {
    if (status === "success") return "bg-green-600 text-white";
    if (status === "failed")  return "bg-red-600 text-white";
    if (status === "running") return "bg-yellow-500 text-black";
    return "bg-gray-600 text-white";
  };

  const formatDate = (dateStr) => {
    if (!dateStr) return "—";
    const d = new Date(dateStr);
    return d.toLocaleString();
  };

  return (
    <div>

      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-3xl font-bold">Job History</h1>
        <button
          onClick={fetchJobs}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
        >
          Refresh
        </button>
      </div>

      {/* Loading */}
      {loading && (
        <p className="text-gray-400">Loading jobs...</p>
      )}

      {/* Empty state */}
      {!loading && jobs.length === 0 && (
        <div className="bg-gray-800 rounded p-8 text-center text-gray-400">
          No jobs found. Run a command from the Devices page to see history here.
        </div>
      )}

      {/* Jobs Table */}
      {!loading && jobs.length > 0 && (
        <div className="bg-gray-800 rounded overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-700 text-gray-300 text-left">
                <th className="p-4">#</th>
                <th className="p-4">Command</th>
                <th className="p-4">Status</th>
                <th className="p-4">Time</th>
                <th className="p-4">Output</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map((job) => (
                <tr
                  key={job.id}
                  className="border-t border-gray-700 hover:bg-gray-750"
                >
                  <td className="p-4 text-gray-400">{job.id}</td>
                  <td className="p-4 font-mono text-blue-300">{job.command}</td>
                  <td className="p-4">
                    <span className={`px-2 py-1 rounded text-xs font-bold ${getStatusStyle(job.status)}`}>
                      {job.status.toUpperCase()}
                    </span>
                  </td>
                  <td className="p-4 text-gray-400 text-xs">{formatDate(job.created_at)}</td>
                  <td className="p-4">
                    {job.results ? (
                      <button
                        onClick={() => setSelectedJob(job)}
                        className="text-blue-400 hover:text-blue-300 underline text-xs"
                      >
                        View Output
                      </button>
                    ) : (
                      <span className="text-gray-500 text-xs">—</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Output Modal */}
      {selectedJob && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg w-2/3 max-h-96 flex flex-col">

            {/* Modal Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
              <div>
                <span className="font-bold text-white">Job #{selectedJob.id}</span>
                <span className="ml-3 font-mono text-blue-300 text-sm">{selectedJob.command}</span>
              </div>
              <button
                onClick={() => setSelectedJob(null)}
                className="text-gray-400 hover:text-white text-xl font-bold"
              >
                ✕
              </button>
            </div>

            {/* Modal Output */}
            <div className="p-4 overflow-auto flex-1">
              <pre className="text-green-400 text-xs font-mono whitespace-pre-wrap">
                {selectedJob.results}
              </pre>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}