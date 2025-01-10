from django.urls import path
from .views import *

urlpatterns = [
    path('unread/', NotificationUnreadView.as_view(), name='unread'),
    path('Search/', NotificationSearchView.as_view(), name='search'),
    path('<uuid:notificationId>/', NotificationDetailView.as_view(), name='detail'),
    path('read_all/', NotificationReadAllView.as_view(), name='read_all'),
]