from django.urls import path
from .views import *

urlpatterns = [
    path('index/', BillboardIndexView.as_view(), name='index'),
    path('<int:noticeId>/', BillboardDetailView.as_view(), name='billboard_detail'),
    path('create/', BillboardCreateView.as_view(), name='billboard_create'),
    path('modify/', BillboardModifyView.as_view(), name='billboard_modify'),
]