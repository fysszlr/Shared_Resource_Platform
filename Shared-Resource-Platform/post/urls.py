from django.urls import path
from .views import *

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:post_id>/', PostDetailView.as_view(), name='detail'),
    path('<int:post_id>/comments/', PostCommentDetailView.as_view(), name='comments'),
    path('<int:post_id>/comments/create/', PostCommentCreateView.as_view(), name='comments_create'),
    path('<int:post_id>/favour/', PostFavouriteView.as_view(), name='favourite'),
    path('<int:post_id>/not_favour/', PostUnfavouriteView.as_view(), name='not_favourite'),
    path('<int:post_id>/like/', PostLikeView.as_view(), name='like'),
    path('<int:post_id>/not_like/', PostUnlikeView.as_view(), name='unlike'),
    path('<int:post_id>/dislike/', PostDislikeView.as_view(), name='dislike'),
    path('<int:post_id>/not_dislike/', PostUndislikeView.as_view(), name='undislike'),
    path('search/', PostSearchView.as_view(), name='search'),
    path('own/', PostOwnView.as_view(), name='own'),
    path('<int:post_id>/change/', PostChangeView.as_view(), name='change'),
    path('delete/', PostDeleteView.as_view(), name='delete'),
    path('<int:post_id>/confirmPay/', PostPayView.as_view(), name='confirmPay'),
    path('new/', PostNewView.as_view(), name='new'),
]