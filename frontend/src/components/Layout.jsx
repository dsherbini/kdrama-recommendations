// src/components/Layout.jsx
// Layout for the app with sidebar and main content

import Sidebar from "./Sidebar";

export default function Layout({ children }) {
  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 bg-gray-50 min-h-screen">{children}</main>
    </div>
  );
}
