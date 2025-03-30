# urls.py
from django.urls import path
from .views import IndividualRegistrationView, NGORegistrationView

urlpatterns = [
    path('api/register/individual/', IndividualRegistrationView.as_view(), name='individual-registration'),
    path('api/register/ngo/', NGORegistrationView.as_view(), name='ngo-registration'),
]