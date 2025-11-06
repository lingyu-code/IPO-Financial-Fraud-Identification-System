from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Company, RedFlag, FraudAnalysis
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Company, RedFlag, FraudAnalysis
from .serializers import (
    CompanySerializer, RedFlagSerializer, FraudAnalysisSerializer,
    CompanyWithRedFlagsSerializer, RiskStatisticsSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('-created_at')
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search', 'high_risk_companies']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CompanyWithRedFlagsSerializer
        return CompanySerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            companies = Company.objects.filter(
                Q(company_name__icontains=query) | 
                Q(ticker_symbol__icontains=query) |
                Q(industry__icontains=query)
            )
        else:
            companies = Company.objects.all()
        
        serializer = CompanyWithRedFlagsSerializer(companies, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def high_risk_companies(self, request):
        companies = Company.objects.filter(risk_category='HIGH')
        serializer = CompanyWithRedFlagsSerializer(companies, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def analyze_fraud(self, request, pk=None):
        company = self.get_object()
        
        # Perform fraud analysis
        risk_factors = self._analyze_company_fraud(company)
        
        # Create red flags based on analysis
        self._create_red_flags(company, risk_factors)
        
        # Update company risk score and category
        company.calculate_risk_score()
        company.save()
        
        # Create fraud analysis record
        fraud_analysis = FraudAnalysis.objects.create(
            company=company,
            risk_factors=risk_factors,
            confidence_score=self._calculate_confidence(risk_factors),
            recommendations=self._generate_recommendations(risk_factors)
        )
        
        return Response({
            'message': 'Fraud analysis completed',
            'analysis_id': fraud_analysis.id,
            'updated_risk_score': company.fraud_risk_score,
            'risk_category': company.risk_category
        })
    
    def _analyze_company_fraud(self, company):
        risk_factors = {}
        
        # Revenue growth anomaly
        if company.revenue and company.total_assets:
            revenue_to_assets = float(company.revenue) / float(company.total_assets)
            if revenue_to_assets > 2.0:
                risk_factors['revenue_growth_anomaly'] = {
                    'score': 30,
                    'description': f'Unusually high revenue to assets ratio: {revenue_to_assets:.2f}'
                }
        
        # Profitability issues
        if company.net_income and company.revenue:
            profit_margin = float(company.net_income) / float(company.revenue)
            if profit_margin < 0.05:
                risk_factors['profitability_issues'] = {
                    'score': 20 if profit_margin >= 0 else 40,
                    'description': f'Low profit margin: {profit_margin:.2%}'
                }
        
        # High leverage
        if company.total_liabilities and company.total_assets:
            leverage = float(company.total_liabilities) / float(company.total_assets)
            if leverage > 0.8:
                risk_factors['high_leverage'] = {
                    'score': 25,
                    'description': f'High debt leverage: {leverage:.2f}'
                }
        
        # Large offering size
        if company.total_proceeds and company.total_assets:
            offering_ratio = float(company.total_proceeds) / float(company.total_assets)
            if offering_ratio > 0.5:
                risk_factors['large_offering_size'] = {
                    'score': 15,
                    'description': f'Large offering relative to assets: {offering_ratio:.2f}'
                }
        
        return risk_factors
    
    def _create_red_flags(self, company, risk_factors):
        # Clear existing red flags for this company
        company.red_flags.all().delete()
        
        flag_mapping = {
            'revenue_growth_anomaly': ('REVENUE_GROWTH_ANOMALY', 'HIGH'),
            'profitability_issues': ('PROFITABILITY_ISSUES', 'MEDIUM'),
            'high_leverage': ('HIGH_LEVERAGE', 'HIGH'),
            'large_offering_size': ('LARGE_OFFERING_SIZE', 'MEDIUM')
        }
        
        for factor, (flag_type, severity) in flag_mapping.items():
            if factor in risk_factors:
                RedFlag.objects.create(
                    company=company,
                    flag_type=flag_type,
                    severity=severity,
                    description=risk_factors[factor]['description']
                )
    
    def _calculate_confidence(self, risk_factors):
        # Calculate confidence based on number and severity of risk factors
        base_confidence = 0.8
        factor_count = len(risk_factors)
        
        if factor_count == 0:
            return 0.9  # High confidence for no risk factors
        elif factor_count == 1:
            return 0.7
        elif factor_count == 2:
            return 0.6
        else:
            return 0.5
    
    def _generate_recommendations(self, risk_factors):
        recommendations = []
        
        if 'revenue_growth_anomaly' in risk_factors:
            recommendations.append("Review revenue recognition policies and verify customer contracts.")
        
        if 'profitability_issues' in risk_factors:
            recommendations.append("Analyze cost structure and business model sustainability.")
        
        if 'high_leverage' in risk_factors:
            recommendations.append("Assess debt repayment capability and refinancing risks.")
        
        if 'large_offering_size' in risk_factors:
            recommendations.append("Evaluate the purpose of offering proceeds and growth plans.")
        
        if not recommendations:
            recommendations.append("No immediate concerns identified. Continue monitoring financial performance.")
        
        return "\n".join(recommendations)


class RedFlagViewSet(viewsets.ModelViewSet):
    queryset = RedFlag.objects.all().order_by('-detected_at')
    serializer_class = RedFlagSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = RedFlag.objects.all()
        company_id = self.request.query_params.get('company_id')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset


class FraudAnalysisViewSet(viewsets.ModelViewSet):
    queryset = FraudAnalysis.objects.all().order_by('-analysis_date')
    serializer_class = FraudAnalysisSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = FraudAnalysis.objects.all()
        company_id = self.request.query_params.get('company_id')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset


class FraudDetectionViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'risk_statistics':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=False, methods=['post'])
    def detect_fraud(self, request):
        company_id = request.data.get('company_id')
        try:
            company = Company.objects.get(id=company_id)
            
            # Perform analysis
            risk_factors = {}
            if company.revenue and company.total_assets:
                revenue_to_assets = float(company.revenue) / float(company.total_assets)
                if revenue_to_assets > 2.0:
                    risk_factors['revenue_growth_anomaly'] = 30
            
            if company.net_income and company.revenue:
                profit_margin = float(company.net_income) / float(company.revenue)
                if profit_margin < 0.05:
                    risk_factors['profitability_issues'] = 20 if profit_margin >= 0 else 40
            
            total_risk_score = sum(risk_factors.values())
            
            return Response({
                'company_id': company_id,
                'risk_score': total_risk_score,
                'risk_factors': risk_factors,
                'is_suspicious': total_risk_score > 50
            })
        
        except Company.DoesNotExist:
            return Response(
                {'error': 'Company not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def risk_statistics(self, request):
        total_companies = Company.objects.count()
        high_risk_count = Company.objects.filter(risk_category='HIGH').count()
        medium_risk_count = Company.objects.filter(risk_category='MEDIUM').count()
        low_risk_count = Company.objects.filter(risk_category='LOW').count()
        
        high_risk_percentage = (high_risk_count / total_companies * 100) if total_companies > 0 else 0
        
        statistics = {
            'total_companies': total_companies,
            'high_risk_count': high_risk_count,
            'medium_risk_count': medium_risk_count,
            'low_risk_count': low_risk_count,
            'high_risk_percentage': round(high_risk_percentage, 2)
        }
        
        serializer = RiskStatisticsSerializer(statistics)
        return Response(serializer.data)
