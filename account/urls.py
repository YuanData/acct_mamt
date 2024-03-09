from django.urls import path

from .views import AccountCreateAPIView, AccountVerifyAPIView

urlpatterns = [
    path('create/', AccountCreateAPIView.as_view(), name='account-create'),
    path('verify/', AccountVerifyAPIView.as_view(), name='account-verify'),
]
