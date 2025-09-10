import React, { useState } from "react";
import axios from "axios";

type ResultType = {
  query: string;
  result: string;
  ppt_file: string;
  pdf_file: string;
  retrieved_docs: string[];
};

export default function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<ResultType | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post<ResultType>(
        "http://127.0.0.1:8000/generate?model=gpt-5&use_knowledge=true",
        { query }
      );
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Error fetching response");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-3xl mx-auto bg-white shadow-xl rounded-2xl p-6 space-y-6">
        <h1 className="text-3xl font-bold text-gray-800 text-center">
          Finnancial Agent –  Here to guide you in finance domain 
        </h1>

        <form onSubmit={handleSubmit} className="flex gap-4">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about finance, investments, planning..."
            className="flex-1 border rounded-xl px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Thinking..." : "Ask"}
          </button>
        </form>

        {result && (
          <div className="space-y-4">
            <div className="p-4 bg-gray-50 rounded-xl border">
              <h2 className="font-semibold text-gray-700 mb-2">💡 Answer:</h2>
              <p className="text-gray-800 whitespace-pre-line">{result?.result}</p>
            </div>

            <div className="flex gap-4">
              <a
                href={`http://127.0.0.1:8000/${result?.ppt_file}`}
                className="bg-green-600 text-white px-4 py-2 rounded-xl hover:bg-green-700"
                download
              >
                ⬇ Download PPT
              </a>
              <a
                href={`http://127.0.0.1:8000/${result?.pdf_file}`}
                className="bg-red-600 text-white px-4 py-2 rounded-xl hover:bg-red-700"
                download
              >
                ⬇ Download PDF
              </a>
            </div>

            <div className="p-4 bg-gray-50 rounded-xl border">
              <h2 className="font-semibold text-gray-700 mb-2"> Sources:</h2>
              <ul className="list-disc pl-6 text-gray-600 space-y-1">
                {result?.retrieved_docs.map((doc, idx) => (
                  <li key={idx}>{doc.slice(0, 120)}...</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
