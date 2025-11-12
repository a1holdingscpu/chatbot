import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is already logged in
    const storedUser = localStorage.getItem('dealiq_user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = (username, password) => {
    // Demo credentials
    const validCredentials = [
      { username: 'demo', password: 'demo123', name: 'Demo User', email: 'demo@dealiq.com', plan: 'Professional' },
      { username: 'admin', password: 'admin123', name: 'Admin User', email: 'admin@dealiq.com', plan: 'Enterprise' },
      { username: 'test', password: 'test123', name: 'Test User', email: 'test@dealiq.com', plan: 'Starter' }
    ];

    const user = validCredentials.find(
      cred => cred.username === username && cred.password === password
    );

    if (user) {
      const userData = {
        name: user.name,
        email: user.email,
        plan: user.plan,
        username: user.username
      };
      setUser(userData);
      localStorage.setItem('dealiq_user', JSON.stringify(userData));
      return { success: true };
    }

    return { success: false, error: 'Invalid username or password' };
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('dealiq_user');
  };

  const value = {
    user,
    login,
    logout,
    isAuthenticated: !!user,
    loading
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
