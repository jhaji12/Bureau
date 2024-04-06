from django.contrib import admin
from django.urls import path
from transactions.views import TransactionAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transaction/', TransactionAPIView.as_view(), name='transaction_api'),
]
