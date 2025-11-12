import { useState, useEffect } from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';
import Dashboard from './pages/Dashboard';
import DealsPage from './pages/DealsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import UploadPage from './pages/UploadPage';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function Navigation() {
  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-3">
            <div className="bg-white text-blue-600 font-bold text-xl px-3 py-1 rounded">
              DealIQ
            </div>
            <span className="text-xl font-semibold">Pro</span>
          </Link>
          
          <div className="flex space-x-1">
            <Link
              to="/"
              className="px-4 py-2 rounded-lg hover:bg-white/10 transition-colors"
              data-testid="nav-dashboard"
            >
              Dashboard
            </Link>
            <Link
              to="/upload"
              className="px-4 py-2 rounded-lg hover:bg-white/10 transition-colors"
              data-testid="nav-upload"
            >
              Upload
            </Link>
            <Link
              to="/deals"
              className="px-4 py-2 rounded-lg hover:bg-white/10 transition-colors"
              data-testid="nav-deals"
            >
              Deals
            </Link>
            <Link
              to="/analytics"
              className="px-4 py-2 rounded-lg hover:bg-white/10 transition-colors"
              data-testid="nav-analytics"
            >
              Analytics
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <div className="App min-h-screen bg-gray-50">
      <BrowserRouter>
        <Navigation />
        <Toaster position="top-right" />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/deals" element={<DealsPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
export { API };
