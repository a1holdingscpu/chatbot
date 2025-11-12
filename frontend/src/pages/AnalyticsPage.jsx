import { useEffect, useState } from 'react';
import axios from 'axios';
import { API } from '../App';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, DollarSign, Target, PieChart } from 'lucide-react';
import { toast } from 'sonner';

export default function AnalyticsPage() {
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
        axios.get(`${API}/deals?limit=10`)
      ]);
      setStats(statsRes.data);
      setTopDeals(dealsRes.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
      toast.error('Failed to load analytics');
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
          <p className="mt-4 text-gray-600">Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (!stats || stats.total_deals === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <PieChart className="h-16 w-16 text-gray-400 mb-4" />
            <p className="text-lg text-gray-600 mb-2">No analytics available</p>
            <p className="text-sm text-gray-500">Upload deals to see analytics</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8" data-testid="analytics-page">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Analytics Dashboard</h1>
        <p className="text-gray-600">Deep insights into your real estate investment portfolio</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card data-testid="analytics-total-deals">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-gray-600">Total Deals Analyzed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-gray-900">{stats.total_deals}</div>
            <p className="text-sm text-gray-500 mt-1">
              {stats.top_deals_count} high-quality deals (70+ score)
            </p>
          </CardContent>
        </Card>

        <Card data-testid="analytics-avg-score">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-gray-600">Average Deal Score</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-gray-900">{stats.average_score.toFixed(1)}</div>
            <p className="text-sm text-gray-500 mt-1">Out of 100</p>
          </CardContent>
        </Card>

        <Card data-testid="analytics-cap-rate">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-gray-600">Avg Cap Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-gray-900">{stats.average_cap_rate.toFixed(2)}%</div>
            <p className="text-sm text-gray-500 mt-1">Annual return on investment</p>
          </CardContent>
        </Card>

        <Card data-testid="analytics-coc">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-gray-600">Avg Cash on Cash</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-gray-900">{stats.average_cash_on_cash.toFixed(2)}%</div>
            <p className="text-sm text-gray-500 mt-1">Return on invested capital</p>
          </CardContent>
        </Card>
      </div>

      {/* Portfolio Value */}
      <Card className="mb-8" data-testid="portfolio-value-card">
        <CardHeader>
          <div className="flex items-center space-x-2">
            <DollarSign className="h-6 w-6 text-green-600" />
            <CardTitle>Total Portfolio Value</CardTitle>
          </div>
          <CardDescription>Combined value of all analyzed deals</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-4xl font-bold text-green-600">
            ${(stats.total_value / 1000000).toFixed(2)}M
          </div>
        </CardContent>
      </Card>

      {/* Distribution Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        {/* Strategy Distribution */}
        <Card data-testid="strategy-distribution-card">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Target className="h-5 w-5 text-blue-600" />
              <CardTitle>Strategy Distribution</CardTitle>
            </div>
            <CardDescription>Breakdown of recommended investment strategies</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(stats.strategy_distribution).map(([strategy, count]) => {
                const percentage = ((count / stats.total_deals) * 100).toFixed(1);
                return (
                  <div key={strategy}>
                    <div className="flex items-center justify-between mb-2">
                      <Badge className={getStrategyColor(strategy)}>
                        {strategy.replace('_', ' ')}
                      </Badge>
                      <span className="text-sm font-medium">
                        {count} deals ({percentage}%)
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full transition-all"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Property Type Distribution */}
        <Card data-testid="property-type-distribution-card">
          <CardHeader>
            <div className="flex items-center space-x-2">
              <PieChart className="h-5 w-5 text-purple-600" />
              <CardTitle>Property Type Distribution</CardTitle>
            </div>
            <CardDescription>Types of properties in your portfolio</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {Object.entries(stats.property_type_distribution).map(([type, count]) => {
                const percentage = ((count / stats.total_deals) * 100).toFixed(1);
                return (
                  <div key={type}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-gray-900">{type || 'Unknown'}</span>
                      <span className="text-sm text-gray-600">
                        {count} ({percentage}%)
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-purple-600 h-2 rounded-full transition-all"
                        style={{ width: `${percentage}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Top Performing Deals */}
      <Card data-testid="top-deals-analytics-card">
        <CardHeader>
          <div className="flex items-center space-x-2">
            <TrendingUp className="h-5 w-5 text-green-600" />
            <CardTitle>Top 10 Performing Deals</CardTitle>
          </div>
          <CardDescription>Highest scoring investment opportunities</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {topDeals.map((deal, index) => (
              <div
                key={deal.id}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                data-testid={`top-deal-analytics-${deal.id}`}
              >
                <div className="flex items-center space-x-4 flex-1">
                  <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="font-semibold text-gray-900">
                        {deal.address || '(No Address)'}
                      </span>
                      <Badge className={getStrategyColor(deal.preferred_strategy)}>
                        {deal.preferred_strategy?.replace('_', ' ')}
                      </Badge>
                    </div>
                    <div className="text-sm text-gray-600">
                      ${deal.price.toLocaleString()} • 
                      Cap: {deal.cap_rate.toFixed(2)}% • 
                      CoC: {deal.cash_on_cash_pct.toFixed(2)}% • 
                      CF: ${deal.monthly_cashflow.toLocaleString()}/mo
                    </div>
                  </div>
                </div>
                <div className="text-right ml-4">
                  <div className="text-2xl font-bold text-blue-600">{deal.deal_score}</div>
                  <div className="text-xs text-gray-500">Score</div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
