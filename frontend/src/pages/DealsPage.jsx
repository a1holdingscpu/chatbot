import { useEffect, useState } from 'react';
import axios from 'axios';
import { API } from '../App';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Search, Filter, SortAsc, SortDesc, Eye, TrendingUp, TrendingDown, Sparkles, FileSpreadsheet } from 'lucide-react';
import { toast } from 'sonner';
import AIAnalysisDialog from '../components/AIAnalysisDialog';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';

export default function DealsPage() {
  const [deals, setDeals] = useState([]);
  const [filteredDeals, setFilteredDeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedDeal, setSelectedDeal] = useState(null);
  const [aiAnalysisDeal, setAiAnalysisDeal] = useState(null);
  const [showAIDialog, setShowAIDialog] = useState(false);
  const [purchaseDeal, setPurchaseDeal] = useState(null);
  const [showPurchaseDialog, setShowPurchaseDialog] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [strategyFilter, setStrategyFilter] = useState('all');
  const [sortBy, setSortBy] = useState('deal_score');
  const [sortOrder, setSortOrder] = useState('desc');

  useEffect(() => {
    fetchDeals();
  }, []);

  useEffect(() => {
    applyFiltersAndSort();
  }, [deals, searchTerm, strategyFilter, sortBy, sortOrder]);

  const fetchDeals = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/deals?limit=1000`);
      setDeals(response.data);
    } catch (error) {
      console.error('Error fetching deals:', error);
      toast.error('Failed to load deals');
    } finally {
      setLoading(false);
    }
  };

  const applyFiltersAndSort = () => {
    let filtered = [...deals];

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter((deal) =>
        (deal.address || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
        (deal.property_type || '').toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Strategy filter
    if (strategyFilter !== 'all') {
      filtered = filtered.filter((deal) => deal.preferred_strategy === strategyFilter);
    }

    // Sort
    filtered.sort((a, b) => {
      const aVal = a[sortBy] || 0;
      const bVal = b[sortBy] || 0;
      return sortOrder === 'asc' ? aVal - bVal : bVal - aVal;
    });

    setFilteredDeals(filtered);
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

  const getScoreColor = (score) => {
    if (score >= 70) return 'text-green-600';
    if (score >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const toggleSort = () => {
    setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[calc(100vh-4rem)]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading deals...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8" data-testid="deals-page">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">All Deals</h1>
        <p className="text-gray-600">Browse and analyze all your real estate investment opportunities</p>
      </div>

      {/* Filters */}
      <Card className="mb-6">
        <CardContent className="pt-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search by address..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
                data-testid="search-input"
              />
            </div>

            {/* Strategy Filter */}
            <Select value={strategyFilter} onValueChange={setStrategyFilter}>
              <SelectTrigger data-testid="strategy-filter">
                <SelectValue placeholder="All Strategies" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Strategies</SelectItem>
                <SelectItem value="wholesale">Wholesale</SelectItem>
                <SelectItem value="flip">Flip</SelectItem>
                <SelectItem value="buy_hold">Buy & Hold</SelectItem>
                <SelectItem value="subject_to">Subject To</SelectItem>
                <SelectItem value="seller_finance">Seller Finance</SelectItem>
                <SelectItem value="hold">Hold</SelectItem>
              </SelectContent>
            </Select>

            {/* Sort By */}
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger data-testid="sort-by">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="deal_score">Deal Score</SelectItem>
                <SelectItem value="price">Price</SelectItem>
                <SelectItem value="cap_rate">Cap Rate</SelectItem>
                <SelectItem value="cash_on_cash_pct">Cash on Cash</SelectItem>
                <SelectItem value="monthly_cashflow">Cash Flow</SelectItem>
              </SelectContent>
            </Select>

            {/* Sort Order */}
            <Button variant="outline" onClick={toggleSort} data-testid="sort-order-btn">
              {sortOrder === 'asc' ? (
                <>
                  <SortAsc className="mr-2 h-4 w-4" />
                  Ascending
                </>
              ) : (
                <>
                  <SortDesc className="mr-2 h-4 w-4" />
                  Descending
                </>
              )}
            </Button>
          </div>

          <div className="mt-4 text-sm text-gray-600">
            Showing {filteredDeals.length} of {deals.length} deals
          </div>
        </CardContent>
      </Card>

      {/* Deals Table */}
      {filteredDeals.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <p className="text-gray-600 mb-4">No deals found matching your filters</p>
            <Button variant="outline" onClick={() => { setSearchTerm(''); setStrategyFilter('all'); }}>
              Clear Filters
            </Button>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent className="p-0">
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Score</TableHead>
                    <TableHead>Address</TableHead>
                    <TableHead>Strategy</TableHead>
                    <TableHead className="text-right">Price</TableHead>
                    <TableHead className="text-right">Cap Rate</TableHead>
                    <TableHead className="text-right">Cash Flow</TableHead>
                    <TableHead className="text-right">CoC %</TableHead>
                    <TableHead className="text-center">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredDeals.map((deal) => (
                    <TableRow key={deal.id} className="hover:bg-gray-50" data-testid={`deal-row-${deal.id}`}>
                      <TableCell>
                        <span className={`text-2xl font-bold ${getScoreColor(deal.deal_score)}`}>
                          {deal.deal_score}
                        </span>
                      </TableCell>
                      <TableCell>
                        <div>
                          <div className="font-medium text-gray-900">
                            {deal.address || '(No Address)'}
                          </div>
                          <div className="text-sm text-gray-500">{deal.property_type}</div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <Badge className={getStrategyColor(deal.preferred_strategy)}>
                          {deal.preferred_strategy?.replace('_', ' ')}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right font-medium">
                        ${deal.price.toLocaleString()}
                      </TableCell>
                      <TableCell className="text-right">
                        <div className="flex items-center justify-end">
                          {deal.cap_rate >= 8 ? (
                            <TrendingUp className="h-4 w-4 text-green-600 mr-1" />
                          ) : (
                            <TrendingDown className="h-4 w-4 text-gray-400 mr-1" />
                          )}
                          {deal.cap_rate.toFixed(2)}%
                        </div>
                      </TableCell>
                      <TableCell className="text-right">
                        <span className={deal.monthly_cashflow > 0 ? 'text-green-600' : 'text-red-600'}>
                          ${deal.monthly_cashflow.toLocaleString()}
                        </span>
                      </TableCell>
                      <TableCell className="text-right">
                        {deal.cash_on_cash_pct.toFixed(2)}%
                      </TableCell>
                      <TableCell className="text-center">
                        <div className="flex items-center justify-center space-x-2">
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => setSelectedDeal(deal)}
                            data-testid={`view-deal-${deal.id}`}
                          >
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => {
                              setAiAnalysisDeal(deal);
                              setShowAIDialog(true);
                            }}
                            className="text-purple-600 hover:text-purple-700 hover:bg-purple-50"
                            data-testid={`ai-analysis-${deal.id}`}
                          >
                            <Sparkles className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => {
                              setPurchaseDeal(deal);
                              setShowPurchaseDialog(true);
                            }}
                            className="text-green-600 hover:text-green-700 hover:bg-green-50"
                            data-testid={`purchase-report-${deal.id}`}
                          >
                            <FileSpreadsheet className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* AI Analysis Dialog */}
      <AIAnalysisDialog
        deal={aiAnalysisDeal}
        open={showAIDialog}
        onOpenChange={setShowAIDialog}
      />

      {/* Purchase Report Dialog */}
      <PurchaseReportDialog
        deal={purchaseDeal}
        open={showPurchaseDialog}
        onOpenChange={setShowPurchaseDialog}
      />

      {/* Deal Details Dialog */}
      <Dialog open={!!selectedDeal} onOpenChange={(open) => !open && setSelectedDeal(null)}>
        <DialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto" data-testid="deal-details-dialog">
          {selectedDeal && (
            <>
              <DialogHeader>
                <DialogTitle className="text-2xl">
                  {selectedDeal.address || '(No Address)'}
                </DialogTitle>
                <DialogDescription>
                  {selectedDeal.property_type} • Deal Score: {selectedDeal.deal_score}
                </DialogDescription>
              </DialogHeader>

              <div className="space-y-6">
                {/* Strategy */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Recommended Strategy</h3>
                  <Badge className={getStrategyColor(selectedDeal.preferred_strategy)} data-testid="deal-strategy-badge">
                    {selectedDeal.preferred_strategy?.replace('_', ' ')}
                  </Badge>
                </div>

                {/* Financial Overview */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Financial Overview</h3>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <div className="bg-gray-50 p-3 rounded">
                      <div className="text-sm text-gray-600">Purchase Price</div>
                      <div className="text-lg font-semibold">${selectedDeal.price.toLocaleString()}</div>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <div className="text-sm text-gray-600">Down Payment</div>
                      <div className="text-lg font-semibold">${selectedDeal.down_payment_amount.toLocaleString()}</div>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <div className="text-sm text-gray-600">Loan Amount</div>
                      <div className="text-lg font-semibold">${selectedDeal.loan_amount.toLocaleString()}</div>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <div className="text-sm text-gray-600">Monthly Mortgage</div>
                      <div className="text-lg font-semibold">${selectedDeal.monthly_mortgage.toLocaleString()}</div>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <div className="text-sm text-gray-600">ARV</div>
                      <div className="text-lg font-semibold">${selectedDeal.arv.toLocaleString()}</div>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <div className="text-sm text-gray-600">Estimated Rehab</div>
                      <div className="text-lg font-semibold">${selectedDeal.estimated_rehab.toLocaleString()}</div>
                    </div>
                  </div>
                </div>

                {/* Returns */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Return Metrics</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-blue-50 p-3 rounded">
                      <div className="text-sm text-blue-600">Cap Rate</div>
                      <div className="text-xl font-bold text-blue-900">{selectedDeal.cap_rate.toFixed(2)}%</div>
                    </div>
                    <div className="bg-green-50 p-3 rounded">
                      <div className="text-sm text-green-600">Cash on Cash</div>
                      <div className="text-xl font-bold text-green-900">{selectedDeal.cash_on_cash_pct.toFixed(2)}%</div>
                    </div>
                    <div className="bg-purple-50 p-3 rounded">
                      <div className="text-sm text-purple-600">Monthly Cash Flow</div>
                      <div className="text-xl font-bold text-purple-900">${selectedDeal.monthly_cashflow.toLocaleString()}</div>
                    </div>
                    <div className="bg-orange-50 p-3 rounded">
                      <div className="text-sm text-orange-600">NOI</div>
                      <div className="text-xl font-bold text-orange-900">${selectedDeal.noi.toLocaleString()}</div>
                    </div>
                  </div>
                </div>

                {/* Income & Expenses */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Income & Expenses</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-50 p-3 rounded">
                      <div className="text-sm text-gray-600">Gross Annual Income</div>
                      <div className="text-lg font-semibold text-green-600">
                        ${selectedDeal.gross_income_annual.toLocaleString()}
                      </div>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <div className="text-sm text-gray-600">Operating Expenses</div>
                      <div className="text-lg font-semibold text-red-600">
                        ${selectedDeal.operating_expenses.toLocaleString()}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Property Details */}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">Property Details</h3>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {selectedDeal.sqft > 0 && (
                      <div>
                        <div className="text-sm text-gray-600">Square Feet</div>
                        <div className="font-medium">{selectedDeal.sqft.toLocaleString()}</div>
                      </div>
                    )}
                    {selectedDeal.beds && (
                      <div>
                        <div className="text-sm text-gray-600">Bedrooms</div>
                        <div className="font-medium">{selectedDeal.beds}</div>
                      </div>
                    )}
                    {selectedDeal.baths && (
                      <div>
                        <div className="text-sm text-gray-600">Bathrooms</div>
                        <div className="font-medium">{selectedDeal.baths}</div>
                      </div>
                    )}
                    {selectedDeal.units > 0 && (
                      <div>
                        <div className="text-sm text-gray-600">Units</div>
                        <div className="font-medium">{selectedDeal.units}</div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
