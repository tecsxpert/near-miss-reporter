import { useEffect, useState, useContext } from "react";
import api from "../services/api";
import toast from "react-hot-toast";
import { FaHome, FaPlus, FaSignOutAlt, FaChartBar, FaRobot, FaEye } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../components/AuthContext";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

export default function Home() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("OPEN");
  const [editId, setEditId] = useState(null);

  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [filter, setFilter] = useState("ALL");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const [page, setPage] = useState(0);
  const [totalPages, setTotalPages] = useState(0);

  const [dark, setDark] = useState(false);
  const [aiInsight, setAiInsight] = useState("");
  const [aiLoading, setAiLoading] = useState(false);

  const navigate = useNavigate();
  const { user, logout } = useContext(AuthContext);
  const size = 5;

  // 🔹 Debounce search
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearch(search);
      setPage(0);
    }, 500);
    return () => clearTimeout(handler);
  }, [search]);

  // 🔹 Load dark mode from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("dark");
    if (saved === "true") {
      document.documentElement.classList.add("dark");
      setDark(true);
    }
  }, []);

  // 🔹 Toggle dark mode (global)
  const toggleDark = () => {
    const isDark = !dark;
    setDark(isDark);
    localStorage.setItem("dark", isDark);
    document.documentElement.classList.toggle("dark", isDark);
  };

  // 🔹 Fetch reports
  const fetchReports = () => {
    setLoading(true);
    const url = debouncedSearch.trim() !== "" 
        ? `/api/search?q=${debouncedSearch}&page=${page}&size=${size}` 
        : `/api/page?page=${page}&size=${size}`;
        
    api.get(url)
      .then((res) => {
        setReports(res.data.content);
        setTotalPages(res.data.totalPages);
      })
      .catch(() => toast.error("Failed to load data"))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchReports();
  }, [page, debouncedSearch]);

  // 🔹 Add / Update
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title || !description) return;

    if (editId) {
      api
        .put(`/api/update/${editId}`, { title, description, status })
        .then(() => {
          toast.success("Report updated");
          resetForm();
          fetchReports();
        })
        .catch((err) => {
          console.error(err);
          toast.error("Failed to update report");
        });
    } else {
      api.post("/api/add", { title, description, status })
        .then(() => {
          toast.success("Report added");
          resetForm();
          fetchReports();
        })
        .catch((err) => {
          console.error(err);
          toast.error("Failed to add report");
        });
    }
  };

  const resetForm = () => {
    setTitle("");
    setDescription("");
    setStatus("OPEN");
    setEditId(null);
  };

  // 🔹 Delete
  const handleDelete = (id) => {
    api.delete(`/api/delete/${id}`)
      .then(() => {
        toast.success("Report deleted");
        fetchReports();
      })
      .catch((err) => {
        console.error(err);
        toast.error("Failed to delete report");
      });
  };

  // 🔹 Upload CSV
  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    api.post("/api/upload", formData)
    .then((res) => {
      toast.success(res.data || "File uploaded successfully");
      fetchReports(); // Refresh the list
    })
    .catch((err) => {
      toast.error(err.response?.data || "Error uploading file");
    });
    
    // Reset file input
    e.target.value = null;
  };

  // 🔹 Edit
  const handleEdit = (r) => {
    setTitle(r.title);
    setDescription(r.description);
    setStatus(r.status);
    setEditId(r.id);
  };

  // 🔹 Filter (client-side for status and date)
  const filteredReports = reports.filter((r) => {
      const matchStatus = filter === "ALL" || r.status === filter;
      const rDate = new Date(r.createdAt || new Date());
      const matchStart = !startDate || rDate >= new Date(startDate);
      const matchEnd = !endDate || rDate <= new Date(endDate);
      return matchStatus && matchStart && matchEnd;
  });

  const fetchAIInsights = () => {
      setAiLoading(true);
      api.post("http://127.0.0.1:5000/api/recommend", { reports: reports })
        .then(res => setAiInsight(res.data.recommendation || res.data.message))
        .catch(() => setAiInsight("Failed to load AI insights. Is the Flask service running?"))
        .finally(() => setAiLoading(false));
  };

  // 🔹 Chart data (with colors)
  const chartData = [
    {
      name: "OPEN",
      value: reports.filter((r) => r.status === "OPEN").length,
      fill: "#22c55e",
    },
    {
      name: "CLOSED",
      value: reports.filter((r) => r.status === "CLOSED").length,
      fill: "#ef4444",
    },
  ];

  // 🔹 Loading spinner
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-100 dark:bg-gray-900">
        <div className="h-12 w-12 animate-spin rounded-full border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="flex flex-col md:flex-row min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      {/* 🔷 Sidebar */}
      <aside className="w-full md:w-60 bg-gray-900 text-white p-4 md:p-5 flex md:flex-col justify-between md:justify-start md:min-h-screen sticky top-0 z-10">
        <h2 className="text-xl font-bold mb-0 md:mb-6 hidden md:block">Dashboard</h2>

        <div className="flex md:flex-col gap-4 md:gap-0 w-full justify-around md:justify-start overflow-x-auto">
          <div className="flex flex-col md:flex-row items-center gap-1 md:gap-2 mb-0 md:mb-4 cursor-pointer hover:text-blue-400" onClick={() => navigate("/home")}>
            <FaHome className="text-xl md:text-base"/> <span className="text-xs md:text-base">Home</span>
          </div>

          <div className="flex flex-col md:flex-row items-center gap-1 md:gap-2 mb-0 md:mb-4 cursor-pointer hover:text-blue-400" onClick={() => window.scrollTo(0, document.body.scrollHeight)}>
            <FaPlus className="text-xl md:text-base"/> <span className="text-xs md:text-base">Add</span>
          </div>

          <div className="flex flex-col md:flex-row items-center gap-1 md:gap-2 mb-0 md:mb-4 cursor-pointer hover:text-blue-400" onClick={() => navigate("/analytics")}>
            <FaChartBar className="text-xl md:text-base"/> <span className="text-xs md:text-base">Analytics</span>
          </div>

          <button
            onClick={() => {
              logout();
              navigate("/");
            }}
            className="flex flex-col md:flex-row items-center gap-1 md:gap-2 mt-0 md:mt-10 bg-red-500 px-3 py-2 rounded hover:bg-red-600 text-xs md:text-base"
          >
            <FaSignOutAlt className="text-xl md:text-base"/> <span className="hidden md:inline">Logout</span>
          </button>
        </div>
      </aside>

      {/* 🔷 Main Content */}
      <main className="flex-1 p-4 md:p-6 w-full max-w-full overflow-hidden">
        {/* 🔷 Profile + Dark Toggle */}
        <div className="bg-white dark:bg-gray-800 p-4 rounded shadow mb-6 flex justify-between items-center">
          <div>
            <h2 className="font-semibold">👤 Welcome, {user}</h2>
            <p className="text-sm text-gray-500 dark:text-gray-300">
              Manage your reports efficiently
            </p>
          </div>

          <button
            onClick={toggleDark}
            className="bg-gray-700 text-white px-3 py-1 rounded"
          >
            {dark ? "☀️ Light" : "🌙 Dark"}
          </button>
        </div>

        {/* 🔷 KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
           <div className="p-4 bg-blue-100 dark:bg-blue-900 rounded shadow">
             <h3 className="text-gray-600 dark:text-gray-300">Total Reports</h3>
             <p className="text-2xl font-bold">{reports.length}</p>
           </div>
           <div className="p-4 bg-green-100 dark:bg-green-900 rounded shadow">
             <h3 className="text-gray-600 dark:text-gray-300">Open</h3>
             <p className="text-2xl font-bold">{reports.filter(r => r.status === 'OPEN').length}</p>
           </div>
           <div className="p-4 bg-red-100 dark:bg-red-900 rounded shadow">
             <h3 className="text-gray-600 dark:text-gray-300">Closed</h3>
             <p className="text-2xl font-bold">{reports.filter(r => r.status === 'CLOSED').length}</p>
           </div>
           <div className="p-4 bg-purple-100 dark:bg-purple-900 rounded shadow">
             <h3 className="text-gray-600 dark:text-gray-300">High Severity</h3>
             <p className="text-2xl font-bold">{reports.filter(r => r.severity === 'High').length}</p>
           </div>
        </div>

        {/* 🔷 AI Panel */}
        <div className="bg-indigo-50 dark:bg-indigo-900 p-4 rounded shadow mb-6 border border-indigo-200">
           <div className="flex justify-between items-center mb-2">
              <h2 className="font-semibold flex items-center gap-2"><FaRobot /> AI Insights</h2>
              <button onClick={fetchAIInsights} className="bg-indigo-500 text-white px-3 py-1 rounded text-sm hover:bg-indigo-600">
                 Analyze Current Page
              </button>
           </div>
           {aiLoading ? (
             <div className="flex gap-2 items-center text-indigo-500"><div className="h-4 w-4 animate-spin rounded-full border-b-2 border-indigo-500"></div> Generating insights...</div>
           ) : (
             <p className="text-sm whitespace-pre-wrap">{aiInsight || "Click 'Analyze' to get AI recommendations on these near-misses."}</p>
           )}
        </div>

        {/* 🔷 Analytics */}
        <div className="bg-white dark:bg-gray-800 p-4 rounded shadow mb-6">
          <h2 className="mb-3 font-semibold">📊 Analytics</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" stroke={dark ? "#fff" : "#000"} />
              <YAxis stroke={dark ? "#fff" : "#000"} />
              <Tooltip />
              <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={index} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* 🔷 Form */}
        <form
          onSubmit={handleSubmit}
          className="bg-white dark:bg-gray-800 p-6 rounded shadow mb-6"
        >
          <h3 className="font-semibold mb-3">
            {editId ? "Update Report" : "Add Report"}
          </h3>

          <input
            placeholder="Title"
            className="w-full border p-2 mb-2 rounded dark:bg-gray-700 dark:text-white"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <input
            placeholder="Description"
            className="w-full border p-2 mb-2 rounded dark:bg-gray-700 dark:text-white"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          <select
            className="w-full border p-2 mb-3 rounded dark:bg-gray-700 dark:text-white"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="OPEN">OPEN</option>
            <option value="CLOSED">CLOSED</option>
          </select>

          <button className="w-full bg-green-500 text-white py-2 rounded hover:bg-green-600">
            {editId ? "Update" : "Add"}
          </button>
        </form>

        {/* 🔷 Search + Filter */}
        <div className="flex flex-wrap gap-4 mb-4">
          <input
            placeholder="Search (debounced)..."
            className="flex-1 border p-2 rounded dark:bg-gray-700 dark:text-white min-w-[200px]"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          <select
            className="border p-2 rounded dark:bg-gray-700 dark:text-white"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
          >
            <option value="ALL">All Status</option>
            <option value="OPEN">Open</option>
            <option value="CLOSED">Closed</option>
          </select>
          
          <input 
             type="date" 
             className="border p-2 rounded dark:bg-gray-700 dark:text-white"
             value={startDate}
             onChange={(e) => setStartDate(e.target.value)}
          />
          <span className="self-center">to</span>
          <input 
             type="date" 
             className="border p-2 rounded dark:bg-gray-700 dark:text-white"
             value={endDate}
             onChange={(e) => setEndDate(e.target.value)}
          />
          
          {/* Upload CSV */}
          <div className="flex items-center gap-2 border p-2 rounded dark:bg-gray-700 dark:border-gray-600">
            <label htmlFor="csvUpload" className="cursor-pointer text-sm font-semibold dark:text-white hover:text-blue-500">
              📥 Import CSV
            </label>
            <input
              id="csvUpload"
              type="file"
              accept=".csv"
              className="hidden"
              onChange={handleFileUpload}
            />
          </div>
        </div>

        {/* 🔷 Table */}
        <div className="bg-white dark:bg-gray-800 rounded shadow overflow-x-auto">
          <table className="w-full text-center whitespace-nowrap md:whitespace-normal">
            <thead className="bg-gray-800 text-white">
              <tr>
                <th className="p-2">S.No</th>
                <th className="p-2">Title</th>
                <th className="p-2">Description</th>
                <th className="p-2">Status</th>
                <th className="p-2">Actions</th>
              </tr>
            </thead>

            <tbody>
              {filteredReports.map((r, i) => (
                <tr key={r.id} className="border-b">
                  <td className="p-2">{page * size + i + 1}</td>
                  <td>{r.title}</td>
                  <td>{r.description}</td>
                  <td>{r.status}</td>

                  <td className="p-2">
                    <button
                      onClick={() => navigate(`/report/${r.id}`)}
                      className="bg-gray-500 text-white px-2 py-1 mr-2 rounded hover:bg-gray-600"
                    >
                       <FaEye />
                    </button>

                    <button
                      onClick={() => handleEdit(r)}
                      className="bg-blue-500 text-white px-2 py-1 mr-2 rounded hover:bg-blue-600"
                    >
                      Edit
                    </button>

                    <button
                      onClick={() => handleDelete(r.id)}
                      className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}

              {filteredReports.length === 0 && (
                <tr>
                  <td colSpan="5" className="p-4">
                    No data found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* 🔷 Pagination */}
        <div className="flex justify-center gap-4 mt-4">
          <button
            onClick={() => setPage((p) => p - 1)}
            disabled={page === 0}
            className="px-3 py-1 rounded bg-gray-300 dark:bg-gray-700 disabled:opacity-50"
          >
            Prev
          </button>

          <span className="px-2">
            Page {page + 1} / {totalPages}
          </span>

          <button
            onClick={() => setPage((p) => p + 1)}
            disabled={page + 1 >= totalPages}
            className="px-3 py-1 rounded bg-gray-300 dark:bg-gray-700 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </main>
    </div>
  );
}