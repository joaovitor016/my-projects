from django.conf.urls import url, include
from rest_framework import routers
from core.views_api import UserViewSet, PersonalDataViewSet, ProfessionalDataViewSet, FinancialDataViewSet, \
    UserProfileViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'personal', PersonalDataViewSet)
router.register(r'professional', ProfessionalDataViewSet)
router.register(r'financial', FinancialDataViewSet)
router.register(r'profile', UserProfileViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
