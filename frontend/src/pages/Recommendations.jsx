// pages/Recommendations.jsx

import { useEffect, useState } from "react";
import axios from "axios";
import Card from "../components/Card";
import Select from "react-select";

function App() {
  const [titles, setTitles] = useState([]);
  const [selectedTitle, setSelectedTitle] = useState(null);
  const [numRecs, setNumRecs] = useState(null); // Keep number of recs as null initially. Can change this to 3 (or any number) instead
  const [recommendations, setRecommendations] = useState([]);

  //const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8080";
  const API_URL = process.env.REACT_APP_API_URL || "https://kdramarama-backend-a44a9cb5e8b4.herokuapp.com";

  useEffect(() => {
    axios.get(`${API_URL}/titles`)
      .then((res) => {
        setTitles(res.data.map((t) => ({ value: t, label: t })));
      })
      .catch((error) => {
        console.error("Error fetching titles:", error);
      });
  }, [API_URL]);

  const handleRecommend = async () => {
    if (!selectedTitle || !numRecs) return;
    
    try {
      const res = await axios.post(`${API_URL}/recommendations`, {
        title: selectedTitle.value,
        n: numRecs,
      });
      setRecommendations(res.data);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }
  };

  return (
    <div
      className="w-full bg-cover bg-center min-h-screen bg-gray-50 p-6"
      style={{
        backgroundImage: "url('/home_img2.jpg')",
      }}
    >
      <h1 className="text-4xl font-bold text-center text-[#6ea3e8] mb-4 pt-[6vh]">
        Find your next favorite k-drama.
      </h1>
      <p className="text-center text-gray-700 mb-8">
        Select a k-drama that you have watched and enjoyed from the list below and get recommendations.
      </p>

      {/* Kdrama title dropdown */}
      <div className="flex justify-center gap-4 mb-6 flex-wrap">
        <div className="min-w-[250px]">
          <Select
            options={titles}
            value={selectedTitle}
            onChange={setSelectedTitle}
            placeholder="Search or select a k-drama"
            isClearable
            styles={{
              control: (provided) => ({
                ...provided,
                borderRadius: "0.75rem", // rounded-xl
              }),
            }}
          />
        </div>

        {/* Num recommendations dropdown */}
        <div className="min-w-[250px]">
          <Select
            options={[1, 2, 3, 4, 5].map((n) => ({
              value: n,
              label: `${n} ${n === 1 ? "recommendation" : "recommendations"}`,
            }))}
            value={numRecs ? { value: numRecs, label: `${numRecs} ${numRecs === 1 ? "recommendation" : "recommendations"}` } : null}
            onChange={(selected) => setNumRecs(selected?.value)}
            placeholder="Select number of recommendations"
            isClearable
            styles={{
              control: (provided) => ({
                ...provided,
                borderRadius: "0.75rem", // rounded-xl
              }),
            }}
          />
        </div>

        {/* Get recommendations button */}
        <button
          className="bg-[#6ea3e8] hover:bg-blue-200 text-white px-4 py-2 rounded-xl"
          onClick={handleRecommend}
        >
          Get Recommendations
        </button>
      </div>

      {/* Grid layout with card components */}
      <div className="flex flex-wrap justify-center gap-10">
        {recommendations.slice(0, 5).map((rec) => (
          <Card key={rec.title} drama={rec} />
        ))}
      </div>
    </div>
  );
}

export default App;
