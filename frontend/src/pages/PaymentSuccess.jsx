import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { API } from '../App';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CheckCircle, Download, Loader2, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';

export default function PaymentSuccess() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const sessionId = searchParams.get('session_id');
  
  const [status, setStatus] = useState('checking'); // checking, success, error
  const [paymentData, setPaymentData] = useState(null);
  const [downloading, setDownloading] = useState(false);
  const [pollCount, setPollCount] = useState(0);

  useEffect(() => {
    if (sessionId) {
      checkPaymentStatus();
    } else {
      setStatus('error');
    }
  }, [sessionId, pollCount]);

  const checkPaymentStatus = async () => {
    try {
      const response = await axios.get(`${API}/payments/status/${sessionId}`);
      
      if (response.data.payment_status === 'paid') {
        setStatus('success');
        setPaymentData(response.data);
        toast.success('Payment successful!');
      } else if (response.data.status === 'expired') {
        setStatus('error');
        toast.error('Payment session expired');
      } else if (pollCount < 5) {
        // Continue polling
        setTimeout(() => setPollCount(prev => prev + 1), 2000);
      } else {
        setStatus('error');
        toast.error('Unable to verify payment status');
      }
    } catch (error) {
      console.error('Error checking payment:', error);
      if (pollCount < 5) {
        setTimeout(() => setPollCount(prev => prev + 1), 2000);
      } else {
        setStatus('error');
        toast.error('Error verifying payment');
      }
    }
  };

  const handleDownload = async () => {
    try {
      setDownloading(true);
      
      const response = await axios.post(
        `${API}/payments/download-report`,
        { session_id: sessionId },
        { responseType: 'blob' }
      );
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      // Extract filename from content-disposition header if available
      const contentDisposition = response.headers['content-disposition'];
      const filename = contentDisposition
        ? contentDisposition.split('filename=')[1].replace(/"/g, '')
        : 'DealiQ_Report.xlsx';
      
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      toast.success('Report downloaded successfully!');
    } catch (error) {
      console.error('Download error:', error);
      toast.error('Failed to download report');
    } finally {
      setDownloading(false);
    }
  };

  if (status === 'checking') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md w-full">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Loader2 className="w-16 h-16 text-blue-600 animate-spin mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Verifying Payment...</h2>
            <p className="text-gray-600 text-center">
              Please wait while we confirm your payment
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (status === 'error') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <Card className="max-w-md w-full">
          <CardContent className="flex flex-col items-center justify-center py-12">
            <AlertCircle className="w-16 h-16 text-red-600 mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Payment Error</h2>
            <p className="text-gray-600 text-center mb-6">
              We couldn't verify your payment. Please contact support if you were charged.
            </p>
            <Button onClick={() => navigate('/deals')}>
              Return to Deals
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
      <Card className="max-w-2xl w-full">
        <CardHeader className="text-center border-b">
          <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="w-12 h-12 text-white" />
          </div>
          <CardTitle className="text-3xl font-bold text-gray-900">Payment Successful!</CardTitle>
          <p className="text-gray-600 mt-2">Thank you for your purchase</p>
        </CardHeader>
        
        <CardContent className="py-8">
          <div className="space-y-6">
            {/* Payment Details */}
            <div className="bg-gray-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Order Summary</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Product</span>
                  <span className="font-medium text-gray-900">Premium Deal Report</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Deal ID</span>
                  <span className="font-medium text-gray-900">{paymentData?.deal_id}</span>
                </div>
                <div className="flex justify-between pt-3 border-t">
                  <span className="text-gray-600">Amount Paid</span>
                  <span className="font-bold text-green-600 text-xl">$25.00</span>
                </div>
              </div>
            </div>

            {/* What's Included */}
            <div className="bg-blue-50 rounded-lg p-6 border-2 border-blue-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Your Report Includes:</h3>
              <ul className="space-y-2">
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">Comprehensive financial metrics and analysis</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">AI-powered insights and predictions</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">5 comparable properties (comps) analysis</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">Investment scenarios and ROI calculations</span>
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-5 h-5 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">Professional Excel report with multiple sheets</span>
                </li>
              </ul>
            </div>

            {/* Download Button */}
            <Button
              size="lg"
              onClick={handleDownload}
              disabled={downloading}
              className="w-full bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-lg py-6"
              data-testid="download-report-btn"
            >
              {downloading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Generating Report...
                </>
              ) : (
                <>
                  <Download className="mr-2 h-5 w-5" />
                  Download Your Report
                </>
              )}
            </Button>

            {/* Additional Actions */}
            <div className="flex space-x-4">
              <Button
                variant="outline"
                onClick={() => navigate('/deals')}
                className="flex-1"
              >
                View All Deals
              </Button>
              <Button
                variant="outline"
                onClick={() => navigate('/dashboard')}
                className="flex-1"
              >
                Go to Dashboard
              </Button>
            </div>

            {/* Support Note */}
            <p className="text-sm text-gray-500 text-center pt-4">
              Need help? Contact support at support@dealiq.com
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
