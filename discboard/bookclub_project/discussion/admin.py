from django.contrib import admin
from .models import Club, Post, Comment, Profile, Theme, User, BookRecommendation, BookDiscussion

admin.site.register(Club)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(Theme)
admin.site.register(User)
admin.site.register(BookRecommendation)
admin.site.register(BookDiscussion)

