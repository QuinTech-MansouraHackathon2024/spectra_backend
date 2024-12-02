from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import SignUpView
from .views import DoctorListView
from .views import MedicalDataDetailView
from .views import create_medical_data
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('signup/', SignUpView.as_view(), name='signup'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('medical-data/', MedicalDataDetailView.as_view(), name='medical-data'),
    path('medical-data/add/', create_medical_data, name='medical-data-create')
]