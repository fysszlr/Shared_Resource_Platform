from django.urls import path
from .views import *

urlpatterns = [
    path('create/', TagCreateView.as_view(), name='create'),
    path('search/', TagSearchView.as_view(), name='search')
]