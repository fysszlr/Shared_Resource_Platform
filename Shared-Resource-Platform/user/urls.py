from django.urls import path
from .views import *

app_name = "user"
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('<int:user_id>/profile/', UserProfileView.as_view(), name='profile'),
    path('<int:user_id>/follows/', UserFollowsView.as_view(), name='follows'),
    path('<int:user_id>/fans/', UserFansView.as_view(), name='fans'),
    path('<int:user_id>/favorites/', UserFavoritesView.as_view(), name='favorites'),
    path('<int:user_id>/modify/', UserModifyView.as_view(), name='modify'),
    path('<int:user_id>/updata_avatar', UserUpdateAvatarView.as_view(), name='update_avatar'),
    path('<int:user_id>/follow/', UserFollowView.as_view(), name='follow'),
    path('<int:user_id>/not_follow/', UserNotFollowView.as_view(), name='unfollow'),
    path('list/', UserListView.as_view(), name='list'),
    path('block/', UserBlockView.as_view(), name='block'),
    path('unblock/', UserUnblockView.as_view(), name='unblock'),
    path('chart/', ChartView.as_view(), name='charts'),
    path('upload/', UserUploadFile.as_view(), name='upload'),
]