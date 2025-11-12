import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Home, Lock, Mail, AlertCircle, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(email, password);

    if (result.success) {
      toast.success('Login successful!');
      navigate('/dashboard');
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
              <Home className="w-7 h-7 text-white" />
            </div>
            <span className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              DealiQ Pro
            </span>
          </div>
          <p className="text-gray-600">Sign in to access your account</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Welcome Back</CardTitle>
            <CardDescription>Enter your credentials to continue</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="username"
                    type="text"
                    placeholder="Enter username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="password"
                    type="password"
                    placeholder="Enter password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="pl-10"
                    required
                  />
                </div>
              </div>

              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600"
                disabled={loading}
              >
                {loading ? 'Signing in...' : 'Sign In'}
              </Button>
            </form>

            {/* Demo Credentials */}
            <div className="mt-6 pt-6 border-t">
              <p className="text-sm text-gray-600 mb-3 font-semibold">Demo Accounts:</p>
              <div className="space-y-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => fillDemo('demo')}
                  className="w-full justify-start text-left"
                >
                  <div className="flex-1">
                    <div className="font-semibold">Demo User</div>
                    <div className="text-xs text-gray-500">demo / demo123 • Professional Plan</div>
                  </div>
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => fillDemo('admin')}
                  className="w-full justify-start text-left"
                >
                  <div className="flex-1">
                    <div className="font-semibold">Admin User</div>
                    <div className="text-xs text-gray-500">admin / admin123 • Enterprise Plan</div>
                  </div>
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => fillDemo('test')}
                  className="w-full justify-start text-left"
                >
                  <div className="flex-1">
                    <div className="font-semibold">Test User</div>
                    <div className="text-xs text-gray-500">test / test123 • Starter Plan</div>
                  </div>
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <div className="text-center mt-6">
          <Button variant="link" onClick={() => navigate('/')}>
            ← Back to Home
          </Button>
        </div>
      </div>
    </div>
  );
}
