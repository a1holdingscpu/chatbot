import { useState, useEffect } from 'react';
import '@/App.css';
import { BrowserRouter, Routes, Route, Link, useLocation, Navigate } from 'react-router-dom';
import axios from 'axios';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';
import { User, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { AuthProvider, useAuth } from './context/AuthContext';
import SaaSLanding from './pages/SaaSLanding';
import LoginPage from './pages/LoginPage';
import ClientDashboard from './pages/ClientDashboard';
import DealsPage from './pages/DealsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import UploadPage from './pages/UploadPage';
import PaymentSuccess from './pages/PaymentSuccess';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Protected Route Component
function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
}

function Navigation() {
  const { user, logout } = useAuth();
  
  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/dashboard" className="flex items-center space-x-3">
            <div className="bg-white text-blue-600 font-bold text-xl px-3 py-1 rounded">
              DealiQ
            </div>
            <span className="text-xl font-semibold">Pro</span>
          </Link>
          
          <div className="flex items-center space-x-1">
            <Link
              to="/dashboard"
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
            
            <div className="ml-4 pl-4 border-l border-white/20 flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                className="text-white hover:bg-white/10"
              >
                <User className="w-4 h-4 mr-2" />
                {user?.name || 'User'}
              </Button>
              <Button
                variant="ghost"
                size="sm"
                className="text-white hover:bg-white/10"
                onClick={logout}
                title="Logout"
              >
                <LogOut className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

function AppContent() {
  const location = useLocation();
  const showNav = location.pathname !== '/';

  return (
    <div className="App min-h-screen bg-gray-50">
      {showNav && <Navigation />}
      <Toaster position="top-right" />
      <Routes>
        {/* Landing Page */}
        <Route path="/" element={<SaaSLanding />} />
        
        {/* App Routes */}
        <Route path="/dashboard" element={<ClientDashboard />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/deals" element={<DealsPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="/payment-success" element={<PaymentSuccess />} />
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
