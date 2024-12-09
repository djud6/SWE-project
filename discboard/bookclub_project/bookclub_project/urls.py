from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('discussion.urls')),
    path('members/', include('members.urls')),
]
