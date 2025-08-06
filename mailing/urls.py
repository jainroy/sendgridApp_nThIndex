from django.urls import path
from .views import SendMailView, AddEmailView, SendBulkMailView

urlpatterns = [
    path('send-mail/', SendMailView.as_view(), name='send-mail'),
    path('add-email/', AddEmailView.as_view(), name='add-emai'),
    path('send-bulk-mail/', SendBulkMailView.as_view(), name='send-bulk-mail'),
]