import { Outlet } from 'react-router-dom';
import { useState } from 'react';
import Navbar from './navbar';
import Sidebar from './sidebar';
import Footer from './footer';

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar setSidebarOpen={setSidebarOpen} />

      <div className="flex flex-1">
        <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />

        <main className="flex-1 px-4 py-8 md:px-6 lg:px-8">
          <div className="container mx-auto">
            <Outlet />
          </div>
        </main>
      </div>

      <Footer />
    </div>
  );
}
