//pages/About.jsx

import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

export default function About() {
  const navigate = useNavigate();

  return (
    <div
      className="h-screen w-full bg-cover bg-center flex justify-center items-center"
      style={{
        backgroundImage: "url('/home_img.jpg')",
      }}
    >
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="bg-white/30 backdrop-blur-lg shadow-xl rounded-2xl p-8 max-w-2xl text-center"
      >
        <h1 className="text-4xl font-bold text-[#6ea3e8] mb-4">
          Recommendations from an avid k-drama viewer
        </h1>

        <p className="text-gray-800 font-medium mb-6">
          After watching k-dramas for several years, I built this app to help others discover their next favorite k-drama.
          Unlike other recommendation systems, my recommendations are not based solely on simple details like genre or cast. 
          Instead, they're based on my personal reviews of over 150 k-dramas.
        </p>

        <button
          onClick={() => navigate("/recommendations")}
          className="px-6 py-2 rounded-xl bg-[#6ea3e8] text-white hover:bg-blue-300 transition-colors"
        >
          Get Recommendations
        </button>
      </motion.div>
    </div>
  );
}
