from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=False)  # Ensures email is required
    
    # Username remains the primary login field
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or self.username


class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('home')

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    selected_themes = models.ManyToManyField(Theme)
    books_per_year = models.CharField(max_length=20, choices=[
        ('0-5', '0-5'),
        ('5-10', '5-10'),
        ('10-20', '10-20'),
        ('20+', '20+'),
    ],
    null=True,
    blank=True,
    )
    profile_pic = (models.ImageField(null=True, blank=True, upload_to="static/profile" ))
    goodreads_url = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return str(self.user)
    
class BookRecommendation(models.Model):
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    goodreads_url = models.CharField(max_length=200, null=True, blank=True)
    cover_image = models.ImageField(upload_to='static/club')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Club(models.Model):
    moderator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="moderated_clubs"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name="joined_clubs", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.ManyToManyField(Theme, related_name="club_theme")
    recommendation = models.ManyToManyField(BookRecommendation, related_name="club_rec", blank=True)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="post_dislikes", blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    upvotes = models.ManyToManyField(User, related_name="post_upvotes", blank=True)
    downvotes = models.ManyToManyField(User, related_name="post_downvotes", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title
    
# Add this to models.py
class BookDiscussion(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='book_discussions')
    book_title = models.CharField(max_length=200)
    book_cover = models.ImageField(upload_to='static/clubs', null=True, blank=True)
    goodreads_url = models.CharField(max_length=200, null=True, blank=True)
    discussion_title = models.CharField(max_length=200)
    discussion_description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.book_title} - {self.discussion_title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    book_discussion = models.ForeignKey(BookDiscussion, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.created_by}'



