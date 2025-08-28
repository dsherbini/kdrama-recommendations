//pages/Home.jsx

import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div
      className="h-screen w-full bg-cover bg-center flex flex-col justify-center items-center text-[#6ea3e8] font-bold pt-[30vh]"
      style={{
        backgroundImage: "url('/home_img.jpg')",
      }}
    >
      <h1 className="text-5xl md:text-6xl font-bold mb-12 text-center drop-shadow-lg">
        Find your next favorite k-drama.
      </h1>

      <button
        className="bg-[#6ea3e8] hover:bg-blue-200 text-white px-6 py-3 rounded-xl text-lg drop-shadow-md"
        onClick={() => navigate("/recommendations")}
      >
        Get Recommendations
      </button>
    </div>
  );
}
