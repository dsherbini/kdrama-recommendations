// src/components/Card.jsx
// Card component to display drama info and open Popup on click.

import { useState } from "react";
import { motion } from "framer-motion";
import Popup from "./Popup";
import GenreChip from "./GenreChip";

export default function Card({ drama }) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <>
      <motion.div
        className="bg-white p-4 rounded-lg shadow hover:shadow-lg cursor-pointer w-52"
        whileHover={{ scale: 1.05 }}
        onClick={openModal}
      >
        {/* Fixed height container for title */}
        <div className="h-24 flex items-center justify-center text-center p-2">
          <h2 className="card-header text-lg">{drama.title}</h2>
        </div>

        <img
          src={drama.image}
          alt={drama.title}
          className="w-full h-48 object-contain rounded"
        />
      </motion.div>

      {isModalOpen && (
        <Popup onClose={closeModal}>
          {/* Title */}
          <h2 className="card-header text-2xl font-bold mb-4 text-center">{drama.title}</h2>

          {/* Image + details */}
          <div className="flex flex-col md:flex-row gap-4">
            <img
              src={drama.image}
              alt={drama.title}
              className="w-full md:w-48 h-48 object-contain rounded"
            />

            <div className="flex-1 flex flex-col justify-center gap-2">
              {drama.korean_title && (
                <p>🇰🇷 <strong>Original Korean Title:</strong> {drama.korean_title}</p>
              )}
              {drama.translated_title && (
                <p>🔄 <strong>Translated Title:</strong> {drama.translated_title}</p>
              )}
              {drama.rating && (
                <p>⭐ <strong>Rating:</strong> {drama.rating}</p>
              )}
              {drama.genres && (
                <div>
                  🎭 <strong>Genres:</strong>
                  <div className="mt-1 flex flex-wrap">
                    <GenreChip genre={drama.genres} />
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Synopsis */}
          {drama.synopsis && (
            <p className="mt-4 text-gray-700">
              <strong>Synopsis:</strong> {drama.synopsis}
            </p>
          )}

          {/* Link */}
          {drama.link && (
            <a
              href={drama.link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-700 hover:text-blue-500 mt-4 inline-block"
            >
              More Details
            </a>
          )}
        </Popup>
      )}
    </>
  );
}
