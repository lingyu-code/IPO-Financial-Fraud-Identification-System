<template>
  <div class="about">
    <div class="about-container">
      <div class="about-header">
        <h1>About IPO Financial Fraud Detection System</h1>
        <p class="subtitle">Advanced machine learning platform for identifying potential fraud in IPO companies</p>
      </div>

      <div class="about-content">
        <div class="info-section">
          <h2>System Overview</h2>
          <p>
            The IPO Financial Fraud Detection System is a comprehensive platform designed to identify and analyze
            potential financial fraud in companies going through Initial Public Offerings (IPOs). Our system utilizes
            advanced machine learning algorithms and financial analysis techniques to detect red flags and assess
            fraud risk.
          </p>
        </div>

        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3>Fraud Detection</h3>
            <p>Advanced algorithms analyze financial data to identify potential fraud patterns and anomalies.</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Risk Assessment</h3>
            <p>Comprehensive risk scoring system categorizes companies by their fraud risk levels.</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">🚩</div>
            <h3>Red Flag Analysis</h3>
            <p>Identifies specific red flags in financial statements and company operations.</p>
          </div>

          <div class="feature-card">
            <div class="feature-icon">📈</div>
            <h3>Analytics Dashboard</h3>
            <p>Interactive dashboards provide insights into fraud trends and risk distribution.</p>
          </div>
        </div>

        <div class="info-section">
          <h2>How It Works</h2>
          <div class="process-steps">
            <div class="step">
              <div class="step-number">1</div>
              <div class="step-content">
                <h4>Data Collection</h4>
                <p>Gather financial data, company information, and market data for IPO candidates.</p>
              </div>
            </div>

            <div class="step">
              <div class="step-number">2</div>
              <div class="step-content">
                <h4>Analysis & Scoring</h4>
                <p>Apply machine learning models to analyze data and generate fraud risk scores.</p>
              </div>
            </div>

            <div class="step">
              <div class="step-number">3</div>
              <div class="step-content">
                <h4>Red Flag Identification</h4>
                <p>Identify specific issues and anomalies that indicate potential fraud.</p>
              </div>
            </div>

            <div class="step">
              <div class="step-number">4</div>
              <div class="step-content">
                <h4>Reporting & Insights</h4>
                <p>Generate comprehensive reports and provide actionable insights for investors.</p>
              </div>
            </div>
          </div>
        </div>

        <div class="info-section">
          <h2>Technology Stack</h2>
          <div class="tech-stack">
            <div class="tech-category">
              <h4>Frontend</h4>
              <ul>
                <li>Vue.js 3 with TypeScript</li>
                <li>Vue Router for navigation</li>
                <li>Axios for API communication</li>
                <li>Responsive CSS design</li>
              </ul>
            </div>

            <div class="tech-category">
              <h4>Backend</h4>
              <ul>
                <li>Django REST Framework</li>
                <li>Python machine learning libraries</li>
                <li>SQLite database</li>
                <li>RESTful API architecture</li>
              </ul>
            </div>

            <div class="tech-category">
              <h4>Machine Learning</h4>
              <ul>
                <li>Anomaly detection algorithms</li>
                <li>Financial ratio analysis</li>
                <li>Pattern recognition models</li>
                <li>Risk scoring systems</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="info-section">
          <h2>Contact Information</h2>
          <div class="contact-info">
            <p><strong>Email:</strong> support@ipofrauddetection.com</p>
            <p><strong>Phone:</strong> +1 (555) 123-4567</p>
            <p><strong>Address:</strong> 123 Financial District, San Francisco, CA 94111</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about {
  background-color: #f8f9fa;
  min-height: calc(100vh - 140px);
  padding: 2rem 0;
}

.about-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.about-header {
  text-align: center;
  margin-bottom: 3rem;
}

.about-header h1 {
  color: #2c3e50;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.info-section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.info-section h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.info-section p {
  line-height: 1.6;
  color: #555;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.feature-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #666;
  font-size: 0.9rem;
}

.process-steps {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
}

.step-number {
  background: #3498db;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.step-content h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.step-content p {
  color: #666;
  margin: 0;
}

.tech-stack {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.tech-category h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.tech-category ul {
  list-style: none;
  padding: 0;
}

.tech-category li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #ecf0f1;
  color: #555;
}

.tech-category li:last-child {
  border-bottom: none;
}

.contact-info {
  color: #555;
}

.contact-info p {
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .about-container {
    padding: 0 1rem;
  }

  .about-header h1 {
    font-size: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .step {
    flex-direction: column;
    text-align: center;
  }

  .tech-stack {
    grid-template-columns: 1fr;
  }
}
</style>
