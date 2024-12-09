from django.urls import path
from . import views
from .views import AddThemeView

urlpatterns = [
    path('', views.home, name='home'),
    path('clubs/', views.club_list, name='club_list'),
    path('clubs/<int:club_id>/', views.club_detail, name='club_detail'),
    path('clubs/new/', views.club_create, name='club_create'),
    path('theme/new/', AddThemeView.as_view(), name='new_theme'),

    path('clubs/<int:id>/edit/', views.club_update, name='club_update'),
    path('clubs/<int:id>/delete/', views.club_delete, name='club_delete'),

    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('clubs/<int:club_id>/discussions/new/', views.discussion_create, name='discussion_create'),
    path('discussions/<int:id>/edit/', views.discussion_edit, name='discussion_edit'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
    path('discussions/<int:discussion_id>/comments/new/', views.comment_create, name='comment_create'),
    path('comments/<int:id>/delete/', views.comment_delete, name='comment_delete'),
    path('theme/<str:th>/', views.theme_view, name='theme'),
    path('clubs-by-theme/', views.clubs_by_theme_view, name='clubs_by_theme'),

    path('posts/<int:pk>/upvote/', views.upvote_post, name='upvote_post'),
    path('posts/<int:pk>/downvote/', views.downvote_post, name='downvote_post'),
    path('clubs/<int:pk>/like/', views.like_club, name='like_club'),
    path('clubs/<int:pk>/dislike/', views.dislike_club, name='dislike_club'),

    path('clubs/join/<int:pk>/', views.join_club, name='join_club'),
    path('clubs/leave/<int:pk>/', views.leave_club, name='leave_club'),
]