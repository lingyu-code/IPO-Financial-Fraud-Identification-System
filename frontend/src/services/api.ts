import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with base configuration
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// API service for IPO companies
export const companyAPI = {
    // Get all companies
    getAllCompanies: () => apiClient.get('/companies/'),

    // Get company by ID
    getCompany: (id: number) => apiClient.get(`/companies/${id}/`),

    // Create new company
    createCompany: (data: any) => apiClient.post('/companies/', data),

    // Update company
    updateCompany: (id: number, data: any) => apiClient.put(`/companies/${id}/`, data),

    // Delete company
    deleteCompany: (id: number) => apiClient.delete(`/companies/${id}/`),

    // Search companies
    searchCompanies: (query: string) => apiClient.get(`/companies/search/?q=${query}`),

    // Get high risk companies
    getHighRiskCompanies: () => apiClient.get('/companies/high_risk_companies/'),

    // Analyze fraud for company
    analyzeFraud: (id: number) => apiClient.post(`/companies/${id}/analyze_fraud/`),
};

// API service for fraud detection
export const fraudAPI = {
    // Detect fraud for company
    detectFraud: (companyId: number) => apiClient.post('/fraud-detection/detect_fraud/', { company_id: companyId }),

    // Get risk statistics
    getRiskStatistics: () => apiClient.get('/fraud-detection/risk_statistics/'),
};

// API service for red flags
export const redFlagAPI = {
    // Get all red flags
    getAllRedFlags: () => apiClient.get('/red-flags/'),

    // Get red flags by company
    getRedFlagsByCompany: (companyId: number) => apiClient.get(`/red-flags/?company_id=${companyId}`),
};

// API service for fraud analysis
export const fraudAnalysisAPI = {
    // Get all fraud analyses
    getAllAnalyses: () => apiClient.get('/fraud-analysis/'),

    // Get analysis by company
    getAnalysisByCompany: (companyId: number) => apiClient.get(`/fraud-analysis/?company_id=${companyId}`),
};

// Export the axios instance for direct use if needed
export default apiClient;
