// src/components/Popup.jsx
// Popup component for the cards. Popup modal box appears when a card is clicked.

import { motion } from "framer-motion";

export default function Popup({ children, onClose }) {
  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
      onClick={onClose} // Close when clicking outside
    >
      <motion.div
        className="bg-white rounded-lg shadow-lg w-full max-w-2xl relative flex flex-col max-h-[80vh]"
        onClick={(e) => e.stopPropagation()}
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
      >
        {/* Header (fixed) */}
        <div className="flex justify-end p-3 border-b">
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 font-bold text-xl"
          >
            ✕
          </button>
        </div>

        {/* Scrollable Content */}
        <div className="overflow-y-auto p-6">
          {children}
        </div>
      </motion.div>
    </div>
  );
}

