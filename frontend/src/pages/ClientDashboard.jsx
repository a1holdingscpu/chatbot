import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API } from '../App';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Upload, TrendingUp, DollarSign, Building2, Target, 
  BarChart3, FileSpreadsheet, Clock, Zap, ArrowRight,
  Calendar, Crown, Sparkles, Activity, TrendingDown
} from 'lucide-react';
import { toast } from 'sonner';

export default function ClientDashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [recentDeals, setRecentDeals] = useState([]);
  const [loading, setLoading] = useState(true);

  // Mock user data - in real app, this would come from auth context
  const [userData] = useState({
    name: "John Smith",
    email: "john@example.com",
    plan: "Professional",
    planColor: "blue",
    dealsThisMonth: 47,
    dealsLimit: null, // null = unlimited
    uploadsThisMonth: 8,
    memberSince: "Jan 2025"
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsRes, dealsRes] = await Promise.all([
        axios.get(`${API}/stats`),
        axios.get(`${API}/deals?limit=5`)
      ]);
      setStats(statsRes.data);
      setRecentDeals(dealsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      title: "Upload New Deals",
      description: "Analyze properties from Excel",
      icon: <Upload className="w-8 h-8" />,
      color: "from-blue-500 to-blue-600",
      action: () => navigate('/upload')
    },
    {
      title: "Browse All Deals",
      description: "View & filter your portfolio",
      icon: <Building2 className="w-8 h-8" />,
      color: "from-purple-500 to-purple-600",
      action: () => navigate('/deals')
    },
    {
      title: "View Analytics",
      description: "Insights & performance",
      icon: <BarChart3 className="w-8 h-8" />,
      color: "from-green-500 to-green-600",
      action: () => navigate('/analytics')
    }
  ];

  const recentActivity = [
    { action: "Uploaded deals", count: "12 properties", time: "2 hours ago", icon: <Upload className="w-4 h-4" /> },
    { action: "Analyzed portfolio", count: "Phoenix Metro", time: "5 hours ago", icon: <BarChart3 className="w-4 h-4" /> },
    { action: "Exported deals", count: "Top 10 deals", time: "1 day ago", icon: <FileSpreadsheet className="w-4 h-4" /> },
  ];

  const getStrategyColor = (strategy) => {
    const colors = {
      wholesale: 'bg-purple-100 text-purple-800',
      flip: 'bg-orange-100 text-orange-800',
      buy_hold: 'bg-green-100 text-green-800',
      subject_to: 'bg-blue-100 text-blue-800',
      seller_finance: 'bg-yellow-100 text-yellow-800',
      hold: 'bg-gray-100 text-gray-800'
    };
    return colors[strategy] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-7xl">
        {/* Welcome Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Welcome back, {userData.name}! 👋
              </h1>
              <p className="text-gray-600">Here's what's happening with your portfolio today</p>
            </div>
            <div className="mt-4 md:mt-0">
              <Badge className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white border-none">
                <Crown className="w-4 h-4 mr-2" />
                {userData.plan} Plan
              </Badge>
            </div>
          </div>
        </div>

        {/* Account Usage Stats */}
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <Card className="border-2 border-blue-100 bg-gradient-to-br from-blue-50 to-white">
            <CardHeader>
              <CardTitle className="text-sm font-medium text-gray-600">Deals Analyzed</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-end justify-between">
                <div>
                  <div className="text-3xl font-bold text-gray-900">{userData.dealsThisMonth}</div>
                  <p className="text-sm text-gray-600 mt-1">
                    {userData.dealsLimit ? `of ${userData.dealsLimit} this month` : 'Unlimited'}
                  </p>
                </div>
                <Activity className="w-8 h-8 text-blue-600" />
              </div>
              {userData.dealsLimit && (
                <Progress value={(userData.dealsThisMonth / userData.dealsLimit) * 100} className="mt-4" />
              )}
            </CardContent>
          </Card>

          <Card className="border-2 border-purple-100 bg-gradient-to-br from-purple-50 to-white">
            <CardHeader>
              <CardTitle className="text-sm font-medium text-gray-600">File Uploads</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-end justify-between">
                <div>
                  <div className="text-3xl font-bold text-gray-900">{userData.uploadsThisMonth}</div>
                  <p className="text-sm text-gray-600 mt-1">This month</p>
                </div>
                <Upload className="w-8 h-8 text-purple-600" />
              </div>
            </CardContent>
          </Card>

          <Card className="border-2 border-green-100 bg-gradient-to-br from-green-50 to-white">
            <CardHeader>
              <CardTitle className="text-sm font-medium text-gray-600">Member Since</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-end justify-between">
                <div>
                  <div className="text-3xl font-bold text-gray-900">{userData.memberSince}</div>
                  <p className="text-sm text-gray-600 mt-1">Active subscriber</p>
                </div>
                <Calendar className="w-8 h-8 text-green-600" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {quickActions.map((action, idx) => (
              <Card
                key={idx}
                className="cursor-pointer hover:shadow-xl transition-all duration-300 border-2 hover:border-blue-200"
                onClick={action.action}
              >
                <CardContent className="p-6">
                  <div className={`w-16 h-16 bg-gradient-to-br ${action.color} rounded-xl flex items-center justify-center text-white mb-4`}>
                    {action.icon}
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">{action.title}</h3>
                  <p className="text-gray-600 mb-4">{action.description}</p>
                  <Button variant="ghost" className="p-0 h-auto text-blue-600 hover:text-blue-700">
                    Get started <ArrowRight className="ml-2 w-4 h-4" />
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Portfolio Overview */}
        {stats && stats.total_deals > 0 && (
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="w-5 h-5 mr-2 text-blue-600" />
                  Portfolio Summary
                </CardTitle>
                <CardDescription>Your investment portfolio at a glance</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-600">Total Deals</span>
                    <span className="text-2xl font-bold text-gray-900">{stats.total_deals}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-600">Average Score</span>
                    <span className="text-2xl font-bold text-blue-600">{stats.average_score.toFixed(1)}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-600">Top Deals (70+)</span>
                    <span className="text-2xl font-bold text-green-600">{stats.top_deals_count}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-gray-600">Portfolio Value</span>
                    <span className="text-2xl font-bold text-purple-600">
                      ${(stats.total_value / 1000000).toFixed(2)}M
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Activity className="w-5 h-5 mr-2 text-purple-600" />
                  Recent Activity
                </CardTitle>
                <CardDescription>Your latest actions</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentActivity.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg transition">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center text-blue-600">
                          {item.icon}
                        </div>
                        <div>
                          <div className="font-medium text-gray-900">{item.action}</div>
                          <div className="text-sm text-gray-600">{item.count}</div>
                        </div>
                      </div>
                      <div className="text-xs text-gray-500">{item.time}</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Recent Deals */}
        {recentDeals.length > 0 && (
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="flex items-center">
                    <Building2 className="w-5 h-5 mr-2 text-green-600" />
                    Recent Deals
                  </CardTitle>
                  <CardDescription>Your most recently analyzed properties</CardDescription>
                </div>
                <Button variant="outline" onClick={() => navigate('/deals')}>
                  View All Deals
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {recentDeals.map((deal) => (
                  <div
                    key={deal.id}
                    className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
                    onClick={() => navigate('/deals')}
                  >
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h4 className="font-semibold text-gray-900">
                          {deal.address || '(No Address)'}
                        </h4>
                        <Badge className={getStrategyColor(deal.preferred_strategy)}>
                          {deal.preferred_strategy?.replace('_', ' ')}
                        </Badge>
                      </div>
                      <div className="flex items-center space-x-6 text-sm text-gray-600">
                        <span className="flex items-center">
                          <DollarSign className="w-4 h-4 mr-1" />
                          ${deal.price.toLocaleString()}
                        </span>
                        <span className="flex items-center">
                          <TrendingUp className="w-4 h-4 mr-1" />
                          {deal.cap_rate.toFixed(2)}% Cap
                        </span>
                        <span className={`flex items-center ${deal.monthly_cashflow > 0 ? 'text-green-600' : 'text-red-600'}`}>
                          ${deal.monthly_cashflow.toLocaleString()}/mo
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-600">{deal.deal_score}</div>
                      <div className="text-xs text-gray-500">Score</div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Empty State */}
        {!stats || stats.total_deals === 0 && (
          <Card className="border-2 border-dashed border-blue-300 bg-blue-50">
            <CardContent className="flex flex-col items-center justify-center py-16">
              <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mb-6">
                <Upload className="h-10 w-10 text-blue-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Get Started with Your First Upload</h3>
              <p className="text-gray-600 mb-6 text-center max-w-md">
                Upload an Excel file with your property deals to start analyzing and making data-driven investment decisions
              </p>
              <Button
                size="lg"
                onClick={() => navigate('/upload')}
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white"
              >
                <Upload className="mr-2 h-5 w-5" />
                Upload Your First Deals
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Tips & Resources */}
        <div className="mt-8 grid md:grid-cols-2 gap-6">
          <Card className="bg-gradient-to-br from-blue-50 to-purple-50 border-blue-200">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Sparkles className="w-5 h-5 mr-2 text-blue-600" />
                Pro Tips
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                <li className="flex items-start">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs mr-3 mt-0.5">1</div>
                  <div className="flex-1">
                    <p className="text-sm text-gray-700">Upload deals in bulk for faster analysis - supports Excel files with hundreds of properties</p>
                  </div>
                </li>
                <li className="flex items-start">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs mr-3 mt-0.5">2</div>
                  <div className="flex-1">
                    <p className="text-sm text-gray-700">Focus on deals with 70+ scores for the highest probability opportunities</p>
                  </div>
                </li>
                <li className="flex items-start">
                  <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs mr-3 mt-0.5">3</div>
                  <div className="flex-1">
                    <p className="text-sm text-gray-700">Use the analytics dashboard to track your portfolio performance over time</p>
                  </div>
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-50 to-blue-50 border-green-200">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Zap className="w-5 h-5 mr-2 text-green-600" />
                Need Help?
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <p className="text-sm text-gray-700">Access our resources to get the most out of DealIQ Pro</p>
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start" onClick={() => window.open('#', '_blank')}>
                    <FileSpreadsheet className="mr-2 h-4 w-4" />
                    Download Sample Excel Template
                  </Button>
                  <Button variant="outline" className="w-full justify-start" onClick={() => window.open('#', '_blank')}>
                    <Clock className="mr-2 h-4 w-4" />
                    Watch Video Tutorial
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
