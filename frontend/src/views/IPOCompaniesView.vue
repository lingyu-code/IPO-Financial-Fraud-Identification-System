<template>
    <div class="ipo-companies">
        <div class="header">
            <h1>IPO Financial Fraud Detection System</h1>
            <div class="header-stats">
                <div class="stat-card">
                    <h3>{{ statistics.total_companies || 0 }}</h3>
                    <p>Total Companies</p>
                </div>
                <div class="stat-card high-risk">
                    <h3>{{ statistics.high_risk_count || 0 }}</h3>
                    <p>High Risk</p>
                </div>
                <div class="stat-card medium-risk">
                    <h3>{{ statistics.medium_risk_count || 0 }}</h3>
                    <p>Medium Risk</p>
                </div>
                <div class="stat-card low-risk">
                    <h3>{{ statistics.low_risk_count || 0 }}</h3>
                    <p>Low Risk</p>
                </div>
            </div>
        </div>

        <div class="controls">
            <div class="search-bar">
                <input v-model="searchQuery" type="text" placeholder="Search companies by name or ticker..."
                    @input="searchCompanies" />
            </div>
            <button class="btn-primary" @click="showAddCompanyModal = true">
                Add New Company
            </button>
        </div>

        <div class="companies-list">
            <div v-if="loading" class="loading">Loading companies...</div>

            <div v-else-if="companies.length === 0" class="empty-state">
                <p>No companies found. Add your first IPO company to get started.</p>
            </div>

            <div v-else class="company-cards">
                <div v-for="company in companies" :key="company.id" class="company-card"
                    :class="company.risk_category.toLowerCase() + '-risk'">
                    <div class="company-header">
                        <h3>{{ company.company_name }}</h3>
                        <span class="ticker">{{ company.ticker_symbol }}</span>
                    </div>

                    <div class="company-details">
                        <div class="detail">
                            <label>Industry:</label>
                            <span>{{ company.industry }}</span>
                        </div>
                        <div class="detail">
                            <label>Offering Date:</label>
                            <span>{{ formatDate(company.offering_date) }}</span>
                        </div>
                        <div class="detail">
                            <label>Offering Price:</label>
                            <span>${{ company.offering_price }}</span>
                        </div>
                        <div class="detail">
                            <label>Total Proceeds:</label>
                            <span>${{ formatNumber(company.total_proceeds) }}</span>
                        </div>
                    </div>

                    <div class="risk-section">
                        <div class="risk-score">
                            <div class="score-circle" :class="getRiskClass(company.fraud_risk_score)">
                                {{ company.fraud_risk_score }}
                            </div>
                            <div class="risk-info">
                                <span class="risk-category">{{ company.risk_category }} Risk</span>
                                <span class="score-label">Fraud Risk Score</span>
                            </div>
                        </div>

                        <div class="actions">
                            <button class="btn-analyze" @click="analyzeFraud(company.id)"
                                :disabled="analyzingCompany === company.id">
                                {{ analyzingCompany === company.id ? 'Analyzing...' : 'Analyze Fraud' }}
                            </button>
                            <button class="btn-details" @click="viewCompanyDetails(company)">
                                Details
                            </button>
                        </div>
                    </div>

                    <div v-if="company.red_flags && company.red_flags.length > 0" class="red-flags">
                        <h4>Red Flags ({{ company.red_flags.length }})</h4>
                        <div v-for="flag in company.red_flags.slice(0, 2)" :key="flag.id" class="red-flag"
                            :class="flag.severity.toLowerCase()">
                            <span class="flag-type">{{ flag.flag_type.replace('_', ' ') }}</span>
                            <span class="flag-severity">{{ flag.severity }}</span>
                        </div>
                        <div v-if="company.red_flags.length > 2" class="more-flags">
                            +{{ company.red_flags.length - 2 }} more flags
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add Company Modal -->
        <div v-if="showAddCompanyModal" class="modal-overlay" @click="showAddCompanyModal = false">
            <div class="modal" @click.stop>
                <h2>Add New IPO Company</h2>
                <form @submit.prevent="addCompany">
                    <div class="form-group">
                        <label>Company Name *</label>
                        <input v-model="newCompany.company_name" type="text" required />
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>Ticker Symbol</label>
                            <input v-model="newCompany.ticker_symbol" type="text" />
                        </div>
                        <div class="form-group">
                            <label>Industry *</label>
                            <input v-model="newCompany.industry" type="text" required />
                        </div>
                    </div>

                    <div class="form-group">
                        <label>Offering Date *</label>
                        <input v-model="newCompany.offering_date" type="date" required />
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>Offering Price ($) *</label>
                            <input v-model="newCompany.offering_price" type="number" step="0.01" required />
                        </div>
                        <div class="form-group">
                            <label>Shares Offered *</label>
                            <input v-model="newCompany.shares_offered" type="number" required />
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>Revenue ($)</label>
                            <input v-model="newCompany.revenue" type="number" step="0.01" />
                        </div>
                        <div class="form-group">
                            <label>Net Income ($)</label>
                            <input v-model="newCompany.net_income" type="number" step="0.01" />
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label>Total Assets ($)</label>
                            <input v-model="newCompany.total_assets" type="number" step="0.01" />
                        </div>
                        <div class="form-group">
                            <label>Total Liabilities ($)</label>
                            <input v-model="newCompany.total_liabilities" type="number" step="0.01" />
                        </div>
                    </div>

                    <div class="form-actions">
                        <button type="button" @click="showAddCompanyModal = false">Cancel</button>
                        <button type="submit" :disabled="addingCompany">
                            {{ addingCompany ? 'Adding...' : 'Add Company' }}
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Company Details Modal -->
        <div v-if="selectedCompany" class="modal-overlay" @click="selectedCompany = null">
            <div class="modal large" @click.stop>
                <h2>{{ selectedCompany.company_name }} Details</h2>
                <div class="company-details-full">
                    <!-- Company details would go here -->
                    <p>Detailed company view with complete fraud analysis would be implemented here.</p>
                </div>
                <div class="modal-actions">
                    <button @click="selectedCompany = null">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { companyAPI, fraudAPI } from '@/services/api'

interface Company {
    id: number
    company_name: string
    ticker_symbol: string
    industry: string
    offering_date: string
    offering_price: number
    shares_offered: number
    total_proceeds: number
    revenue: number | null
    net_income: number | null
    total_assets: number | null
    total_liabilities: number | null
    fraud_risk_score: number
    risk_category: string
    red_flags: any[]
}

interface Statistics {
    total_companies: number
    high_risk_count: number
    medium_risk_count: number
    low_risk_count: number
    high_risk_percentage: number
}

const companies = ref<Company[]>([])
const statistics = ref<Statistics>({} as Statistics)
const loading = ref(false)
const searchQuery = ref('')
const showAddCompanyModal = ref(false)
const selectedCompany = ref<Company | null>(null)
const analyzingCompany = ref<number | null>(null)
const addingCompany = ref(false)

const newCompany = ref({
    company_name: '',
    ticker_symbol: '',
    industry: '',
    offering_date: '',
    offering_price: 0,
    shares_offered: 0,
    revenue: null,
    net_income: null,
    total_assets: null,
    total_liabilities: null
})

// Load companies and statistics
const loadData = async () => {
    loading.value = true
    try {
        const [companiesResponse, statsResponse] = await Promise.all([
            companyAPI.getAllCompanies(),
            fraudAPI.getRiskStatistics()
        ])
        companies.value = companiesResponse.data
        statistics.value = statsResponse.data
    } catch (error) {
        console.error('Error loading data:', error)
        alert('Error loading data from server. Make sure the backend is running.')
    } finally {
        loading.value = false
    }
}

// Search companies
const searchCompanies = async () => {
    if (!searchQuery.value.trim()) {
        loadData()
        return
    }

    try {
        const response = await companyAPI.searchCompanies(searchQuery.value)
        companies.value = response.data
    } catch (error) {
        console.error('Error searching companies:', error)
    }
}

// Add new company
const addCompany = async () => {
    addingCompany.value = true
    try {
        await companyAPI.createCompany(newCompany.value)
        showAddCompanyModal.value = false
        // Reset form
        newCompany.value = {
            company_name: '',
            ticker_symbol: '',
            industry: '',
            offering_date: '',
            offering_price: 0,
            shares_offered: 0,
            revenue: null,
            net_income: null,
            total_assets: null,
            total_liabilities: null
        }
        // Reload data
        loadData()
    } catch (error) {
        console.error('Error adding company:', error)
        alert('Error adding company. Please check the data and try again.')
    } finally {
        addingCompany.value = false
    }
}

// Analyze fraud for a company
const analyzeFraud = async (companyId: number) => {
    analyzingCompany.value = companyId
    try {
        await companyAPI.analyzeFraud(companyId)
        // Reload data to get updated risk scores
        loadData()
    } catch (error) {
        console.error('Error analyzing fraud:', error)
        alert('Error analyzing fraud. Please try again.')
    } finally {
        analyzingCompany.value = null
    }
}

// View company details
const viewCompanyDetails = (company: Company) => {
    selectedCompany.value = company
}

// Utility functions
const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
}

const formatNumber = (num: number) => {
    return new Intl.NumberFormat().format(num)
}

const getRiskClass = (score: number) => {
    if (score >= 70) return 'high-risk'
    if (score >= 40) return 'medium-risk'
    return 'low-risk'
}

// Load data when component mounts
onMounted(() => {
    loadData()
})
</script>

<style scoped>
.ipo-companies {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.header {
    margin-bottom: 2rem;
}

.header h1 {
    color: #2c3e50;
    margin-bottom: 1rem;
}

.header-stats {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.stat-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
    min-width: 120px;
}

.stat-card h3 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: bold;
}

.stat-card p {
    margin: 0.5rem 0 0 0;
    color: #666;
    font-size: 0.9rem;
}

.high-risk h3 {
    color: #e74c3c;
}

.medium-risk h3 {
    color: #f39c12;
}

.low-risk h3 {
    color: #27ae60;
}

.controls {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
    align-items: center;
}

.search-bar {
    flex: 1;
}

.search-bar input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.btn-primary {
    background: #3498db;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
}

.btn-primary:hover {
    background: #2980b9;
}

.company-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1.5rem;
}

.company-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #ddd;
}

.company-card.high-risk {
    border-left-color: #e74c3c;
}

.company-card.medium-risk {
    border-left-color: #f39c12;
}

.company-card.low-risk {
    border-left-color: #27ae60;
}

.company-header {
    display: flex;
    justify-content: between;
    align-items: center;
    margin-bottom: 1rem;
}

.company-header h3 {
    margin: 0;
    flex: 1;
}

.ticker {
    background: #ecf0f1;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: bold;
}

.company-details {
    margin-bottom: 1rem;
}

.detail {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
}

.detail label {
    font-weight: 600;
    color: #666;
}

.risk-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.risk-score {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.score-circle {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 1.2rem;
    color: white;
}

.score-circle.high-risk {
    background: #e74c3c;
}

.score-circle.medium-risk {
    background: #f39c12;
}

.score-circle.low-risk {
    background: #27ae60;
}

.risk-info {
    display: flex;
    flex-direction: column;
}

.risk-category {
    font-weight: bold;
    font-size: 1.1rem;
}

.score-label {
    font-size: 0.8rem;
    color: #666;
}

.actions {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.btn-analyze,
.btn-details {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
}

.btn-analyze {
    background: #3498db;
    color: white;
}

.btn-analyze:hover:not(:disabled) {
    background: #2980b9;
}

.btn-analyze:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
}

.btn-details {
    background: #ecf0f1;
    color: #2c3e50;
}

.btn-details:hover {
    background: #bdc3c7;
}

.red-flags {
    border-top: 1px solid #ecf0f1;
    padding-top: 1rem;
}

.red-flags h4 {
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
    color: #666;
}

.red-flag {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem;
    margin-bottom: 0.25rem;
    border-radius: 4px;
    font-size: 0.8rem;
}

.red-flag.critical {
    background: #ffebee;
}

.red-flag.high {
    background: #fff3e0;
}

.red-flag.medium {
    background: #fff8e1;
}

.red-flag.low {
    background: #f1f8e9;
}

.flag-type {
    font-weight: 600;
}

.flag-severity {
    padding: 0.1rem 0.4rem;
    border-radius: 3px;
    font-size: 0.7rem;
    font-weight: bold;
    text-transform: uppercase;
}

.red-flag.critical .flag-severity {
    background: #f44336;
    color: white;
}

.red-flag.high .flag-severity {
    background: #ff9800;
    color: white;
}

.red-flag.medium .flag-severity {
    background: #ffc107;
    color: black;
}

.red-flag.low .flag-severity {
    background: #8bc34a;
    color: white;
}

.more-flags {
    text-align: center;
    color: #666;
    font-size: 0.8rem;
    margin-top: 0.5rem;
}

.loading,
.empty-state {
    text-align: center;
    padding: 3rem;
    color: #666;
}

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    max-width: 500px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
}

.modal.large {
    max-width: 800px;
}

.form-group {
    margin-bottom: 1rem;
}

.form-row {
    display: flex;
    gap: 1rem;
}

.form-row .form-group {
    flex: 1;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.form-group input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.form-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
    margin-top: 1.5rem;
}

.form-actions button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.form-actions button[type="button"] {
    background: #ecf0f1;
    color: #2c3e50;
}

.form-actions button[type="submit"] {
    background: #3498db;
    color: white;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 1rem;
}
</style>
