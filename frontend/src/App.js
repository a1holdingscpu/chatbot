import { useState, useEffect } from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';
import { Calculator } from 'lucide-react';
import InvestorLanding from './pages/InvestorLanding';
import Dashboard from './pages/Dashboard';
import DealsPage from './pages/DealsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import UploadPage from './pages/UploadPage';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AnalyzerNavigation() {
  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/analyzer" className="flex items-center space-x-3">
            <div className="bg-white text-blue-600 font-bold text-xl px-3 py-1 rounded">
              DealIQ
            </div>
            <span className="text-xl font-semibold">Analyzer</span>
          </Link>
          
          <div className="flex space-x-1">
            <Link
              to="/analyzer"
              className="px-4 py-2 rounded-lg hover:bg-white/10 transition-colors"
              data-testid="nav-dashboard"
            >
              Dashboard
            </Link>
            <Link
              to="/analyzer/upload"
              className="px-4 py-2 rounded-lg hover:bg-white/10 transition-colors"
              data-testid="nav-upload"
            >
              Upload
            </Link>
            <Link
              to="/analyzer/deals"
              className="px-4 py-2 rounded-lg hover:bg-white/10 transition-colors"
              data-testid="nav-deals"
            >
              Deals
            </Link>
            <Link
              to="/analyzer/analytics"
              className="px-4 py-2 rounded-lg hover:bg-white/10 transition-colors"
              data-testid="nav-analytics"
            >
              Analytics
            </Link>
            <Link
              to="/"
              className="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors border border-white/20"
            >
              ← Back to Home
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

function AppContent() {
  const location = useLocation();
  const isAnalyzer = location.pathname.startsWith('/analyzer');

  return (
    <div className="App min-h-screen bg-gray-50">
      {isAnalyzer && <AnalyzerNavigation />}
      <Toaster position="top-right" />
      <Routes>
        {/* Public Landing Page */}
        <Route path="/" element={<InvestorLanding />} />
        
        {/* Internal Analyzer Tool */}
        <Route path="/analyzer" element={<Dashboard />} />
        <Route path="/analyzer/upload" element={<UploadPage />} />
        <Route path="/analyzer/deals" element={<DealsPage />} />
        <Route path="/analyzer/analytics" element={<AnalyticsPage />} />
      </Routes>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppContent />
    </BrowserRouter>
  );
}

export default App;
export { API };
