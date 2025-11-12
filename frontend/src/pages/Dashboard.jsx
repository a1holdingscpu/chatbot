import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API } from '../App';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Upload, TrendingUp, DollarSign, Building2, Target } from 'lucide-react';
import { toast } from 'sonner';

export default function Dashboard() {
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [topDeals, setTopDeals] = useState([]);
  const [loading, setLoading] = useState(true);

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
      setTopDeals(dealsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

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
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8" data-testid="dashboard">
      {/* Hero Section */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Welcome to DealIQ Pro</h1>
        <p className="text-lg text-gray-600">Intelligent Real Estate Deal Analysis & Investment Insights</p>
      </div>

      {/* Quick Actions */}
      {!stats || stats.total_deals === 0 ? (
        <Card className="mb-8 border-2 border-dashed border-blue-300 bg-blue-50">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Upload className="h-16 w-16 text-blue-600 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Get Started</h3>
            <p className="text-gray-600 mb-6 text-center max-w-md">
              Upload your first Excel file to analyze real estate deals and get instant insights
            </p>
            <Button
              size="lg"
              onClick={() => navigate('/analyzer/upload')}
              className="bg-blue-600 hover:bg-blue-700"
              data-testid="get-started-upload-btn"
            >
              <Upload className="mr-2 h-5 w-5" />
              Upload Deals
            </Button>
          </CardContent>
        </Card>
      ) : (
        <>
          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <Card data-testid="stat-total-deals">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Total Deals</CardTitle>
                <Building2 className="h-5 w-5 text-blue-600" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-gray-900">{stats.total_deals}</div>
                <p className="text-xs text-gray-500 mt-1">{stats.top_deals_count} top deals</p>
              </CardContent>
            </Card>

            <Card data-testid="stat-avg-score">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Avg Deal Score</CardTitle>
                <Target className="h-5 w-5 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-gray-900">{stats.average_score.toFixed(1)}</div>
                <p className="text-xs text-gray-500 mt-1">Out of 100</p>
              </CardContent>
            </Card>

            <Card data-testid="stat-cap-rate">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Avg Cap Rate</CardTitle>
                <TrendingUp className="h-5 w-5 text-purple-600" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-gray-900">{stats.average_cap_rate.toFixed(2)}%</div>
                <p className="text-xs text-gray-500 mt-1">Annual return</p>
              </CardContent>
            </Card>

            <Card data-testid="stat-total-value">
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium text-gray-600">Portfolio Value</CardTitle>
                <DollarSign className="h-5 w-5 text-orange-600" />
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold text-gray-900">
                  ${(stats.total_value / 1000000).toFixed(1)}M
                </div>
                <p className="text-xs text-gray-500 mt-1">Total deal value</p>
              </CardContent>
            </Card>
          </div>

          {/* Top Deals */}
          <Card data-testid="top-deals-section">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Top Performing Deals</CardTitle>
                  <CardDescription>Highest scoring investment opportunities</CardDescription>
                </div>
                <Button
                  variant="outline"
                  onClick={() => navigate('/analyzer/deals')}
                  data-testid="view-all-deals-btn"
                >
                  View All Deals
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {topDeals.map((deal) => (
                  <div
                    key={deal.id}
                    className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
                    onClick={() => navigate('/analyzer/deals')}
                    data-testid={`top-deal-${deal.id}`}
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
                        <span>Price: ${deal.price.toLocaleString()}</span>
                        <span>Cap Rate: {deal.cap_rate.toFixed(2)}%</span>
                        <span>Cash Flow: ${deal.monthly_cashflow.toLocaleString()}/mo</span>
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

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
            <Card className="cursor-pointer hover:shadow-lg transition-shadow" onClick={() => navigate('/analyzer/upload')}>
              <CardHeader>
                <Upload className="h-8 w-8 text-blue-600 mb-2" />
                <CardTitle>Upload New Deals</CardTitle>
                <CardDescription>Analyze more real estate opportunities</CardDescription>
              </CardHeader>
            </Card>

            <Card className="cursor-pointer hover:shadow-lg transition-shadow" onClick={() => navigate('/analyzer/analytics')}>
              <CardHeader>
                <TrendingUp className="h-8 w-8 text-green-600 mb-2" />
                <CardTitle>View Analytics</CardTitle>
                <CardDescription>Deep dive into your portfolio metrics</CardDescription>
              </CardHeader>
            </Card>
          </div>
        </>
      )}
    </div>
  );
}
