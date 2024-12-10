from django.urls import path
from . import views
from .views import AddThemeView, AddRecommendation

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

    path('clubs/<int:club_id>/recommendations/add/', views.AddRecommendation.as_view(), name='add_recommendation'),
    path('clubs/<int:club_id>/recommendations/', views.view_recommendations, name='view_recommendations'),
    path('clubs/<int:club_id>/members/', views.view_members, name='view_members'),

    
    # Book Discussion URLs
    path('club/<int:club_id>/book-discussion/create/', views.create_book_discussion, name='create_book_discussion'),
    path('book-discussion/<int:book_discussion_id>/', views.book_discussion_detail, name='book_discussion_detail'),
    path('book-discussion/<int:book_discussion_id>/edit/', views.edit_book_discussion, name='edit_book_discussion'),
    path('book-discussion/<int:book_discussion_id>/delete/', views.delete_book_discussion, name='delete_book_discussion'),
    path('profile/<int:member_id>/', views.member_profile, name='member_profile'),  # Other members' profiles

]