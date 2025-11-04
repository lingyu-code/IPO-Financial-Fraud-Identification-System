<template>
    <div class="analytics">
        <div class="analytics-container">
            <div class="analytics-header">
                <h1>Fraud Analytics</h1>
                <p class="subtitle">Comprehensive analysis and insights into IPO fraud patterns</p>
            </div>

            <!-- Analytics Overview Cards -->
            <div class="analytics-overview">
                <div class="overview-card">
                    <div class="overview-icon">📊</div>
                    <div class="overview-content">
                        <h3>Risk Analysis</h3>
                        <p>Detailed breakdown of fraud risk across all companies</p>
                    </div>
                </div>

                <div class="overview-card">
                    <div class="overview-icon">🚩</div>
                    <div class="overview-content">
                        <h3>Red Flag Trends</h3>
                        <p>Identify common patterns and emerging fraud indicators</p>
                    </div>
                </div>

                <div class="overview-card">
                    <div class="overview-icon">📈</div>
                    <div class="overview-content">
                        <h3>Performance Metrics</h3>
                        <p>Track detection accuracy and system performance</p>
                    </div>
                </div>
            </div>

            <!-- Main Analytics Grid -->
            <div class="analytics-grid">
                <!-- Risk Score Distribution -->
                <div class="analytics-card">
                    <div class="card-header">
                        <h3>Risk Score Distribution</h3>
                        <div class="time-filter">
                            <select v-model="timeRange">
                                <option value="7d">Last 7 Days</option>
                                <option value="30d">Last 30 Days</option>
                                <option value="90d">Last 90 Days</option>
                                <option value="all">All Time</option>
                            </select>
                        </div>
                    </div>
                    <div class="chart-container">
                        <div class="bar-chart">
                            <div class="bar-chart-item">
                                <div class="bar-label">Low Risk (0-39)</div>
                                <div class="bar-container">
                                    <div class="bar low" :style="{ width: riskDistribution.low + '%' }"></div>
                                    <span class="bar-value">{{ riskDistribution.low }}%</span>
                                </div>
                            </div>
                            <div class="bar-chart-item">
                                <div class="bar-label">Medium Risk (40-69)</div>
                                <div class="bar-container">
                                    <div class="bar medium" :style="{ width: riskDistribution.medium + '%' }"></div>
                                    <span class="bar-value">{{ riskDistribution.medium }}%</span>
                                </div>
                            </div>
                            <div class="bar-chart-item">
                                <div class="bar-label">High Risk (70-100)</div>
                                <div class="bar-container">
                                    <div class="bar high" :style="{ width: riskDistribution.high + '%' }"></div>
                                    <span class="bar-value">{{ riskDistribution.high }}%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Top Red Flags -->
                <div class="analytics-card">
                    <div class="card-header">
                        <h3>Top Red Flags</h3>
                    </div>
                    <div class="red-flags-list">
                        <div v-for="(flag, index) in topRedFlags" :key="index" class="red-flag-item">
                            <div class="flag-rank">{{ index + 1 }}</div>
                            <div class="flag-details">
                                <h4>{{ flag.type }}</h4>
                                <p>{{ flag.description }}</p>
                            </div>
                            <div class="flag-count">
                                <span class="count">{{ flag.count }}</span>
                                <span class="label">occurrences</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Industry Analysis -->
                <div class="analytics-card">
                    <div class="card-header">
                        <h3>Industry Risk Analysis</h3>
                    </div>
                    <div class="industry-list">
                        <div v-for="industry in industryAnalysisWithPercentage" :key="industry.name"
                            class="industry-item">
                            <div class="industry-name">
                                <span>{{ industry.name }}</span>
                                <span class="company-count">{{ industry.companyCount }} companies</span>
                            </div>
                            <div class="industry-risk">
                                <div class="risk-bar">
                                    <div class="risk-fill" :class="industry.riskLevel"
                                        :style="{ width: industry.riskPercentage + '%' }"></div>
                                </div>
                                <span class="risk-score">{{ industry.averageRisk }}%</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Detection Performance -->
                <div class="analytics-card">
                    <div class="card-header">
                        <h3>Detection Performance</h3>
                    </div>
                    <div class="performance-stats">
                        <div class="performance-item">
                            <div class="performance-label">Accuracy Rate</div>
                            <div class="performance-value">{{ performance.accuracy }}%</div>
                            <div class="performance-bar">
                                <div class="performance-fill" :style="{ width: performance.accuracy + '%' }"></div>
                            </div>
                        </div>
                        <div class="performance-item">
                            <div class="performance-label">False Positive Rate</div>
                            <div class="performance-value">{{ performance.falsePositive }}%</div>
                            <div class="performance-bar">
                                <div class="performance-fill false-positive"
                                    :style="{ width: performance.falsePositive + '%' }"></div>
                            </div>
                        </div>
                        <div class="performance-item">
                            <div class="performance-label">Detection Speed</div>
                            <div class="performance-value">{{ performance.speed }}ms</div>
                            <div class="performance-bar">
                                <div class="performance-fill speed"
                                    :style="{ width: Math.min(performance.speed / 10, 100) + '%' }"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Recent Analysis Activity -->
                <div class="analytics-card">
                    <div class="card-header">
                        <h3>Recent Analysis Activity</h3>
                    </div>
                    <div class="activity-list">
                        <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                            <div class="activity-icon" :class="activity.type">
                                {{ getActivityIcon(activity.type) }}
                            </div>
                            <div class="activity-details">
                                <h4>{{ activity.title }}</h4>
                                <p>{{ activity.description }}</p>
                                <span class="activity-time">{{ activity.time }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Export Options -->
                <div class="analytics-card">
                    <div class="card-header">
                        <h3>Export Reports</h3>
                    </div>
                    <div class="export-options">
                        <button class="export-btn" @click="exportReport('pdf')">
                            <span class="export-icon">📄</span>
                            <span>Export as PDF</span>
                        </button>
                        <button class="export-btn" @click="exportReport('csv')">
                            <span class="export-icon">📊</span>
                            <span>Export as CSV</span>
                        </button>
                        <button class="export-btn" @click="exportReport('excel')">
                            <span class="export-icon">📈</span>
                            <span>Export as Excel</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'

const timeRange = ref('30d')

// Mock data for analytics
const riskDistribution = ref({
    low: 45,
    medium: 35,
    high: 20
})

const topRedFlags = ref([
    {
        type: 'Revenue Recognition',
        description: 'Aggressive revenue recognition practices',
        count: 12
    },
    {
        type: 'Related Party Transactions',
        description: 'Undisclosed related party transactions',
        count: 9
    },
    {
        type: 'Inventory Valuation',
        description: 'Questionable inventory valuation methods',
        count: 7
    },
    {
        type: 'Expense Capitalization',
        description: 'Inappropriate expense capitalization',
        count: 6
    },
    {
        type: 'Revenue Growth Anomalies',
        description: 'Unusually high revenue growth rates',
        count: 5
    }
])

const industryAnalysis = ref([
    {
        name: 'Technology',
        companyCount: 15,
        averageRisk: 65,
        riskLevel: 'high'
    },
    {
        name: 'Healthcare',
        companyCount: 12,
        averageRisk: 52,
        riskLevel: 'medium'
    },
    {
        name: 'Finance',
        companyCount: 8,
        averageRisk: 48,
        riskLevel: 'medium'
    },
    {
        name: 'Manufacturing',
        companyCount: 10,
        averageRisk: 38,
        riskLevel: 'low'
    },
    {
        name: 'Retail',
        companyCount: 7,
        averageRisk: 42,
        riskLevel: 'medium'
    }
])

const performance = ref({
    accuracy: 92,
    falsePositive: 8,
    speed: 250
})

const recentActivity = ref([
    {
        id: 1,
        type: 'analysis',
        title: 'Fraud Analysis Completed',
        description: 'Analysis for TechCorp IPO completed',
        time: '2 hours ago'
    },
    {
        id: 2,
        type: 'alert',
        title: 'High Risk Detected',
        description: 'New high risk company identified',
        time: '5 hours ago'
    },
    {
        id: 3,
        type: 'update',
        title: 'Model Updated',
        description: 'Machine learning model retrained',
        time: '1 day ago'
    },
    {
        id: 4,
        type: 'report',
        title: 'Monthly Report Generated',
        description: 'Monthly fraud analysis report created',
        time: '2 days ago'
    }
])

// Computed properties
const industryAnalysisWithPercentage = computed(() => {
    return industryAnalysis.value.map(industry => ({
        ...industry,
        riskPercentage: Math.min(industry.averageRisk * 1.5, 100)
    }))
})

// Methods
const getActivityIcon = (type: string) => {
    const icons: { [key: string]: string } = {
        analysis: '🔍',
        alert: '⚠️',
        update: '🔄',
        report: '📊'
    }
    return icons[type] || '📝'
}

const exportReport = (format: string) => {
    // In a real application, this would trigger a download
    alert(`Exporting analytics report as ${format.toUpperCase()}...`)
    console.log(`Exporting report as ${format}`)
}

// Load analytics data
const loadAnalyticsData = async () => {
    // In a real application, this would fetch data from the API
    console.log('Loading analytics data for time range:', timeRange.value)
}

// Watch for time range changes
// onMounted(() => {
//     loadAnalyticsData()
// })
</script>

<style scoped>
.analytics {
    background-color: #f8f9fa;
    min-height: calc(100vh - 140px);
    padding: 2rem 0;
}

.analytics-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.analytics-header {
    margin-bottom: 2rem;
}

.analytics-header h1 {
    color: #2c3e50;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.subtitle {
    color: #666;
    font-size: 1.1rem;
}

/* Analytics Overview */
.analytics-overview {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.overview-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: transform 0.3s ease;
}

.overview-card:hover {
    transform: translateY(-2px);
}

.overview-icon {
    font-size: 2rem;
}

.overview-content h3 {
    margin: 0 0 0.5rem 0;
    color: #2c3e50;
}

.overview-content p {
    margin: 0;
    color: #666;
    font-size: 0.9rem;
}

/* Analytics Grid */
.analytics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 1.5rem;
}

.analytics-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.card-header h3 {
    margin: 0;
    color: #2c3e50;
}

.time-filter select {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
}

/* Bar Chart */
.bar-chart {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.bar-chart-item {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.bar-label {
    width: 120px;
    font-size: 0.9rem;
    color: #666;
}

.bar-container {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.bar {
    height: 20px;
    border-radius: 10px;
    transition: width 0.5s ease;
}

.bar.low {
    background: #27ae60;
}

.bar.medium {
    background: #f39c12;
}

.bar.high {
    background: #e74c3c;
}

.bar-value {
    width: 40px;
    text-align: right;
    font-weight: bold;
    font-size: 0.9rem;
}

/* Red Flags List */
.red-flags-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.red-flag-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid #ecf0f1;
    border-radius: 8px;
}

.flag-rank {
    background: #3498db;
    color: white;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    flex-shrink: 0;
}

.flag-details {
    flex: 1;
}

.flag-details h4 {
    margin: 0 0 0.25rem 0;
    color: #2c3e50;
}

.flag-details p {
    margin: 0;
    color: #666;
    font-size: 0.8rem;
}

.flag-count {
    text-align: center;
}

.flag-count .count {
    display: block;
    font-size: 1.2rem;
    font-weight: bold;
    color: #e74c3c;
}

.flag-count .label {
    font-size: 0.7rem;
    color: #666;
    text-transform: uppercase;
}

/* Industry Analysis */
.industry-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.industry-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid #ecf0f1;
}

.industry-item:last-child {
    border-bottom: none;
}

.industry-name {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.industry-name span:first-child {
    font-weight: 600;
    color: #2c3e50;
}

.company-count {
    font-size: 0.8rem;
    color: #666;
}

.industry-risk {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.risk-bar {
    width: 100px;
    height: 8px;
    background: #ecf0f1;
    border-radius: 4px;
    overflow: hidden;
}

.risk-fill {
    height: 100%;
    transition: width 0.5s ease;
}

.risk-fill.low {
    background: #27ae60;
}

.risk-fill.medium {
    background: #f39c12;
}

.risk-fill.high {
    background: #e74c3c;
}

.risk-score {
    width: 40px;
    text-align: right;
    font-weight: bold;
    font-size: 0.9rem;
}

/* Performance Stats */
.performance-stats {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.performance-item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.performance-label {
    font-size: 0.9rem;
    color: #666;
}

.performance-value {
    font-size: 1.2rem;
    font-weight: bold;
    color: #2c3e50;
}

.performance-bar {
    height: 6px;
    background: #ecf0f1;
    border-radius: 3px;
    overflow: hidden;
}

.performance-fill {
    height: 100%;
    background: #27ae60;
    transition: width 0.5s ease;
}

.performance-fill.false-positive {
    background: #e74c3c;
}

.performance-fill.speed {
    background: #3498db;
}

/* Activity List */
.activity-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.activity-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
    border: 1px solid #ecf0f1;
    border-radius: 8px;
}

.activity-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    flex-shrink: 0;
}

.activity-icon.analysis {
    background: #e3f2fd;
}

.activity-icon.alert {
    background: #ffebee;
}

.activity-icon.update {
    background: #fff3e0;
}

.activity-icon.report {
    background: #e8f5e8;
}

.activity-details {
    flex: 1;
}

.activity-details h4 {
    margin: 0 0 0.25rem 0;
    color: #2c3e50;
}

.activity-details p {
    margin: 0 0 0.5rem 0;
    color: #666;
    font-size: 0.9rem;
}

.activity-time {
    font-size: 0.8rem;
    color: #999;
}

/* Export Options */
.export-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 1rem;
}

.export-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem;
    border: 1px solid #3498db;
    border-radius: 8px;
    background: white;
    color: #3498db;
    cursor: pointer;
    transition: all 0.3s ease;
}

.export-btn:hover {
    background: #3498db;
    color: white;
}

.export-icon {
    font-size: 1.5rem;
}

@media (max-width: 768px) {
    .analytics-container {
        padding: 0 1rem;
    }

    .analytics-grid {
        grid-template-columns: 1fr;
    }

    .analytics-overview {
        grid-template-columns: 1fr;
    }

    .bar-chart-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .bar-container {
        width: 100%;
    }

    .industry-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .industry-risk {
        width: 100%;
        justify-content: space-between;
    }

    .export-options {
        grid-template-columns: 1fr;
    }
}
</style>
