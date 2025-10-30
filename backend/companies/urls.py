from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, RedFlagViewSet, FraudAnalysisViewSet, FraudDetectionViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'red-flags', RedFlagViewSet)
router.register(r'fraud-analysis', FraudAnalysisViewSet)
router.register(r'fraud-detection', FraudDetectionViewSet, basename='fraud-detection')

urlpatterns = [
    path('', include(router.urls)),
]
