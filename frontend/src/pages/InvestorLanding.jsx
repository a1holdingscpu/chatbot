import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { TrendingUp, Home, DollarSign, BarChart3, MapPin, Users, ChevronRight, Menu, X, Check, Star, Play, Award, Shield, Zap, Target, ArrowRight, Building2, Calculator, Clock, Mail, Phone, MessageSquare, PieChart, TrendingDown, Activity, Briefcase, FileText, Globe } from 'lucide-react';

export default function InvestorLanding() {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [selectedDeal, setSelectedDeal] = useState(null);
  
  // Animated metrics
  const [metrics, setMetrics] = useState({
    portfolioValue: 0,
    activeDeals: 0,
    avgROI: 0,
    totalReturns: 0
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        portfolioValue: Math.min(prev.portfolioValue + 50000, 8500000),
        activeDeals: Math.min(prev.activeDeals + 1, 47),
        avgROI: Math.min(prev.avgROI + 0.5, 28.4),
        totalReturns: Math.min(prev.totalReturns + 25000, 2340000)
      }));
    }, 20);
    return () => clearInterval(interval);
  }, []);

  const activePipeline = [
    {
      id: 1,
      address: "3847 E Desert Inn Rd, Las Vegas, NV",
      type: "Fix & Flip",
      status: "Under Contract",
      purchase: 285000,
      arv: 425000,
      rehab: 42000,
      profit: 98000,
      roi: 30.2,
      timeline: "90 days",
      equity: 140000,
      stage: "Acquisition"
    },
    {
      id: 2,
      address: "1523 W University Dr, Tempe, AZ",
      type: "Buy & Hold Rental",
      status: "In Rehab",
      purchase: 340000,
      arv: 480000,
      rehab: 55000,
      profit: 85000,
      roi: 21.5,
      timeline: "120 days",
      equity: 140000,
      stage: "Renovation"
    },
    {
      id: 3,
      address: "892 N Scottsdale Rd, Scottsdale, AZ",
      type: "Wholesale Deal",
      status: "Active",
      purchase: 195000,
      arv: 315000,
      rehab: 35000,
      profit: 85000,
      roi: 37.0,
      timeline: "30 days",
      equity: 120000,
      stage: "Marketing"
    },
    {
      id: 4,
      address: "4521 S Mill Ave, Tempe, AZ",
      type: "Multi-Family",
      status: "Analyzing",
      purchase: 890000,
      arv: 1250000,
      rehab: 125000,
      profit: 235000,
      roi: 23.2,
      timeline: "180 days",
      equity: 360000,
      stage: "Due Diligence"
    }
  ];

  const portfolioPerformance = [
    { quarter: "Q4 2024", deals: 12, revenue: 487000, roi: 26.8 },
    { quarter: "Q3 2024", deals: 9, revenue: 342000, roi: 24.3 },
    { quarter: "Q2 2024", deals: 11, revenue: 521000, roi: 29.1 },
    { quarter: "Q1 2024", deals: 8, revenue: 298000, roi: 22.7 }
  ];

  const marketData = [
    { market: "Phoenix Metro", deals: 23, avgROI: 28.4, growth: "+12.3%" },
    { market: "Tempe", deals: 15, avgROI: 31.2, growth: "+15.7%" },
    { market: "Scottsdale", deals: 9, avgROI: 25.8, growth: "+8.2%" },
    { market: "Nationwide", deals: 47, avgROI: 27.1, growth: "+10.5%" }
  ];

  const investmentOpportunities = [
    {
      title: "Private Money Partnership",
      minInvestment: 50000,
      targetReturn: "12-15% Annual",
      term: "12 months",
      security: "First lien position",
      description: "Secure lending on vetted deals with equity cushion"
    },
    {
      title: "Joint Venture Equity",
      minInvestment: 100000,
      targetReturn: "25-35% ROI",
      term: "6-12 months",
      security: "Equity partnership",
      description: "Co-invest on high-ROI fix & flip opportunities"
    },
    {
      title: "Portfolio Fund",
      minInvestment: 250000,
      targetReturn: "18-22% Annual",
      term: "24 months",
      security: "Diversified portfolio",
      description: "Invest across multiple deals for reduced risk"
    }
  ];

  const testimonials = [
    {
      name: "Robert Martinez",
      role: "Private Lender",
      amount: "$500K Deployed",
      quote: "I've funded 8 deals with DealiQ. Every loan has been repaid on time with the promised returns. Professional operation.",
      returns: "14.2% average return"
    },
    {
      name: "Jennifer Wu",
      role: "JV Partner",
      amount: "6 Deals Together",
      quote: "The transparency and deal flow is incredible. We've partnered on 6 properties with an average 29% ROI per deal.",
      returns: "29% average ROI"
    },
    {
      name: "David Thompson",
      role: "Fund Investor",
      amount: "$750K Investment",
      quote: "Best decision I made was investing in their portfolio fund. Consistent returns, monthly updates, zero headaches.",
      returns: "19.8% annual return"
    }
  ];

  const companyMetrics = {
    founded: "2021",
    totalDeals: 127,
    successRate: 94,
    avgDealTime: 87,
    totalVolume: 18500000,
    activeInvestors: 34,
    avgInvestorReturn: 23.7,
    repeatInvestorRate: 89
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white shadow-md z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Home className="w-6 h-6 text-white" />
              </div>
              <div>
                <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">DealiQ</span>
                <div className="text-xs text-gray-500">Investor Portal</div>
              </div>
            </div>
            
            <div className="hidden lg:flex items-center space-x-8">
              <a href="#overview" className="text-gray-700 hover:text-blue-600 transition font-medium">Overview</a>
              <a href="#pipeline" className="text-gray-700 hover:text-blue-600 transition font-medium">Active Deals</a>
              <a href="#performance" className="text-gray-700 hover:text-blue-600 transition font-medium">Performance</a>
              <a href="#opportunities" className="text-gray-700 hover:text-blue-600 transition font-medium">Invest</a>
              <button 
                onClick={() => navigate('/dashboard')}
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition font-medium"
              >
                <Calculator className="inline w-4 h-4 mr-2" />
                Deal Analyzer
              </button>
              <button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-lg hover:shadow-lg transition font-semibold">
                Schedule Call
              </button>
            </div>

            <button className="lg:hidden" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Dashboard */}
      <div className="pt-24 pb-12 bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <div className="inline-flex items-center space-x-2 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-semibold mb-6">
              <Activity className="w-4 h-4" />
              <span>Live Investment Dashboard</span>
            </div>
            <h1 className="text-5xl lg:text-6xl font-bold mb-4">
              Institutional-Grade Real Estate Returns
            </h1>
            <p className="text-xl text-blue-100 max-w-3xl mx-auto">
              Nationwide deal flow with Las Vegas Metro hyperfocus. Transparent operations. Proven track record.
            </p>
          </div>

          {/* Key Metrics Dashboard */}
          <div className="grid md:grid-cols-4 gap-6">
            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
              <div className="flex items-center justify-between mb-2">
                <Building2 className="w-8 h-8" />
                <TrendingUp className="w-5 h-5 text-green-300" />
              </div>
              <div className="text-3xl font-bold mb-1">${(metrics.portfolioValue / 1000000).toFixed(1)}M</div>
              <div className="text-sm text-blue-100">Active Portfolio Value</div>
            </div>

            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
              <div className="flex items-center justify-between mb-2">
                <Briefcase className="w-8 h-8" />
                <Activity className="w-5 h-5 text-green-300" />
              </div>
              <div className="text-3xl font-bold mb-1">{metrics.activeDeals}</div>
              <div className="text-sm text-blue-100">Active Deals in Pipeline</div>
            </div>

            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
              <div className="flex items-center justify-between mb-2">
                <BarChart3 className="w-8 h-8" />
                <TrendingUp className="w-5 h-5 text-green-300" />
              </div>
              <div className="text-3xl font-bold mb-1">{metrics.avgROI.toFixed(1)}%</div>
              <div className="text-sm text-blue-100">Average Deal ROI</div>
            </div>

            <div className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20">
              <div className="flex items-center justify-between mb-2">
                <DollarSign className="w-8 h-8" />
                <TrendingUp className="w-5 h-5 text-green-300" />
              </div>
              <div className="text-3xl font-bold mb-1">${(metrics.totalReturns / 1000000).toFixed(1)}M</div>
              <div className="text-sm text-blue-100">Total Investor Returns</div>
            </div>
          </div>
        </div>
      </div>

      {/* Company Track Record */}
      <div className="py-12 bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Our Track Record</h2>
            <p className="text-gray-600">Proven performance since {companyMetrics.founded}</p>
          </div>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="text-center p-6 bg-gray-50 rounded-xl">
              <div className="text-4xl font-bold text-blue-600 mb-2">{companyMetrics.totalDeals}</div>
              <div className="text-sm text-gray-600">Total Deals Closed</div>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-xl">
              <div className="text-4xl font-bold text-green-600 mb-2">{companyMetrics.successRate}%</div>
              <div className="text-sm text-gray-600">Success Rate</div>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-xl">
              <div className="text-4xl font-bold text-purple-600 mb-2">${(companyMetrics.totalVolume / 1000000).toFixed(1)}M</div>
              <div className="text-sm text-gray-600">Total Volume</div>
            </div>
            <div className="text-center p-6 bg-gray-50 rounded-xl">
              <div className="text-4xl font-bold text-blue-600 mb-2">{companyMetrics.activeInvestors}</div>
              <div className="text-sm text-gray-600">Active Investors</div>
            </div>
          </div>
        </div>
      </div>

      {/* Active Pipeline - Shortened version */}
      <div id="pipeline" className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Active Deal Pipeline</h2>
              <p className="text-gray-600">Current opportunities in various stages</p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">Total Pipeline Value</div>
              <div className="text-2xl font-bold text-blue-600">$1.7M</div>
            </div>
          </div>

          <div className="grid lg:grid-cols-2 gap-6">
            {activePipeline.slice(0, 2).map((deal) => (
              <div key={deal.id} className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition">
                <div className="bg-gradient-to-r from-blue-600 to-purple-600 px-6 py-4 text-white">
                  <div className="flex justify-between items-start mb-2">
                    <div>
                      <div className="text-sm opacity-90 mb-1">{deal.type}</div>
                      <div className="font-bold text-lg">{deal.address}</div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      deal.status === 'Under Contract' ? 'bg-green-400 text-green-900' :
                      deal.status === 'In Rehab' ? 'bg-yellow-400 text-yellow-900' :
                      'bg-blue-400 text-blue-900'
                    }`}>
                      {deal.status}
                    </span>
                  </div>
                </div>

                <div className="p-6">
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <div className="text-sm text-gray-500 mb-1">Purchase Price</div>
                      <div className="text-xl font-bold text-gray-900">${deal.purchase.toLocaleString()}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500 mb-1">Target ROI</div>
                      <div className="text-xl font-bold text-blue-600">{deal.roi}%</div>
                    </div>
                  </div>

                  <button 
                    onClick={() => setSelectedDeal(deal)}
                    className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition"
                  >
                    View Full Analysis
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <h2 className="text-5xl font-bold mb-6">
            Ready to Partner With Us?
          </h2>
          <p className="text-2xl text-blue-100 mb-8">
            Join {companyMetrics.activeInvestors} investors earning an average of {companyMetrics.avgInvestorReturn}% returns
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <button className="bg-white text-blue-600 px-10 py-5 rounded-lg text-xl font-bold hover:shadow-2xl transition transform hover:scale-105">
              Schedule Investor Call
            </button>
            <button 
              onClick={() => navigate('/dashboard')}
              className="border-2 border-white text-white px-10 py-5 rounded-lg text-xl font-bold hover:bg-white/10 transition flex items-center justify-center"
            >
              <Calculator className="w-6 h-6 mr-2" />
              Try Deal Analyzer
            </button>
          </div>
          <div className="flex items-center justify-center space-x-8 text-white/90">
            <div className="flex items-center">
              <Check className="w-5 h-5 mr-2" />
              No fees to explore
            </div>
            <div className="flex items-center">
              <Check className="w-5 h-5 mr-2" />
              Flexible investment sizes
            </div>
            <div className="flex items-center">
              <Check className="w-5 h-5 mr-2" />
              Full transparency
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 mb-12">
            <div className="md:col-span-2">
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <Home className="w-6 h-6 text-white" />
                </div>
                <span className="text-2xl font-bold text-white">DealiQ</span>
              </div>
              <p className="text-sm mb-6 max-w-md">
                Professional real estate investment firm focused on high-ROI opportunities in Phoenix Metro and nationwide markets. 
                Transparent operations, proven track record, institutional-grade returns.
              </p>
            </div>
            
            <div>
              <h4 className="text-white font-semibold mb-4">For Investors</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#overview" className="hover:text-white transition">Investment Overview</a></li>
                <li><a href="#pipeline" className="hover:text-white transition">Active Deals</a></li>
                <li><button onClick={() => navigate('/dashboard')} className="hover:text-white transition">Deal Analyzer Tool</button></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-white font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition">About DealiQ</a></li>
                <li><a href="#" className="hover:text-white transition">Contact Us</a></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 pt-8">
            <div className="flex flex-col md:flex-row justify-between items-center text-sm">
              <p>&copy; 2025 DealiQ Investment Group, LLC. All rights reserved.</p>
            </div>
            <div className="mt-4 text-xs text-gray-500 text-center md:text-left">
              <p>This is a demo platform for investor presentations. Past performance does not guarantee future results.</p>
            </div>
          </div>
        </div>
      </footer>

      {/* Deal Details Modal */}
      {selectedDeal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={() => setSelectedDeal(null)}>
          <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-6 flex justify-between items-center">
              <div>
                <h3 className="text-2xl font-bold">{selectedDeal.address}</h3>
                <p className="text-blue-100">{selectedDeal.type}</p>
              </div>
              <button onClick={() => setSelectedDeal(null)} className="text-white hover:bg-white/20 p-2 rounded-lg transition">
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <div className="p-8">
              <div className="grid md:grid-cols-2 gap-8 mb-8">
                <div>
                  <h4 className="text-xl font-bold text-gray-900 mb-4">Financial Overview</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="text-gray-600">Purchase Price</span>
                      <span className="font-bold">${selectedDeal.purchase.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="text-gray-600">Rehab Budget</span>
                      <span className="font-bold">${selectedDeal.rehab.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between p-3 bg-green-50 rounded-lg border border-green-200">
                      <span className="text-gray-700 font-semibold">Projected Profit</span>
                      <span className="font-bold text-green-600">${selectedDeal.profit.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between p-3 bg-blue-50 rounded-lg border border-blue-200">
                      <span className="text-gray-700 font-semibold">Target ROI</span>
                      <span className="font-bold text-blue-600">{selectedDeal.roi}%</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h4 className="text-xl font-bold text-gray-900 mb-4">Deal Status</h4>
                  <div className="space-y-4">
                    <div className="p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Current Stage</div>
                      <div className="text-xl font-bold text-gray-900">{selectedDeal.stage}</div>
                    </div>
                    <div className="p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Status</div>
                      <div className="text-xl font-bold text-gray-900">{selectedDeal.status}</div>
                    </div>
                    <div className="p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Timeline</div>
                      <div className="text-xl font-bold text-gray-900">{selectedDeal.timeline}</div>
                    </div>
                  </div>
                </div>
              </div>
              
              <button className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 rounded-lg text-lg font-semibold hover:shadow-xl transition">
                Request Full Investment Package
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
