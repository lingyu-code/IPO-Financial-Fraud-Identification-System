import axios from "axios";
import { ElMessage } from "element-plus";
const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with base configuration
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Response interceptor - 统一错误处理
apiClient.interceptors.response.use(
    response => {
        let data = response.data;
        // 如果返回的是字符串，尝试解析为JSON
        if (typeof data === "string") {
            data = data ? JSON.parse(data) : data;
        }
        return {
            data: data,
            status: response.status,
            statusText: response.statusText,
            headers: response.headers,
            config: response.config,
        };
    },
    error => {
        if (error.response) {
            const status = error.response.status;
            const responseData = error.response.data;

            if (status === 400) {
                ElMessage.error("请求参数错误，请检查输入");
            } else if (status === 401) {
                ElMessage.error("未授权，请重新登录");
            } else if (status === 403) {
                ElMessage.error("权限不足，无法访问");
            } else if (status === 404) {
                ElMessage.error("请求的资源不存在");
            } else if (status === 405) {
                ElMessage.error("请求方式错误");
            } else if (status === 500) {
                ElMessage.error("服务器内部错误，请查看日志");
            } else {
                ElMessage.error(`请求错误: ${responseData?.message || error.message}`);
            }

            return Promise.reject(responseData);
        } else {
            if (error.code === 'ECONNABORTED') {
                ElMessage.error("请求超时，请重试");
            } else {
                ElMessage.error("网络错误，请检查网络连接");
            }
            return Promise.reject(error);
        }
    }
);


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
export const authAPI = {
    login: (form: { username: string; password: string }) =>
        apiClient.post('/login/', form),
};
// Export the axios instance for direct use if needed
export default apiClient;
