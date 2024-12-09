from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserLoginView, logout_view, EditProfileView # UserRegisterView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile-setup/', views.profile_setup, name='profile_setup'),
    path('theme-selection/', views.theme_selection, name='theme_selection'),
    path('books-per-year/', views.books_per_year, name='books_per_year'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('edit_profile/', EditProfileView.as_view(), name='edit-profile'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name = 'registration/change_password.html'), name='change-password'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
]
