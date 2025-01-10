from django.urls import path
from .views import *

urlpatterns = [
    path('create/', MissionCreateView.as_view(), name='mission_create'),
    path('<int:mission_id>/', MissionDetailView.as_view(), name='mission_detail'),
    path('<int:mission_id>/submit/', MissionSubmitView.as_view(), name='mission_submit'),
    path('<int:mission_id>/submits/', MissionAnswerView.as_view(), name='mission_answer'),
    path('<int:mission_id>/close/', MissionCloseView.as_view(), name='mission_close'),
    path('search/', MissionSearchView.as_view(), name='mission_search'),
    path('own/', MissionOwnView.as_view(), name='mission_own'),
    path('<int:mission_id>/delete/', MissionDeleteView.as_view(), name='mission_delete'),
    path('<int:mission_id>/change/', MissionChangeView.as_view(), name='mission_change'),
]
