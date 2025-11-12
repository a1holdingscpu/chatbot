import { useState } from 'react';
import axios from 'axios';
import { API } from '../App';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { FileSpreadsheet, Check, Loader2, CreditCard } from 'lucide-react';
import { toast } from 'sonner';

export default function PurchaseReportDialog({ deal, open, onOpenChange }) {
  const [loading, setLoading] = useState(false);

  const handlePurchase = async () => {
    if (!deal) return;
    
    try {
      setLoading(true);
      
      // Get current origin URL
      const originUrl = window.location.origin;
      
      // Create checkout session
      const response = await axios.post(`${API}/payments/create-checkout`, {
        deal_id: deal.id,
        origin_url: originUrl
      });
      
      // Redirect to Stripe checkout
      if (response.data.url) {
        window.location.href = response.data.url;
      } else {
        throw new Error('No checkout URL received');
      }
    } catch (error) {
      console.error('Purchase error:', error);
      toast.error('Failed to initiate payment');
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-12 h-12 bg-gradient-to-br from-green-600 to-green-700 rounded-xl flex items-center justify-center">
              <FileSpreadsheet className="w-7 h-7 text-white" />
            </div>
            <div>
              <DialogTitle className="text-2xl">Purchase Premium Report</DialogTitle>
              <DialogDescription>
                Get comprehensive analysis for {deal?.address || 'this property'}
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>

        <div className="space-y-6">
          {/* Price */}
          <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-xl p-6 border-2 border-green-200 text-center">
            <div className="text-4xl font-bold text-green-600 mb-2">$25.00</div>
            <div className="text-sm text-gray-600">One-time purchase • Instant download</div>
          </div>

          {/* What's Included */}
          <div>
            <h3 className="text-lg font-bold text-gray-900 mb-4">What's Included:</h3>
            <div className="space-y-3">
              <div className="flex items-start">
                <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                  <Check className="w-4 h-4 text-green-600" />
                </div>
                <div>
                  <div className="font-semibold text-gray-900">Complete Financial Analysis</div>
                  <div className="text-sm text-gray-600">
                    All metrics including Cap Rate, CoC, NOI, cash flow projections, and ROI calculations
                  </div>
                </div>
              </div>

              <div className="flex items-start">
                <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                  <Check className="w-4 h-4 text-green-600" />
                </div>
                <div>
                  <div className="font-semibold text-gray-900">AI-Powered Insights</div>
                  <div className="text-sm text-gray-600">
                    Predictive analysis, risk factors, opportunities, and personalized recommendations
                  </div>
                </div>
              </div>

              <div className="flex items-start">
                <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                  <Check className="w-4 h-4 text-green-600" />
                </div>
                <div>
                  <div className="font-semibold text-gray-900">Comparable Properties (Comps)</div>
                  <div className="text-sm text-gray-600">
                    5 similar properties with pricing, location, and key specs for market comparison
                  </div>
                </div>
              </div>

              <div className="flex items-start">
                <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                  <Check className="w-4 h-4 text-green-600" />
                </div>
                <div>
                  <div className="font-semibold text-gray-900">Investment Scenarios</div>
                  <div className="text-sm text-gray-600">
                    Multiple exit strategies analyzed with profit projections and timelines
                  </div>
                </div>
              </div>

              <div className="flex items-start">
                <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center mr-3 mt-0.5 flex-shrink-0">
                  <Check className="w-4 h-4 text-green-600" />
                </div>
                <div>
                  <div className="font-semibold text-gray-900">Professional Excel Report</div>
                  <div className="text-sm text-gray-600">
                    Multi-sheet workbook ready for presentations and decision-making
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Property Info */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="text-sm font-semibold text-gray-900 mb-2">Property Details:</h4>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-gray-600">Address:</span>
                <div className="font-medium text-gray-900">{deal?.address || 'N/A'}</div>
              </div>
              <div>
                <span className="text-gray-600">Price:</span>
                <div className="font-medium text-gray-900">${deal?.price?.toLocaleString() || 'N/A'}</div>
              </div>
              <div>
                <span className="text-gray-600">Deal Score:</span>
                <div className="font-medium text-blue-600">{deal?.deal_score || 'N/A'}/100</div>
              </div>
              <div>
                <span className="text-gray-600">Strategy:</span>
                <div className="font-medium text-gray-900">
                  {deal?.preferred_strategy?.replace('_', ' ')?.toUpperCase() || 'N/A'}
                </div>
              </div>
            </div>
          </div>

          {/* Purchase Button */}
          <Button
            size="lg"
            onClick={handlePurchase}
            disabled={loading}
            className="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-lg py-6"
            data-testid="purchase-report-btn"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <CreditCard className="mr-2 h-5 w-5" />
                Purchase for $25.00
              </>
            )}
          </Button>

          <p className="text-xs text-gray-500 text-center">
            Secure payment powered by Stripe • Your card info is never stored on our servers
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
}
