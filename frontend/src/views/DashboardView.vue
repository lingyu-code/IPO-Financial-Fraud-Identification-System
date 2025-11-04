<template>
    <div class="dashboard">
        <div class="dashboard-container">
            <div class="dashboard-header">
                <h1>Fraud Detection Dashboard</h1>
                <p class="subtitle">Overview of IPO companies and fraud risk analysis</p>
            </div>

            <!-- Statistics Cards -->
            <div class="stats-grid">
                <div class="stat-card total">
                    <div class="stat-icon">🏢</div>
                    <div class="stat-content">
                        <h3>{{ statistics.total_companies || 0 }}</h3>
                        <p>Total Companies</p>
                    </div>
                </div>

                <div class="stat-card high-risk">
                    <div class="stat-icon">🔴</div>
                    <div class="stat-content">
                        <h3>{{ statistics.high_risk_count || 0 }}</h3>
                        <p>High Risk</p>
                        <span class="percentage">{{ statistics.high_risk_percentage || 0 }}%</span>
                    </div>
                </div>

                <div class="stat-card medium-risk">
                    <div class="stat-icon">🟡</div>
                    <div class="stat-content">
                        <h3>{{ statistics.medium_risk_count || 0 }}</h3>
                        <p>Medium Risk</p>
                    </div>
                </div>

                <div class="stat-card low-risk">
                    <div class="stat-icon">🟢</div>
                    <div class="stat-content">
                        <h3>{{ statistics.low_risk_count || 0 }}</h3>
                        <p>Low Risk</p>
                    </div>
                </div>
            </div>

            <!-- Main Content Grid -->
            <div class="content-grid">
                <!-- Risk Distribution Chart -->
                <div class="chart-card">
                    <div class="card-header">
                        <h3>Risk Distribution</h3>
                    </div>
                    <div class="chart-placeholder">
                        <div class="chart-visual">
                            <div class="pie-chart" :style="{
                                background: `conic-gradient(
                                    #e74c3c 0% ${chartPercentages.high}%,
                                    #f39c12 ${chartPercentages.high}% ${chartPercentages.high + chartPercentages.medium}%,
                                    #27ae60 ${chartPercentages.high + chartPercentages.medium}% 100%
                                )`
                            }"></div>
                        </div>
                        <div class="chart-legend">
                            <div class="legend-item">
                                <span class="legend-color high"></span>
                                <span>High Risk: {{ statistics.high_risk_count || 0 }}</span>
                            </div>
                            <div class="legend-item">
                                <span class="legend-color medium"></span>
                                <span>Medium Risk: {{ statistics.medium_risk_count || 0 }}</span>
                            </div>
                            <div class="legend-item">
                                <span class="legend-color low"></span>
                                <span>Low Risk: {{ statistics.low_risk_count || 0 }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Recent High Risk Companies -->
                <div class="high-risk-card">
                    <div class="card-header">
                        <h3>Recent High Risk Companies</h3>
                        <RouterLink to="/companies" class="view-all">View All</RouterLink>
                    </div>
                    <div class="high-risk-list">
                        <div v-if="highRiskCompanies.length === 0" class="empty-state">
                            <p>No high risk companies found</p>
                        </div>
                        <div v-else>
                            <div v-for="company in highRiskCompanies.slice(0, 5)" :key="company.id"
                                class="high-risk-item">
                                <div class="company-info">
                                    <h4>{{ company.company_name }}</h4>
                                    <span class="ticker">{{ company.ticker_symbol }}</span>
                                </div>
                                <div class="risk-score">
                                    <div class="score-badge high">{{ company.fraud_risk_score }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="actions-card">
                    <div class="card-header">
                        <h3>Quick Actions</h3>
                    </div>
                    <div class="actions-list">
                        <RouterLink to="/companies" class="action-item">
                            <div class="action-icon">📋</div>
                            <div class="action-content">
                                <h4>Manage Companies</h4>
                                <p>View and manage all IPO companies</p>
                            </div>
                        </RouterLink>

                        <RouterLink to="/analytics" class="action-item">
                            <div class="action-icon">📊</div>
                            <div class="action-content">
                                <h4>View Analytics</h4>
                                <p>Detailed fraud analysis and reports</p>
                            </div>
                        </RouterLink>

                        <button class="action-item" @click="analyzeAllCompanies" :disabled="analyzingAll">
                            <div class="action-icon">🔍</div>
                            <div class="action-content">
                                <h4>Run Analysis</h4>
                                <p>Analyze all companies for fraud</p>
                            </div>
                            <div v-if="analyzingAll" class="loading-spinner"></div>
                        </button>
                    </div>
                </div>

                <!-- System Status -->
                <div class="status-card">
                    <div class="card-header">
                        <h3>System Status</h3>
                    </div>
                    <div class="status-list">
                        <div class="status-item">
                            <span class="status-indicator online"></span>
                            <span>Backend API</span>
                            <span class="status-text">Online</span>
                        </div>
                        <div class="status-item">
                            <span class="status-indicator online"></span>
                            <span>Database</span>
                            <span class="status-text">Connected</span>
                        </div>
                        <div class="status-item">
                            <span class="status-indicator online"></span>
                            <span>ML Models</span>
                            <span class="status-text">Ready</span>
                        </div>
                        <div class="status-item">
                            <span class="status-indicator online"></span>
                            <span>Last Analysis</span>
                            <span class="status-text">{{ lastAnalysisTime }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { companyAPI, fraudAPI } from '@/services/api'

interface Company {
    id: number
    company_name: string
    ticker_symbol: string
    fraud_risk_score: number
    risk_category: string
}

interface Statistics {
    total_companies: number
    high_risk_count: number
    medium_risk_count: number
    low_risk_count: number
    high_risk_percentage: number
}

const statistics = ref<Statistics>({} as Statistics)
const highRiskCompanies = ref<Company[]>([])
const analyzingAll = ref(false)
const lastAnalysisTime = ref('Never')

// Computed properties for pie chart
const chartPercentages = computed(() => {
    const total = statistics.value.total_companies || 1
    return {
        high: ((statistics.value.high_risk_count || 0) / total) * 100,
        medium: ((statistics.value.medium_risk_count || 0) / total) * 100,
        low: ((statistics.value.low_risk_count || 0) / total) * 100
    }
})

// Load dashboard data
const loadDashboardData = async () => {
    try {
        const [statsResponse, highRiskResponse] = await Promise.all([
            fraudAPI.getRiskStatistics(),
            companyAPI.getHighRiskCompanies()
        ])

        statistics.value = statsResponse.data
        highRiskCompanies.value = highRiskResponse.data

        // Update last analysis time
        lastAnalysisTime.value = new Date().toLocaleString()
    } catch (error) {
        console.error('Error loading dashboard data:', error)
    }
}

// Analyze all companies
const analyzeAllCompanies = async () => {
    analyzingAll.value = true
    try {
        // This would typically be a batch analysis endpoint
        // For now, we'll simulate the process
        await new Promise(resolve => setTimeout(resolve, 2000))
        await loadDashboardData()
    } catch (error) {
        console.error('Error analyzing all companies:', error)
    } finally {
        analyzingAll.value = false
    }
}

// Load data when component mounts
onMounted(() => {
    loadDashboardData()
})
</script>

<style scoped>
.dashboard {
    background-color: #f8f9fa;
    min-height: calc(100vh - 140px);
    padding: 2rem 0;
}

.dashboard-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.dashboard-header {
    margin-bottom: 2rem;
}

.dashboard-header h1 {
    color: #2c3e50;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.subtitle {
    color: #666;
    font-size: 1.1rem;
}

/* Statistics Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 1rem;
}

.stat-icon {
    font-size: 2rem;
}

.stat-content h3 {
    margin: 0;
    font-size: 2rem;
    font-weight: bold;
}

.stat-content p {
    margin: 0.25rem 0 0 0;
    color: #666;
    font-size: 0.9rem;
}

.percentage {
    font-size: 0.8rem;
    font-weight: bold;
    color: #e74c3c;
}

/* Risk-specific colors */
.high-risk .stat-content h3 {
    color: #e74c3c;
}

.medium-risk .stat-content h3 {
    color: #f39c12;
}

.low-risk .stat-content h3 {
    color: #27ae60;
}

/* Content Grid */
.content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
}

.chart-card,
.high-risk-card,
.actions-card,
.status-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.card-header h3 {
    margin: 0;
    color: #2c3e50;
}

.view-all {
    color: #3498db;
    text-decoration: none;
    font-size: 0.9rem;
}

/* Chart Styles */
.chart-placeholder {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.chart-visual {
    flex: 1;
    display: flex;
    justify-content: center;
}

.pie-chart {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: conic-gradient(#e74c3c 0% var(--high-percentage, 0%),
            #f39c12 var(--high-percentage, 0%) calc(var(--high-percentage, 0%) + var(--medium-percentage, 0%)),
            #27ae60 calc(var(--high-percentage, 0%) + var(--medium-percentage, 0%)) 100%);
}

.chart-legend {
    flex: 1;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.legend-color {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.legend-color.high {
    background: #e74c3c;
}

.legend-color.medium {
    background: #f39c12;
}

.legend-color.low {
    background: #27ae60;
}

/* High Risk List */
.high-risk-list {
    max-height: 300px;
    overflow-y: auto;
}

.high-risk-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid #ecf0f1;
}

.high-risk-item:last-child {
    border-bottom: none;
}

.company-info h4 {
    margin: 0 0 0.25rem 0;
    color: #2c3e50;
}

.ticker {
    background: #ecf0f1;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
    color: #666;
}

.score-badge {
    background: #e74c3c;
    color: white;
    padding: 0.5rem 0.75rem;
    border-radius: 20px;
    font-weight: bold;
    font-size: 0.9rem;
}

/* Actions List */
.actions-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.action-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid #ecf0f1;
    border-radius: 8px;
    text-decoration: none;
    color: inherit;
    transition: all 0.3s ease;
    background: none;
    cursor: pointer;
}

.action-item:hover {
    background: #f8f9fa;
    border-color: #3498db;
}

.action-icon {
    font-size: 1.5rem;
}

.action-content h4 {
    margin: 0 0 0.25rem 0;
    color: #2c3e50;
}

.action-content p {
    margin: 0;
    color: #666;
    font-size: 0.9rem;
}

.loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

/* Status List */
.status-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.status-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid #ecf0f1;
}

.status-item:last-child {
    border-bottom: none;
}

.status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.status-indicator.online {
    background: #27ae60;
}

.status-text {
    margin-left: auto;
    color: #666;
    font-size: 0.9rem;
}

.empty-state {
    text-align: center;
    padding: 2rem;
    color: #666;
}

@media (max-width: 768px) {
    .dashboard-container {
        padding: 0 1rem;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }

    .content-grid {
        grid-template-columns: 1fr;
    }

    .chart-placeholder {
        flex-direction: column;
        text-align: center;
    }
}
</style>
