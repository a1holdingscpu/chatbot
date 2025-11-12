import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { API } from '../App';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Upload, FileSpreadsheet, CheckCircle, Link as LinkIcon, Table, FileText, PlusCircle, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

export default function UploadPageNew() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('excel');
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null);
  
  // Excel upload state
  const [file, setFile] = useState(null);
  const fileInputRef = useRef(null);
  
  // URL import state
  const [importUrl, setImportUrl] = useState('');
  const [fileType, setFileType] = useState('excel');
  
  // CSV state
  const [csvText, setCsvText] = useState('');
  
  // JSON state
  const [jsonText, setJsonText] = useState('');
  
  // Manual entry state
  const [manualDeal, setManualDeal] = useState({
    address: '',
    price: '',
    property_type: 'residential',
    arv: '',
    estimated_rehab: '',
    monthly_rent: '',
    sqft: '',
    beds: '',
    baths: '',
    units: '1',
    occupancy_pct: '100'
  });

  // Excel Upload Handlers
  const handleFileSelect = (e) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (!selectedFile.name.match(/\.(xlsx|xls|csv)$/)) {
        toast.error('Please select an Excel or CSV file');
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
      if (!droppedFile.name.match(/\.(xlsx|xls|csv)$/)) {
        toast.error('Please select an Excel or CSV file');
        return;
      }
      setFile(droppedFile);
      setResult(null);
    }
  };

  const handleExcelUpload = async () => {
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

  // URL Import Handler
  const handleUrlImport = async () => {
    if (!importUrl.trim()) {
      toast.error('Please enter a URL');
      return;
    }

    try {
      setUploading(true);
      const response = await axios.post(`${API}/upload-url`, {
        url: importUrl,
        file_type: fileType
      });

      setResult(response.data);
      toast.success(response.data.message);
    } catch (error) {
      console.error('URL import error:', error);
      toast.error(error.response?.data?.detail || 'Failed to import from URL');
    } finally {
      setUploading(false);
    }
  };

  // CSV Import Handler
  const handleCsvImport = async () => {
    if (!csvText.trim()) {
      toast.error('Please paste CSV data');
      return;
    }

    try {
      setUploading(true);
      const response = await axios.post(`${API}/upload-csv`, {
        csv_text: csvText
      });

      setResult(response.data);
      toast.success(response.data.message);
    } catch (error) {
      console.error('CSV import error:', error);
      toast.error(error.response?.data?.detail || 'Failed to import CSV');
    } finally {
      setUploading(false);
    }
  };

  // JSON Import Handler
  const handleJsonImport = async () => {
    if (!jsonText.trim()) {
      toast.error('Please paste JSON data');
      return;
    }

    try {
      setUploading(true);
      const jsonData = JSON.parse(jsonText);
      const response = await axios.post(`${API}/upload-json`, {
        json_data: jsonData
      });

      setResult(response.data);
      toast.success(response.data.message);
    } catch (error) {
      console.error('JSON import error:', error);
      if (error instanceof SyntaxError) {
        toast.error('Invalid JSON format');
      } else {
        toast.error(error.response?.data?.detail || 'Failed to import JSON');
      }
    } finally {
      setUploading(false);
    }
  };

  // Manual Deal Handler
  const handleManualSubmit = async () => {
    if (!manualDeal.address || !manualDeal.price) {
      toast.error('Address and Price are required');
      return;
    }

    try {
      setUploading(true);
      const response = await axios.post(`${API}/deals/manual`, manualDeal);

      toast.success('Deal created successfully!');
      setManualDeal({
        address: '',
        price: '',
        property_type: 'residential',
        arv: '',
        estimated_rehab: '',
        monthly_rent: '',
        sqft: '',
        beds: '',
        baths: '',
        units: '1',
        occupancy_pct: '100'
      });
      
      // Navigate to deals page
      setTimeout(() => navigate('/deals'), 1000);
    } catch (error) {
      console.error('Manual deal error:', error);
      toast.error(error.response?.data?.detail || 'Failed to create deal');
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
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-5xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Import Deals</h1>
          <p className="text-gray-600">Multiple ways to import your real estate deal data</p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-5 mb-8">
            <TabsTrigger value="excel" className="flex items-center space-x-2">
              <FileSpreadsheet className="w-4 h-4" />
              <span>Excel</span>
            </TabsTrigger>
            <TabsTrigger value="url" className="flex items-center space-x-2">
              <LinkIcon className="w-4 h-4" />
              <span>URL</span>
            </TabsTrigger>
            <TabsTrigger value="csv" className="flex items-center space-x-2">
              <Table className="w-4 h-4" />
              <span>CSV</span>
            </TabsTrigger>
            <TabsTrigger value="json" className="flex items-center space-x-2">
              <FileText className="w-4 h-4" />
              <span>JSON</span>
            </TabsTrigger>
            <TabsTrigger value="manual" className="flex items-center space-x-2">
              <PlusCircle className="w-4 h-4" />
              <span>Manual</span>
            </TabsTrigger>
          </TabsList>

          {/* Excel Upload Tab */}
          <TabsContent value="excel">
            <Card>
              <CardHeader>
                <CardTitle>Upload Excel File</CardTitle>
                <CardDescription>Upload .xlsx or .xls files containing your real estate deals</CardDescription>
              </CardHeader>
              <CardContent>
                <div
                  className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center hover:border-blue-500 transition-colors cursor-pointer"
                  onDrop={handleDrop}
                  onDragOver={(e) => e.preventDefault()}
                  onClick={() => fileInputRef.current?.click()}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".xlsx,.xls,.csv"
                    onChange={handleFileSelect}
                    className="hidden"
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
                        Supported formats: .xlsx, .xls, .csv
                      </p>
                    </div>
                  )}
                </div>

                {file && (
                  <div className="mt-6 flex justify-center">
                    <Button
                      size="lg"
                      onClick={handleExcelUpload}
                      disabled={uploading}
                      className="bg-blue-600 hover:bg-blue-700"
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
          </TabsContent>

          {/* URL Import Tab */}
          <TabsContent value="url">
            <Card>
              <CardHeader>
                <CardTitle>Import from URL</CardTitle>
                <CardDescription>Download and analyze deals from a URL (Excel, CSV, or JSON file)</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="url-input">File URL</Label>
                  <Input
                    id="url-input"
                    type="url"
                    placeholder="https://example.com/deals.xlsx"
                    value={importUrl}
                    onChange={(e) => setImportUrl(e.target.value)}
                    className="mt-2"
                  />
                  <div className="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-md">
                    <p className="text-xs text-blue-800 font-semibold mb-1">💡 URL Requirements:</p>
                    <ul className="text-xs text-blue-700 space-y-1 ml-4 list-disc">
                      <li>Must be a <strong>direct download link</strong> to the file</li>
                      <li>Google Drive: Use <code className="bg-white px-1 rounded">export?format=xlsx</code> link</li>
                      <li>Dropbox: Add <code className="bg-white px-1 rounded">?dl=1</code> at the end</li>
                      <li>Example: https://example.com/myfile.xlsx</li>
                    </ul>
                  </div>
                </div>

                <div>
                  <Label htmlFor="file-type">File Type</Label>
                  <select
                    id="file-type"
                    value={fileType}
                    onChange={(e) => setFileType(e.target.value)}
                    className="mt-2 w-full px-3 py-2 border border-gray-300 rounded-md"
                  >
                    <option value="excel">Excel (.xlsx, .xls)</option>
                    <option value="csv">CSV (.csv)</option>
                    <option value="json">JSON (.json)</option>
                  </select>
                </div>

                <Button
                  size="lg"
                  onClick={handleUrlImport}
                  disabled={uploading}
                  className="w-full bg-blue-600 hover:bg-blue-700"
                >
                  {uploading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Importing...
                    </>
                  ) : (
                    <>
                      <LinkIcon className="mr-2 h-5 w-5" />
                      Import from URL
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* CSV Import Tab */}
          <TabsContent value="csv">
            <Card>
              <CardHeader>
                <CardTitle>Import CSV Data</CardTitle>
                <CardDescription>Copy and paste CSV data from a spreadsheet</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="csv-textarea">CSV Data</Label>
                  <Textarea
                    id="csv-textarea"
                    placeholder="address,price,beds,baths,sqft&#10;123 Main St,250000,3,2,1500&#10;456 Oak Ave,350000,4,3,2000"
                    value={csvText}
                    onChange={(e) => setCsvText(e.target.value)}
                    className="mt-2 font-mono text-sm"
                    rows={10}
                  />
                  <p className="text-sm text-gray-500 mt-2">
                    First row should contain column headers (address, price, beds, etc.)
                  </p>
                </div>

                <Button
                  size="lg"
                  onClick={handleCsvImport}
                  disabled={uploading}
                  className="w-full bg-blue-600 hover:bg-blue-700"
                >
                  {uploading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Importing...
                    </>
                  ) : (
                    <>
                      <Table className="mr-2 h-5 w-5" />
                      Import CSV
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* JSON Import Tab */}
          <TabsContent value="json">
            <Card>
              <CardHeader>
                <CardTitle>Import JSON Data</CardTitle>
                <CardDescription>Paste JSON array or object with deal data</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="json-textarea">JSON Data</Label>
                  <Textarea
                    id="json-textarea"
                    placeholder='[{"address": "123 Main St", "price": 250000, "beds": 3, "baths": 2}]'
                    value={jsonText}
                    onChange={(e) => setJsonText(e.target.value)}
                    className="mt-2 font-mono text-sm"
                    rows={10}
                  />
                  <p className="text-sm text-gray-500 mt-2">
                    Accepts array of objects or object with 'deals', 'data', or 'properties' key
                  </p>
                </div>

                <Button
                  size="lg"
                  onClick={handleJsonImport}
                  disabled={uploading}
                  className="w-full bg-blue-600 hover:bg-blue-700"
                >
                  {uploading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Importing...
                    </>
                  ) : (
                    <>
                      <FileText className="mr-2 h-5 w-5" />
                      Import JSON
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Manual Entry Tab */}
          <TabsContent value="manual">
            <Card>
              <CardHeader>
                <CardTitle>Add Deal Manually</CardTitle>
                <CardDescription>Enter property details manually</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="col-span-2">
                    <Label htmlFor="address">Address *</Label>
                    <Input
                      id="address"
                      value={manualDeal.address}
                      onChange={(e) => setManualDeal({...manualDeal, address: e.target.value})}
                      placeholder="123 Main St, City, State"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label htmlFor="price">Price *</Label>
                    <Input
                      id="price"
                      type="number"
                      value={manualDeal.price}
                      onChange={(e) => setManualDeal({...manualDeal, price: e.target.value})}
                      placeholder="250000"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label htmlFor="property_type">Property Type</Label>
                    <select
                      id="property_type"
                      value={manualDeal.property_type}
                      onChange={(e) => setManualDeal({...manualDeal, property_type: e.target.value})}
                      className="mt-2 w-full px-3 py-2 border border-gray-300 rounded-md"
                    >
                      <option value="residential">Residential</option>
                      <option value="commercial">Commercial</option>
                      <option value="land">Land</option>
                      <option value="mobile_home_park">Mobile Home Park</option>
                      <option value="rv_park">RV Park</option>
                    </select>
                  </div>

                  <div>
                    <Label htmlFor="arv">ARV (After Repair Value)</Label>
                    <Input
                      id="arv"
                      type="number"
                      value={manualDeal.arv}
                      onChange={(e) => setManualDeal({...manualDeal, arv: e.target.value})}
                      placeholder="300000"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label htmlFor="estimated_rehab">Estimated Rehab</Label>
                    <Input
                      id="estimated_rehab"
                      type="number"
                      value={manualDeal.estimated_rehab}
                      onChange={(e) => setManualDeal({...manualDeal, estimated_rehab: e.target.value})}
                      placeholder="50000"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label htmlFor="monthly_rent">Monthly Rent</Label>
                    <Input
                      id="monthly_rent"
                      type="number"
                      value={manualDeal.monthly_rent}
                      onChange={(e) => setManualDeal({...manualDeal, monthly_rent: e.target.value})}
                      placeholder="2000"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label htmlFor="sqft">Square Feet</Label>
                    <Input
                      id="sqft"
                      type="number"
                      value={manualDeal.sqft}
                      onChange={(e) => setManualDeal({...manualDeal, sqft: e.target.value})}
                      placeholder="1500"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label htmlFor="beds">Bedrooms</Label>
                    <Input
                      id="beds"
                      type="number"
                      value={manualDeal.beds}
                      onChange={(e) => setManualDeal({...manualDeal, beds: e.target.value})}
                      placeholder="3"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label htmlFor="baths">Bathrooms</Label>
                    <Input
                      id="baths"
                      type="number"
                      step="0.5"
                      value={manualDeal.baths}
                      onChange={(e) => setManualDeal({...manualDeal, baths: e.target.value})}
                      placeholder="2"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label htmlFor="units">Units</Label>
                    <Input
                      id="units"
                      type="number"
                      value={manualDeal.units}
                      onChange={(e) => setManualDeal({...manualDeal, units: e.target.value})}
                      placeholder="1"
                      className="mt-2"
                    />
                  </div>

                  <div>
                    <Label htmlFor="occupancy_pct">Occupancy %</Label>
                    <Input
                      id="occupancy_pct"
                      type="number"
                      value={manualDeal.occupancy_pct}
                      onChange={(e) => setManualDeal({...manualDeal, occupancy_pct: e.target.value})}
                      placeholder="100"
                      className="mt-2"
                    />
                  </div>
                </div>

                <Button
                  size="lg"
                  onClick={handleManualSubmit}
                  disabled={uploading}
                  className="w-full bg-blue-600 hover:bg-blue-700"
                >
                  {uploading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Creating...
                    </>
                  ) : (
                    <>
                      <PlusCircle className="mr-2 h-5 w-5" />
                      Create Deal
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Results */}
        {result && result.success && (
          <Card className="border-green-200 bg-green-50 mt-8">
            <CardHeader>
              <div className="flex items-center space-x-3">
                <CheckCircle className="h-6 w-6 text-green-600" />
                <div>
                  <CardTitle className="text-green-900">Import Complete!</CardTitle>
                  <CardDescription className="text-green-700">
                    Successfully imported {result.deals_count} deals
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
                  >
                    View All Deals
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => navigate('/analytics')}
                  >
                    View Analytics
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setFile(null);
                      setImportUrl('');
                      setCsvText('');
                      setJsonText('');
                      setResult(null);
                    }}
                  >
                    Import More
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
