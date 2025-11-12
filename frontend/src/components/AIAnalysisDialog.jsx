import { useState } from 'react';
import axios from 'axios';
import { API } from '../App';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Sparkles, TrendingUp, TrendingDown, AlertTriangle, Target, Lightbulb, Activity, Loader2, CheckCircle } from 'lucide-react';
import { toast } from 'sonner';

export default function AIAnalysisDialog({ deal, open, onOpenChange }) {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAIAnalysis = async () => {
    if (!deal) return;
    
    try {
      setLoading(true);
      const response = await axios.post(`${API}/deals/${deal.id}/ai-analysis`);
      setAnalysis(response.data);
      toast.success('AI analysis complete!');
    } catch (error) {
      console.error('Error fetching AI analysis:', error);
      toast.error('Failed to generate AI analysis');
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = (isOpen) => {
    onOpenChange(isOpen);
    if (isOpen && !analysis) {
      fetchAIAnalysis();
    }
  };

  const getPredictionColor = (prediction) => {
    if (prediction === 'bullish') return 'bg-green-100 text-green-800 border-green-300';
    if (prediction === 'bearish') return 'bg-red-100 text-red-800 border-red-300';
    return 'bg-yellow-100 text-yellow-800 border-yellow-300';
  };

  const getPredictionIcon = (prediction) => {
    if (prediction === 'bullish') return <TrendingUp className="w-5 h-5" />;
    if (prediction === 'bearish') return <TrendingDown className="w-5 h-5" />;
    return <Activity className="w-5 h-5" />;
  };

  const getSeverityColor = (severity) => {
    if (severity === 'high') return 'bg-red-100 text-red-800';
    if (severity === 'medium') return 'bg-yellow-100 text-yellow-800';
    return 'bg-blue-100 text-blue-800';
  };

  const getPotentialColor = (potential) => {
    if (potential === 'high') return 'bg-green-100 text-green-800';
    if (potential === 'medium') return 'bg-blue-100 text-blue-800';
    return 'bg-gray-100 text-gray-800';
  };

  return (
    <Dialog open={open} onOpenChange={handleOpen}>
      <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-12">
            <Loader2 className="w-12 h-12 text-blue-600 animate-spin mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Analyzing Deal with AI...</h3>
            <p className="text-gray-600">Our AI is reviewing all metrics and market data</p>
          </div>
        ) : analysis ? (
          <>
            <DialogHeader>
              <div className="flex items-center space-x-3 mb-2">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
                  <Sparkles className="w-7 h-7 text-white" />
                </div>
                <div>
                  <DialogTitle className="text-2xl">AI Predictive Analysis</DialogTitle>
                  <DialogDescription>
                    {deal?.address || 'Property Analysis'}
                  </DialogDescription>
                </div>
              </div>
            </DialogHeader>

            <div className="space-y-6">
              {/* AI Confidence Score & Prediction */}
              <div className="grid md:grid-cols-2 gap-4">
                <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6 border-2 border-blue-200">
                  <div className="text-sm text-gray-600 mb-2">AI Confidence Score</div>
                  <div className="flex items-end space-x-3">
                    <div className="text-5xl font-bold text-blue-600">{analysis.ai_confidence_score}</div>
                    <div className="text-2xl text-gray-500 mb-2">/100</div>
                  </div>
                  <div className="mt-4 bg-gray-200 rounded-full h-3">
                    <div
                      className="bg-gradient-to-r from-blue-600 to-purple-600 h-3 rounded-full transition-all"
                      style={{ width: `${analysis.ai_confidence_score}%` }}
                    ></div>
                  </div>
                </div>

                <div className={`rounded-xl p-6 border-2 ${getPredictionColor(analysis.prediction)}`}>
                  <div className="text-sm font-medium mb-2">Investment Outlook</div>
                  <div className="flex items-center space-x-3">
                    {getPredictionIcon(analysis.prediction)}
                    <div className="text-3xl font-bold uppercase">{analysis.prediction}</div>
                  </div>
                  <p className="mt-4 text-sm">{analysis.market_outlook}</p>
                </div>
              </div>

              {/* Key Insights */}
              <div>
                <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                  <CheckCircle className="w-5 h-5 mr-2 text-blue-600" />
                  Key Insights
                </h3>
                <div className="space-y-2">
                  {analysis.key_insights.map((insight, idx) => (
                    <Alert key={idx} className="bg-blue-50 border-blue-200">
                      <AlertDescription className="flex items-start">
                        <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs mr-3 mt-0.5 flex-shrink-0">
                          {idx + 1}
                        </div>
                        <span className="text-gray-700">{insight}</span>
                      </AlertDescription>
                    </Alert>
                  ))}
                </div>
              </div>

              {/* Risk Factors */}
              <div>
                <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                  <AlertTriangle className="w-5 h-5 mr-2 text-red-600" />
                  Risk Factors
                </h3>
                <div className="grid md:grid-cols-2 gap-4">
                  {analysis.risk_factors.map((risk, idx) => (
                    <div key={idx} className="bg-white rounded-lg border-2 border-red-200 p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold text-gray-900">{risk.factor}</span>
                        <Badge className={getSeverityColor(risk.severity)}>
                          {risk.severity}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600">{risk.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Opportunities */}
              <div>
                <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                  <Target className="w-5 h-5 mr-2 text-green-600" />
                  Opportunities
                </h3>
                <div className="grid md:grid-cols-2 gap-4">
                  {analysis.opportunities.map((opp, idx) => (
                    <div key={idx} className="bg-white rounded-lg border-2 border-green-200 p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-semibold text-gray-900">{opp.opportunity}</span>
                        <Badge className={getPotentialColor(opp.potential)}>
                          {opp.potential} potential
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600">{opp.description}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div>
                <h3 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
                  <Lightbulb className="w-5 h-5 mr-2 text-yellow-600" />
                  AI Recommendations
                </h3>
                <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl p-6 border-2 border-yellow-200">
                  <ul className="space-y-3">
                    {analysis.recommendations.map((rec, idx) => (
                      <li key={idx} className="flex items-start">
                        <div className="w-6 h-6 bg-yellow-500 text-white rounded-full flex items-center justify-center text-xs mr-3 mt-0.5 flex-shrink-0">
                          {idx + 1}
                        </div>
                        <span className="text-gray-700">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Investment Strategy */}
              <div className="bg-gradient-to-br from-purple-50 to-blue-50 rounded-xl p-6 border-2 border-purple-200">
                <h3 className="text-lg font-bold text-gray-900 mb-2">Recommended Investment Strategy</h3>
                <p className="text-gray-700 text-lg">{analysis.investment_strategy}</p>
              </div>

              {/* Footer */}
              <div className="border-t pt-4">
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <div className="flex items-center">
                    <Sparkles className="w-4 h-4 mr-2" />
                    <span>Powered by {analysis.model}</span>
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => fetchAIAnalysis()}
                    size="sm"
                  >
                    Refresh Analysis
                  </Button>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="py-12 text-center">
            <p className="text-gray-600">No analysis available</p>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
