import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API } from '../App';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Upload, FileSpreadsheet, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

export default function UploadPage() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (!selectedFile.name.match(/\.(xlsx|xls)$/)) {
        toast.error('Please select an Excel file (.xlsx or .xls)');
        return;
      }
      setFile(selectedFile);
      setResult(null);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files?.[0];
    if (droppedFile) {
      if (!droppedFile.name.match(/\.(xlsx|xls)$/)) {
        toast.error('Please select an Excel file (.xlsx or .xls)');
        return;
      }
      setFile(droppedFile);
      setResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a file first');
      return;
    }

    try {
      setUploading(true);
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${API}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setResult(response.data);
      toast.success(response.data.message);
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.detail || 'Failed to upload and analyze file');
    } finally {
      setUploading(false);
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

  return (
    <div className="container mx-auto px-4 py-8" data-testid="upload-page">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Upload Deals</h1>
          <p className="text-gray-600">Upload an Excel file with real estate deal data for instant analysis</p>
        </div>

        {/* Upload Card */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Select File</CardTitle>
            <CardDescription>Upload .xlsx or .xls files containing your real estate deals</CardDescription>
          </CardHeader>
          <CardContent>
            <div
              className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-500 transition-colors cursor-pointer"
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
              onClick={() => fileInputRef.current?.click()}
              data-testid="upload-dropzone"
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileSelect}
                className="hidden"
                data-testid="file-input"
              />
              
              {file ? (
                <div className="flex flex-col items-center">
                  <FileSpreadsheet className="h-16 w-16 text-green-600 mb-4" />
                  <p className="text-lg font-semibold text-gray-900 mb-2">{file.name}</p>
                  <p className="text-sm text-gray-500 mb-4">
                    {(file.size / 1024).toFixed(2)} KB
                  </p>
                  <Button
                    variant="outline"
                    onClick={(e) => {
                      e.stopPropagation();
                      setFile(null);
                      setResult(null);
                    }}
                  >
                    Remove
                  </Button>
                </div>
              ) : (
                <div>
                  <Upload className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-lg font-semibold text-gray-700 mb-2">
                    Drop your Excel file here or click to browse
                  </p>
                  <p className="text-sm text-gray-500">
                    Supported formats: .xlsx, .xls
                  </p>
                </div>
              )}
            </div>

            {file && (
              <div className="mt-6 flex justify-center">
                <Button
                  size="lg"
                  onClick={handleUpload}
                  disabled={uploading}
                  className="bg-blue-600 hover:bg-blue-700"
                  data-testid="upload-analyze-btn"
                >
                  {uploading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Upload className="mr-2 h-5 w-5" />
                      Upload & Analyze
                    </>
                  )}
                </Button>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Results */}
        {result && result.success && (
          <Card className="border-green-200 bg-green-50" data-testid="upload-results">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <CheckCircle className="h-6 w-6 text-green-600" />
                <div>
                  <CardTitle className="text-green-900">Analysis Complete!</CardTitle>
                  <CardDescription className="text-green-700">
                    Successfully analyzed {result.deals_count} deals
                  </CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex space-x-4">
                  <Button
                    onClick={() => navigate('/deals')}
                    className="bg-green-600 hover:bg-green-700"
                    data-testid="view-deals-btn"
                  >
                    View All Deals
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => navigate('/analytics')}
                    data-testid="view-analytics-btn"
                  >
                    View Analytics
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setFile(null);
                      setResult(null);
                    }}
                  >
                    Upload Another
                  </Button>
                </div>

                {result.top_deals && result.top_deals.length > 0 && (
                  <div className="mt-6">
                    <h4 className="font-semibold text-gray-900 mb-3">Top 5 Deals Preview</h4>
                    <div className="space-y-3">
                      {result.top_deals.slice(0, 5).map((deal) => (
                        <div
                          key={deal.id}
                          className="bg-white p-4 rounded-lg border flex items-center justify-between"
                          data-testid={`preview-deal-${deal.id}`}
                        >
                          <div>
                            <div className="flex items-center space-x-2 mb-1">
                              <span className="font-semibold text-gray-900">
                                {deal.address || '(No Address)'}
                              </span>
                              <Badge className={getStrategyColor(deal.preferred_strategy)}>
                                {deal.preferred_strategy?.replace('_', ' ')}
                              </Badge>
                            </div>
                            <div className="text-sm text-gray-600">
                              ${deal.price.toLocaleString()} • Cap Rate: {deal.cap_rate.toFixed(2)}%
                            </div>
                          </div>
                          <div className="text-2xl font-bold text-blue-600">{deal.deal_score}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
