import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { TrendingUp, Home, DollarSign, BarChart3, Zap, Target, Check, Star, Upload, Filter, PieChart, FileSpreadsheet, Calculator, Clock, Shield, Users, ArrowRight, Sparkles, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

export default function SaaSLanding() {
  const navigate = useNavigate();
  const [activePricing, setActivePricing] = useState('monthly');

  // Load Stripe Buy Button script
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://js.stripe.com/v3/buy-button.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      // Cleanup script on unmount
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  const features = [
    {
      icon: <Upload className="w-6 h-6" />,
      title: "Bulk Deal Upload",
      description: "Upload Excel files with hundreds of deals and analyze them instantly"
    },
    {
      icon: <Calculator className="w-6 h-6" />,
      title: "Smart Scoring Algorithm",
      description: "Proprietary scoring system (0-100) for residential, commercial, land, and parks"
    },
    {
      icon: <Target className="w-6 h-6" />,
      title: "Strategy Recommendations",
      description: "Get AI-powered investment strategy suggestions for each deal"
    },
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: "Advanced Analytics",
      description: "Portfolio insights, market trends, and performance tracking"
    },
    {
      icon: <Filter className="w-6 h-6" />,
      title: "Powerful Filtering",
      description: "Filter by strategy, property type, score, location, and metrics"
    },
    {
      icon: <Clock className="w-6 h-6" />,
      title: "Real-time Analysis",
      description: "Instant calculations for Cap Rate, CoC, NOI, cash flow, and ARV"
    }
  ];

  const metrics = [
    { value: "10x", label: "Faster Than Spreadsheets" },
    { value: "127", label: "Property Types Supported" },
    { value: "15+", label: "Financial Metrics Calculated" },
    { value: "100%", label: "Accurate Scoring" }
  ];

  const pricingPlans = {
    monthly: [
      {
        name: "Starter",
        price: "49",
        period: "month",
        description: "Perfect for new investors analyzing their first deals",
        features: [
          "Analyze up to 50 deals/month",
          "Basic financial metrics",
          "Deal scoring algorithm",
          "Export to CSV",
          "Email support"
        ],
        cta: "Start Free Trial",
        popular: false,
        stripeBuyButton: true
      },
      {
        name: "Professional",
        price: "149",
        period: "month",
        description: "For active investors managing multiple deals",
        features: [
          "Analyze unlimited deals",
          "Advanced analytics dashboard",
          "Strategy recommendations",
          "Portfolio tracking",
          "Priority email support",
          "API access"
        ],
        cta: "Start Free Trial",
        popular: true,
        stripeBuyButton: true,
        stripeBuyButtonId: "buy_btn_1SSUsfBgzLEFvozzuKHtoNNv"
      },
      {
        name: "Enterprise",
        price: "499",
        period: "month",
        description: "For investment firms and large portfolios",
        features: [
          "Everything in Professional",
          "White-label option",
          "Custom integrations",
          "Dedicated account manager",
          "Custom scoring models",
          "Phone support"
        ],
        cta: "Contact Sales",
        popular: false
      }
    ],
    annual: [
      {
        name: "Starter",
        price: "39",
        period: "month",
        description: "Perfect for new investors analyzing their first deals",
        features: [
          "Analyze up to 50 deals/month",
          "Basic financial metrics",
          "Deal scoring algorithm",
          "Export to CSV",
          "Email support"
        ],
        cta: "Start Free Trial",
        popular: false,
        savings: "Save $120/year",
        stripeBuyButton: true
      },
      {
        name: "Professional",
        price: "119",
        period: "month",
        description: "For active investors managing multiple deals",
        features: [
          "Analyze unlimited deals",
          "Advanced analytics dashboard",
          "Strategy recommendations",
          "Portfolio tracking",
          "Priority email support",
          "API access"
        ],
        cta: "Start Free Trial",
        popular: true,
        savings: "Save $360/year",
        stripeBuyButton: true,
        stripeBuyButtonId: "buy_btn_1SSUsfBgzLEFvozzuKHtoNNv"
      },
      {
        name: "Enterprise",
        price: "399",
        period: "month",
        description: "For investment firms and large portfolios",
        features: [
          "Everything in Professional",
          "White-label option",
          "Custom integrations",
          "Dedicated account manager",
          "Custom scoring models",
          "Phone support"
        ],
        cta: "Contact Sales",
        popular: false,
        savings: "Save $1,200/year"
      }
    ]
  };

  const testimonials = [
    {
      name: "Sarah Johnson",
      role: "Real Estate Investor",
      company: "Phoenix Properties LLC",
      quote: "DealiQ Pro has completely transformed how I analyze deals. What used to take me hours now takes minutes. The scoring system is incredibly accurate.",
      rating: 5
    },
    {
      name: "Michael Chen",
      role: "Portfolio Manager",
      company: "Southwest Investments",
      quote: "We analyze 200+ deals per month. DealiQ Pro's bulk upload and filtering features have been a game-changer for our team's efficiency.",
      rating: 5
    },
    {
      name: "Lisa Rodriguez",
      role: "Fix & Flip Specialist",
      company: "Desert Homes Inc",
      quote: "The strategy recommendations are spot-on. It's like having an experienced investor advising you on every deal. Highly recommend!",
      rating: 5
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3 cursor-pointer" onClick={() => navigate('/')}>
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Home className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">DealiQ Pro</span>
            </div>
            
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-blue-600 transition font-medium">Features</a>
              <a href="#pricing" className="text-gray-600 hover:text-blue-600 transition font-medium">Pricing</a>
              <a href="#testimonials" className="text-gray-600 hover:text-blue-600 transition font-medium">Testimonials</a>
              <Button variant="ghost" onClick={() => navigate('/dashboard')}>Sign In</Button>
              <Button 
                onClick={() => navigate('/dashboard')}
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white"
              >
                Try Free Demo
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="pt-24 pb-20 bg-gradient-to-br from-blue-50 via-purple-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <Badge className="mb-6 bg-blue-100 text-blue-700 hover:bg-blue-200">
              <Sparkles className="w-4 h-4 mr-2" />
              AI-Powered Deal Analysis
            </Badge>
            <h1 className="text-6xl lg:text-7xl font-bold text-gray-900 mb-6">
              Analyze Real Estate Deals
              <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                In Seconds, Not Hours
              </span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-10">
              Upload your property list, get instant scoring, financial projections, and investment strategies. 
              Make confident decisions backed by data.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                size="lg" 
                onClick={() => navigate('/dashboard')}
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white text-lg px-8 py-6 hover:shadow-xl"
              >
                Start Free Trial
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
              <Button 
                size="lg" 
                variant="outline"
                onClick={() => navigate('/dashboard')}
                className="text-lg px-8 py-6"
              >
                <Upload className="mr-2 w-5 h-5" />
                Try Demo with Sample Data
              </Button>
            </div>
          </div>

          {/* Metrics */}
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 mt-16">
            {metrics.map((metric, idx) => (
              <div key={idx} className="text-center">
                <div className="text-4xl font-bold text-gray-900 mb-2">{metric.value}</div>
                <div className="text-sm text-gray-600">{metric.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Everything You Need to Analyze Deals</h2>
            <p className="text-xl text-gray-600">Powerful features designed for real estate investors</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, idx) => (
              <div key={idx} className="p-6 rounded-xl border border-gray-200 hover:shadow-lg transition">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center text-white mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* How It Works */}
      <div className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-xl text-gray-600">Get started in 3 simple steps</p>
          </div>

          <div className="grid md:grid-cols-3 gap-12">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-6">
                1
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Upload Your Deals</h3>
              <p className="text-gray-600">Drop your Excel file with property details. Support for all standard formats.</p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-6">
                2
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Instant Analysis</h3>
              <p className="text-gray-600">Our AI analyzes each deal, calculating 15+ metrics and scoring opportunities.</p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-600 to-purple-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-6">
                3
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Make Decisions</h3>
              <p className="text-gray-600">Filter, sort, and compare deals. Get strategy recommendations instantly.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Pricing Section */}
      <div id="pricing" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Simple, Transparent Pricing</h2>
            <p className="text-xl text-gray-600 mb-8">Choose the plan that fits your needs</p>
            
            {/* Pricing Toggle */}
            <div className="inline-flex bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setActivePricing('monthly')}
                className={`px-6 py-2 rounded-md font-medium transition ${
                  activePricing === 'monthly' ? 'bg-white text-gray-900 shadow' : 'text-gray-600'
                }`}
              >
                Monthly
              </button>
              <button
                onClick={() => setActivePricing('annual')}
                className={`px-6 py-2 rounded-md font-medium transition ${
                  activePricing === 'annual' ? 'bg-white text-gray-900 shadow' : 'text-gray-600'
                }`}
              >
                Annual
                <Badge className="ml-2 bg-green-100 text-green-700">Save 20%</Badge>
              </button>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {pricingPlans[activePricing].map((plan, idx) => (
              <div
                key={idx}
                className={`rounded-2xl p-8 ${
                  plan.popular
                    ? 'bg-gradient-to-br from-blue-600 to-purple-600 text-white shadow-2xl scale-105'
                    : 'bg-white border-2 border-gray-200'
                }`}
              >
                {plan.popular && (
                  <Badge className="mb-4 bg-white/20 text-white border-white/30">
                    Most Popular
                  </Badge>
                )}
                <h3 className={`text-2xl font-bold mb-2 ${plan.popular ? 'text-white' : 'text-gray-900'}`}>
                  {plan.name}
                </h3>
                <p className={`mb-6 ${plan.popular ? 'text-blue-100' : 'text-gray-600'}`}>
                  {plan.description}
                </p>
                <div className="mb-6">
                  <span className={`text-5xl font-bold ${plan.popular ? 'text-white' : 'text-gray-900'}`}>
                    ${plan.price}
                  </span>
                  <span className={`${plan.popular ? 'text-blue-100' : 'text-gray-600'}`}>
                    /{plan.period}
                  </span>
                  {plan.savings && (
                    <div className="text-sm text-green-300 mt-2">{plan.savings}</div>
                  )}
                </div>
                {plan.stripeBuyButton ? (
                  <div className="mb-6" data-testid="stripe-buy-button">
                    <stripe-buy-button
                      buy-button-id="buy_btn_1SSUq5BgzLEFvozzksgqTg00"
                      publishable-key="pk_live_51SSTnVBgzLEFvozzZLSce2x3zFnoMqx3SBGJVeuYM0y8dLETcozDAOWFLXil18lxARueT9gjupFhhSoEKrmVQWcm00Y9MF05LG"
                    >
                    </stripe-buy-button>
                  </div>
                ) : (
                  <Button
                    className={`w-full mb-6 ${
                      plan.popular
                        ? 'bg-white text-blue-600 hover:bg-gray-100'
                        : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                    }`}
                    onClick={() => navigate('/dashboard')}
                  >
                    {plan.cta}
                  </Button>
                )}
                <ul className="space-y-3">
                  {plan.features.map((feature, fIdx) => (
                    <li key={fIdx} className="flex items-start">
                      <Check className={`w-5 h-5 mr-3 flex-shrink-0 ${plan.popular ? 'text-white' : 'text-green-600'}`} />
                      <span className={plan.popular ? 'text-blue-50' : 'text-gray-600'}>{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Testimonials */}
      <div id="testimonials" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Trusted by Investors</h2>
            <p className="text-xl text-gray-600">See what our customers are saying</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, idx) => (
              <div key={idx} className="bg-white rounded-xl p-8 shadow-lg">
                <div className="flex mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-700 mb-6 italic">"{testimonial.quote}"</p>
                <div>
                  <div className="font-bold text-gray-900">{testimonial.name}</div>
                  <div className="text-sm text-gray-600">{testimonial.role}</div>
                  <div className="text-sm text-blue-600">{testimonial.company}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-5xl font-bold mb-6">
            Ready to Analyze Your First Deal?
          </h2>
          <p className="text-2xl text-blue-100 mb-10">
            Start your 14-day free trial. No credit card required.
          </p>
          <Button
            size="lg"
            onClick={() => navigate('/dashboard')}
            className="bg-white text-blue-600 hover:bg-gray-100 text-xl px-10 py-6"
          >
            Start Free Trial
            <ChevronRight className="ml-2 w-6 h-6" />
          </Button>
          <div className="flex items-center justify-center space-x-8 mt-8 text-blue-100">
            <div className="flex items-center">
              <Check className="w-5 h-5 mr-2" />
              14-day free trial
            </div>
            <div className="flex items-center">
              <Check className="w-5 h-5 mr-2" />
              No credit card required
            </div>
            <div className="flex items-center">
              <Check className="w-5 h-5 mr-2" />
              Cancel anytime
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <Home className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">DealiQ Pro</span>
            </div>
            <div className="text-sm">
              &copy; 2025 DealiQ Pro. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
