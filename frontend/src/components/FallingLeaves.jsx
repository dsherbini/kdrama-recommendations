// src/components/FallingLeaves.jsx
// Fallling leaves effect

import { useEffect, useState } from "react";

const NUM_LEAVES = 15; // number of leaves on screen

export default function FallingLeaves() {
  const [leaves, setLeaves] = useState([]);

  useEffect(() => {
    const newLeaves = Array.from({ length: NUM_LEAVES }).map(() => ({
      id: Math.random().toString(36).substr(2, 9),
      left: Math.random() * 100, // horizontal position %
      size: 20 + Math.random() * 20, // size in px
      duration: 5 + Math.random() * 5, // animation duration
      delay: Math.random() * 5, // animation delay
      rotation: Math.random() * 360, // initial rotation
    }));
    setLeaves(newLeaves);
  }, []);

  return (
    <>
      {leaves.map((leaf) => (
        <img
          key={leaf.id}
          src="/cherry_blossom.png" // Need to find a good leaf image
          alt="leaf"
          className="absolute top-[-50px] animate-fall"
          style={{
            left: `${leaf.left}%`,
            width: `${leaf.size}px`,
            height: `${leaf.size}px`,
            animationDuration: `${leaf.duration}s`,
            animationDelay: `${leaf.delay}s`,
            transform: `rotate(${leaf.rotation}deg)`,
          }}
        />
      ))}
    </>
  );
}
