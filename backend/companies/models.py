from django.db import models


class Company(models.Model):
    RISK_CATEGORIES = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
    ]
    
    company_name = models.CharField(max_length=255)
    ticker_symbol = models.CharField(max_length=10, blank=True, null=True)
    industry = models.CharField(max_length=100)
    offering_date = models.DateField()
    offering_price = models.DecimalField(max_digits=10, decimal_places=2)
    shares_offered = models.IntegerField()
    total_proceeds = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    revenue = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    net_income = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fraud_risk_score = models.IntegerField(default=0)
    risk_category = models.CharField(max_length=10, choices=RISK_CATEGORIES, default='LOW')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Calculate total proceeds if not provided
        if not self.total_proceeds and self.offering_price and self.shares_offered:
            self.total_proceeds = self.offering_price * self.shares_offered
        
        # Calculate fraud risk score based on financial metrics
        self.calculate_risk_score()
        
        super().save(*args, **kwargs)
    
    def calculate_risk_score(self):
        """Calculate fraud risk score based on financial metrics"""
        score = 0
        
        # Revenue growth anomaly (if revenue is too high for industry)
        if self.revenue and self.total_assets:
            revenue_to_assets = self.revenue / self.total_assets
            if revenue_to_assets > 2.0:  # Unusually high revenue for assets
                score += 30
        
        # Profitability issues
        if self.net_income and self.revenue:
            profit_margin = self.net_income / self.revenue
            if profit_margin < 0.05:  # Very low profit margin
                score += 20
            elif profit_margin < 0:  # Negative profit
                score += 40
        
        # High leverage
        if self.total_liabilities and self.total_assets:
            leverage = self.total_liabilities / self.total_assets
            if leverage > 0.8:  # High debt
                score += 25
        
        # Large offering size relative to company size
        if self.total_proceeds and self.total_assets:
            offering_ratio = self.total_proceeds / self.total_assets
            if offering_ratio > 0.5:  # Large offering relative to assets
                score += 15
        
        # Cap the score at 100
        self.fraud_risk_score = min(score, 100)
        
        # Set risk category
        if self.fraud_risk_score >= 70:
            self.risk_category = 'HIGH'
        elif self.fraud_risk_score >= 40:
            self.risk_category = 'MEDIUM'
        else:
            self.risk_category = 'LOW'
    
    def __str__(self):
        return self.company_name


class RedFlag(models.Model):
    SEVERITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    FLAG_TYPES = [
        ('REVENUE_GROWTH_ANOMALY', 'Revenue Growth Anomaly'),
        ('PROFITABILITY_ISSUES', 'Profitability Issues'),
        ('HIGH_LEVERAGE', 'High Leverage'),
        ('LARGE_OFFERING_SIZE', 'Large Offering Size'),
        ('RELATED_PARTY_TRANSACTIONS', 'Related Party Transactions'),
        ('AUDITOR_ISSUES', 'Auditor Issues'),
        ('MANAGEMENT_TURNOVER', 'Management Turnover'),
        ('INCONSISTENT_FINANCIALS', 'Inconsistent Financials'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='red_flags')
    flag_type = models.CharField(max_length=50, choices=FLAG_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    description = models.TextField()
    detected_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.company.company_name} - {self.flag_type}"


class FraudAnalysis(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='fraud_analyses')
    analysis_date = models.DateTimeField(auto_now_add=True)
    risk_factors = models.JSONField()  # Store risk factors as JSON
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)
    recommendations = models.TextField()
    
    def __str__(self):
        return f"Fraud Analysis - {self.company.company_name}"
