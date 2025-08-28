// src/components/Sidebar.jsx
// Left sidebar with hamburger menu

import { useState } from "react";
import { NavLink } from "react-router-dom";
import { Menu, X } from "lucide-react";

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(true);

  return (
    <div className="fixed top-0 left-0 h-screen z-50">
      {/* Toggle hamburger button (always visible) */}
      {!isOpen && (
        <button
          className="p-3 m-2 rounded bg-white/40 backdrop-blur-md text-[#6ea3e8] shadow-md"
          onClick={() => setIsOpen(true)}
        >
          <Menu />
        </button>
      )}

      {/* Sidebar - only render when toggled open */}
      {isOpen && (
        <div
          className="bg-white/30 backdrop-blur-md text-[#6ea3e8] h-full w-64 shadow-lg transition-all duration-300 p-4"
        >

          {/* Close button */}
          <button
            className="mb-4 p-2 rounded bg-white/40 text-[#6ea3e8]"
            onClick={() => setIsOpen(false)}
          >
            <X />
          </button>

          {/* App title */}
          <h1 className="text-2xl font-bold mb-6 text-left px-4">Kdramarama</h1>

          <nav>
            <NavLink to="/" className="block px-4 py-2 hover:bg-white/50 rounded-md">
              Home
            </NavLink>
            <NavLink to="/recommendations" className="block px-4 py-2 hover:bg-white/50 rounded-md">
              Recommendations
            </NavLink>
            <NavLink to="/about" className="block px-4 py-2 hover:bg-white/50 rounded-md">
              About
            </NavLink>
          </nav>
        </div>
      )}
    </div>
  );
}
