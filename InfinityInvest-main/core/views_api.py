from rest_framework import viewsets
from core.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes


# https://www.django-rest-framework.org/tutorial/1-serialization/
# https://docs.djangoproject.com/en/3.1/topics/db/queries/
@permission_classes([IsAuthenticated, IsAdminUser])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes([IsAuthenticated, IsAdminUser])
class PersonalDataViewSet(viewsets.ModelViewSet):
    queryset = PersonalData.objects.all()
    serializer_class = PersonalDataSerializer


@permission_classes([IsAuthenticated, IsAdminUser])
class ProfessionalDataViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalData.objects.all()
    serializer_class = ProfessionalDataSerializer


@permission_classes([IsAuthenticated, IsAdminUser])
class FinancialDataViewSet(viewsets.ModelViewSet):
    queryset = FinancialData.objects.all()
    serializer_class = FinancialDataSerializer


@permission_classes([IsAuthenticated, IsAdminUser])
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
