// src/components/Carousel.jsx

import { motion } from "framer-motion";

export default function Carousel({ dramas }) {
  return (
    <div className="overflow-x-auto py-4">
      <motion.div
        className="flex gap-4"
        drag="x"
        dragConstraints={{ left: -500, right: 0 }}
      >
        {dramas.map((drama) => (
          <motion.div
            key={drama.title}
            className="min-w-[200px] bg-white rounded-lg shadow p-2 cursor-pointer hover:shadow-lg"
            whileHover={{ scale: 1.05 }}
          >
            <img
              src={drama.image}
              alt={drama.title}
              className="w-full h-48 object-cover rounded"
            />
            <h3 className="mt-2 font-semibold">{drama.title}</h3>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
