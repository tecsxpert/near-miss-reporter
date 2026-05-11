import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
  PieChart, Pie, Legend, LineChart, Line, CartesianGrid
} from "recharts";
import { FaArrowLeft } from "react-icons/fa";

export default function Analytics() {
  const navigate = useNavigate();
  const [reports, setReports] = useState([]);
  const [period, setPeriod] = useState("ALL"); // ALL, 7D, 30D

  useEffect(() => {
    // Fetching up to 1000 reports for analytics
    api.get(`/api/page?page=0&size=1000`)
      .then(res => setReports(res.data.content))
      .catch(err => console.error(err));
  }, []);

  // Filter by period
  const filteredReports = reports.filter(r => {
    if (period === "ALL") return true;
    const rDate = new Date(r.createdAt || new Date());
    const now = new Date();
    const diffDays = (now - rDate) / (1000 * 60 * 60 * 24);
    if (period === "7D") return diffDays <= 7;
    if (period === "30D") return diffDays <= 30;
    return true;
  });

  // Data for Status Chart
  const statusData = [
    { name: "OPEN", value: filteredReports.filter(r => r.status === "OPEN").length, fill: "#22c55e" },
    { name: "CLOSED", value: filteredReports.filter(r => r.status === "CLOSED").length, fill: "#ef4444" },
  ];

  // Data for Severity Chart
  const severityData = [
    { name: "High", value: filteredReports.filter(r => r?.severity?.toLowerCase() === "high").length, fill: "#ef4444" },
    { name: "Medium", value: filteredReports.filter(r => r?.severity?.toLowerCase() === "medium").length, fill: "#eab308" },
    { name: "Low", value: filteredReports.filter(r => r?.severity?.toLowerCase() === "low").length, fill: "#3b82f6" },
  ].filter(d => d.value > 0);

  // Data for Trend Chart (Reports per day)
  const trendMap = {};
  filteredReports.forEach(r => {
    const date = new Date(r.createdAt || new Date()).toISOString().split('T')[0];
    trendMap[date] = (trendMap[date] || 0) + 1;
  });
  const trendData = Object.keys(trendMap).sort().map(date => ({ date, count: trendMap[date] }));

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
          <button 
            onClick={() => navigate("/home")} 
            className="flex items-center gap-2 bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
          >
            <FaArrowLeft /> <span className="hidden md:inline">Back</span>
          </button>
          <h2 className="text-xl md:text-3xl font-bold text-center">Analytics Dashboard</h2>
          <select 
            className="border p-2 rounded dark:bg-gray-700 dark:text-white dark:border-gray-600"
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
          >
            <option value="ALL">All Time</option>
            <option value="30D">Last 30 Days</option>
            <option value="7D">Last 7 Days</option>
          </select>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Status Chart */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded shadow">
            <h3 className="text-xl font-semibold mb-4 text-center">Reports by Status</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={statusData}>
                <XAxis dataKey="name" stroke="#8884d8" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" radius={[5, 5, 0, 0]}>
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Severity Chart */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded shadow">
            <h3 className="text-xl font-semibold mb-4 text-center">Reports by Severity</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie 
                  data={severityData.length > 0 ? severityData : [{ name: "No Data", value: 1, fill: "#ccc" }]} 
                  dataKey="value" 
                  nameKey="name" 
                  cx="50%" 
                  cy="50%" 
                  outerRadius={100} 
                  label
                  isAnimationActive={false}
                >
                  {severityData.length > 0 ? severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  )) : <Cell fill="#ccc" />}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Trend Chart */}
          <div className="bg-white dark:bg-gray-800 p-6 rounded shadow md:col-span-2">
            <h3 className="text-xl font-semibold mb-4 text-center">Reporting Trend (Over Time)</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis dataKey="date" stroke="#8884d8" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="count" stroke="#8b5cf6" strokeWidth={3} activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
