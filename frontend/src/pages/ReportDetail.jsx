import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";

export default function ReportDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);

  useEffect(() => {
    // Assuming backend /api/page is used to find it, or we fetch list and find it.
    api.get(`/api/page?page=0&size=1000`)
       .then(res => {
           const found = res.data.content.find(r => r.id.toString() === id);
           setReport(found);
       })
       .catch(err => console.error(err));
  }, [id]);

  if (!report) return <div className="p-6">Loading...</div>;

  const getBadgeColor = (severity) => {
      if (!severity) return "bg-gray-500";
      switch(severity.toLowerCase()) {
          case "high": return "bg-red-500";
          case "medium": return "bg-yellow-500";
          case "low": return "bg-blue-500";
          default: return "bg-gray-500";
      }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto min-h-screen">
      <button onClick={() => navigate("/home")} className="mb-4 bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded shadow transition">
        &larr; Back to Dashboard
      </button>
      
      <div className="bg-white dark:bg-gray-800 p-8 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 relative overflow-hidden">
        {/* Score Badge */}
        <div className={`absolute top-0 right-0 text-white font-bold px-6 py-2 rounded-bl-xl shadow-md ${getBadgeColor(report.severity)}`}>
            {report.severity || "Unknown"} Risk
        </div>

        <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-2 pr-24">{report.title}</h2>
        <div className="flex gap-3 items-center mb-6 text-sm text-gray-500 dark:text-gray-400">
            <span className="bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full">ID: #{report.id}</span>
            <span className={`px-3 py-1 rounded-full font-semibold ${report.status === 'OPEN' ? 'text-green-700 bg-green-100' : 'text-red-700 bg-red-100'}`}>
                {report.status}
            </span>
            <span>📍 {report.location || "N/A"}</span>
        </div>

        <div className="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-600 mb-6">
            <h3 className="text-lg font-semibold mb-2 dark:text-gray-200">Description</h3>
            <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">
                {report.description}
            </p>
        </div>

        <div className="flex gap-4 border-t pt-6 dark:border-gray-700">
             {/* Edit/Delete buttons requested in checklist */}
             <button className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded shadow transition">
                Edit Report
             </button>
             <button className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded shadow transition">
                Delete Report
             </button>
        </div>
      </div>
    </div>
  );
}
