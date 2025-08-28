// src/components/GenreChips.jsx
// Displays genres as colored chips on the card popup

// src/components/GenreChip.jsx
export default function GenreChip({ genre }) {
  // Normalize genre text for display
  let genresArray = [];
  if (Array.isArray(genre)) {
    genresArray = genre;
  } else if (typeof genre === "string") {
    try {
      genresArray = JSON.parse(genre);
      if (!Array.isArray(genresArray)) genresArray = [];
    } catch {
      genresArray = genre
        .replace(/[\[\]']+/g, "")
        .split(",")
        .map((g) => g.trim())
        .filter((g) => g.length > 0);
    }
  }

  // Color palette
  const palette = [
    "bg-red-200 text-red-800",
    "bg-yellow-200 text-yellow-800",
    "bg-green-200 text-green-800",
    "bg-blue-200 text-blue-800",
    "bg-indigo-200 text-indigo-800",
    "bg-purple-200 text-purple-800",
    "bg-pink-200 text-pink-800",
    "bg-teal-200 text-teal-800",
    "bg-orange-200 text-orange-800",
    "bg-gray-200 text-gray-800",
    "bg-cyan-200 text-cyan-800",
    "bg-lime-200 text-lime-800",
    "bg-fuchsia-200 text-fuchsia-800",
    "bg-violet-200 text-violet-800",
  ];

  // Hash function to pick a color from palette
  const hashStringToColor = (str) => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    const index = Math.abs(hash) % palette.length;
    return palette[index];
  };

  return (
    <>
      {genresArray.map((g) => (
        <span
          key={g}
          className={`inline-block px-3 py-1 rounded-full text-sm font-semibold mr-2 mb-2 ${hashStringToColor(
            g
          )}`}
        >
          {g}
        </span>
      ))}
    </>
  );
}
