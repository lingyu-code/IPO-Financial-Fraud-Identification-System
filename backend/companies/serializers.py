from rest_framework import serializers
from .models import Company, RedFlag, FraudAnalysis


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'company_name', 'ticker_symbol', 'industry', 'offering_date',
            'offering_price', 'shares_offered', 'total_proceeds', 'revenue',
            'net_income', 'total_assets', 'total_liabilities', 'fraud_risk_score',
            'risk_category', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'fraud_risk_score', 'risk_category', 'created_at', 'updated_at']


class RedFlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedFlag
        fields = ['id', 'company', 'flag_type', 'severity', 'description', 'detected_at']
        read_only_fields = ['id', 'detected_at']


class FraudAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = FraudAnalysis
        fields = ['id', 'company', 'analysis_date', 'risk_factors', 'confidence_score', 'recommendations']
        read_only_fields = ['id', 'analysis_date']


class CompanyWithRedFlagsSerializer(CompanySerializer):
    red_flags = RedFlagSerializer(many=True, read_only=True)
    
    class Meta(CompanySerializer.Meta):
        fields = CompanySerializer.Meta.fields + ['red_flags']


class RiskStatisticsSerializer(serializers.Serializer):
    total_companies = serializers.IntegerField()
    high_risk_count = serializers.IntegerField()
    medium_risk_count = serializers.IntegerField()
    low_risk_count = serializers.IntegerField()
    high_risk_percentage = serializers.FloatField()
