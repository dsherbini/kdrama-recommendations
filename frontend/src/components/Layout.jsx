// src/components/Layout.jsx
// Layout for the app with sidebar, footer, and main content


import Sidebar from "./Sidebar";
import Footer from "./Footer";

export default function Layout({ children }) {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 bg-gray-50">{children}</main>
      </div>
      <Footer />
    </div>
  );
}

