from django.shortcuts import render, get_object_or_404, redirect
from .models import Club, Post, Comment, Theme, Profile, BookDiscussion, User, BookRecommendation
from .forms import PostForm, CommentForm, ClubForm, BookRecommendationForm, BookDiscussionForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import capfirst
from django.db.models import Q, Count


def home(request):
    # Get all themes
    themes = Theme.objects.all()
    
    # Create a dictionary of clubs by theme
    clubs_by_theme = {}
    for theme in themes:
        clubs = Club.objects.filter(theme=theme)
        if clubs.exists():  # Only include themes with at least one club
            clubs_by_theme[theme] = clubs
    
    return render(request, 'home.html', {'clubs_by_theme': clubs_by_theme})



def club_list(request):
    search_query = request.GET.get('q', '')  # Get search query from request
    if search_query:
        clubs = Club.objects.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        ).distinct()  # Search by name, description, or theme
    else:
        clubs = Club.objects.all()
    return render(request, 'club_list.html', {'clubs': clubs, 'search_query': search_query})

def post_list(request):
    clubs = Club.posts.all()
    return render(request, 'club_detail.html', {'clubs': clubs})



def club_detail(request, club_id):
    is_moderator = is_club_moderator(request.user, club_id)
    club = get_object_or_404(Club, id=club_id)
    is_member = club.members.filter(id=request.user.id).exists()
    return render(request, 'club_detail.html', {
        'club': club,
        'is_moderator': is_moderator,
        'is_member': is_member
        })

def post_detail(request, id):
    is_moderator = is_post_moderator(request.user, id)
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()  # Fetch all comments related to the post
    
    # Handle the inline comment form submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Link the comment to the current post
            comment.created_by = request.user  # Assign the logged-in user as the creator
            comment.save()
            return redirect('post_detail', id=post.id)  # Redirect to the same page to clear the form
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'is_moderator': is_moderator,
    }
    
    return render(request, 'post_detail.html', context)


def is_club_moderator(user, club_id):
    """Check if the user is the moderator of the club"""
    club = get_object_or_404(Club, id=club_id)
    return user == club.moderator

def is_post_moderator(user, club_id):
    """Check if the user is the moderator of the club"""
    post = get_object_or_404(Post, id=club_id)
    return user == post.created_by

def is_Bookpost_moderator(user, book_discussion_id):
    book_discussion = get_object_or_404(BookDiscussion, id=book_discussion_id)
    return user == book_discussion.created_by or user == book_discussion.club.moderator



class AddThemeView(LoginRequiredMixin, CreateView):
    model = Theme
    template_name = 'new_theme.html'
    fields = '__all__'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Capitalize the first word of the theme name
        form.instance.name = capfirst(form.instance.name)
        return super().form_valid(form)

@login_required
def club_create(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.moderator = request.user
            club.save()

            club.theme.set(form.cleaned_data['theme'])

            # Process new themes
            new_theme_name = request.POST.get('new_theme')
            if new_theme_name:
                new_theme_name = capfirst(new_theme_name)
                new_theme, created = Theme.objects.get_or_create(name=new_theme_name)
                club.theme.add(new_theme)

            return redirect('club_detail', club_id=club.id)  # Matches <int:club_id>
    else:
        form = ClubForm()
    return render(request, 'new_club.html', {'form': form})

@login_required
def club_update(request, id):  # Matches <int:id>
    club = get_object_or_404(Club, id=id)
    if request.user != club.moderator:
        return redirect('club_detail', club_id=id)  # Matches <int:club_id>
    if request.method == 'POST':
        form = ClubForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            return redirect('club_detail', club_id=id)  # Matches <int:club_id>
    else:
        form = ClubForm(instance=club)
    return render(request, 'new_club.html', {'form': form})


@login_required
def club_delete(request, id):  # Matches <int:id>
    club = get_object_or_404(Club, id=id)
    if request.user != club.moderator:
        return redirect('club_detail', club_id=id)  # Matches <int:club_id>
    if request.method == 'POST':
        club.delete()
        return redirect('club_list')
    return render(request, 'club_confirm_delete.html', {'club': club})



@login_required
def discussion_create(request, club_id):  # Matches <int:club_id>
    club = get_object_or_404(Club, id=club_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.club_id = club_id
            discussion.created_by = request.user
            discussion.save()
            return redirect('post_detail', id=discussion.id)  # Matches <int:id>
    else:
        form = PostForm()
    return render(request, 'discussion_form.html', {'form': form})



class AddRecommendation(LoginRequiredMixin, CreateView):
    model = BookRecommendation
    template_name = 'add_recommendation.html'
    form_class = BookRecommendationForm  # Ensure the form class is used

    def form_valid(self, form):
        form.instance.recommended_by = self.request.user  # Set the current user
        club_id = self.kwargs.get('club_id')
        club = get_object_or_404(Club, id=club_id)
        form.instance.title = capfirst(form.instance.title)  # Capitalize the title
        self.object = form.save()
        club.recommendation.add(self.object)  # Add the recommendation to the club
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the specific club detail page
        return reverse('club_detail', kwargs={'club_id': self.kwargs['club_id']})





def view_recommendations(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    recommendations = club.recommendation.all()  # Fetch recommendations linked to this club
    return render(request, 'view_recommendations.html', {'club': club, 'recommendations': recommendations})


def view_members(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    members = club.members.all()
    return render(request, 'view_members.html', {'club': club, 'members': members})




@login_required
def discussion_edit(request, id):  # Matches <int:id>
    discussion = get_object_or_404(Post, id=id)
    if request.user != discussion.created_by:
        return redirect('post_detail', id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            return redirect('club_detail', club_id=discussion.club.id)  # Matches <int:club_id>
    else:
        form = PostForm(instance=discussion)
    return render(request, 'discussion_form.html', {'form': form})


@login_required
def delete_post(request, post_id):  # Matches <int:id>
     # Retrieve the post or return a 404 if it doesn't exist
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the current user is the creator of the post
    if request.user != post.created_by:
        return redirect('club_detail', club_id=post.club.id)
    
    if request.method == 'POST':
        # Delete the post and redirect to the club's detail page
        post.delete()
        return redirect('club_detail', club_id=post.club.id)
    
    # Render a confirmation template for GET requests
    return render(request, 'post_confirm_delete.html', {'post': post})
@login_required
def comment_create(request, discussion_id):  # Matches <int:discussion_id>
    discussion = get_object_or_404(Post, id=discussion_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = discussion
            comment.created_by = request.user
            comment.save()
            return redirect('post_detail', id=discussion.id)  # Matches <int:id>
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'discussion': discussion})

@login_required
def comment_delete(request, id):  # Matches <int:id>
    comment = get_object_or_404(Comment, id=id)
    if (request.user != comment.created_by and 
        request.user != comment.post.created_by and 
        request.user != comment.post.club.moderator):
        return redirect('post_detail', id=comment.post.id)  # Matches <int:id>
    if request.method == 'POST':
        comment.delete()
    return redirect('post_detail', id=comment.post.id)  # Matches <int:id>

# views.py
def theme_view(request, th):
    # Find clubs that have the specified theme
    theme_posts = Club.objects.filter(theme__name=th)

    context = {
        'th': th,
        'theme_posts': theme_posts
    }

    return render(request, 'themes.html', context)


def clubs_by_theme_view(request):
    # Get all themes from the database
    themes = Theme.objects.all()
    
    # Create a dictionary to hold the theme and related clubs
    clubs_by_theme = {}
    for theme in themes:
        # Get all clubs that have the current theme
        clubs = Club.objects.filter(theme=theme)
        if clubs.exists():  # Only include themes that have associated clubs
            clubs_by_theme[theme] = clubs

    # Pass the grouped data to the template
    context = {
        'clubs_by_theme': clubs_by_theme,
    }
    
    return render(request, 'clubs_by_theme.html', context)


@login_required
def like_club(request, pk):
    club = get_object_or_404(Club, id=pk)
    if request.user in club.dislikes.all():
        club.dislikes.remove(request.user)  # Remove dislike if the user switches to like
    if request.user not in club.likes.all():
        club.likes.add(request.user)  # Add like
    else:
        club.likes.remove(request.user)  # Toggle off like
    return redirect('club_detail', club_id=club.id)


@login_required
def dislike_club(request, pk):
    club = get_object_or_404(Club, id=pk)
    if request.user in club.likes.all():
        club.likes.remove(request.user)  # Remove like if the user switches to dislike
    if request.user not in club.dislikes.all():
        club.dislikes.add(request.user)  # Add dislike
    else:
        club.dislikes.remove(request.user)  # Toggle off dislike
    return redirect('club_detail', club_id=club.id)



@login_required
def upvote_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.downvotes.all():
        post.downvotes.remove(request.user)  # Remove downvote if the user switches to upvote
    if request.user not in post.upvotes.all():
        post.upvotes.add(request.user)  # Add upvote
    else:
        post.upvotes.remove(request.user)  # Toggle off upvote
    return redirect('post_detail', id=post.id)

@login_required
def downvote_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.upvotes.all():
        post.upvotes.remove(request.user)  # Remove upvote if the user switches to downvote
    if request.user not in post.downvotes.all():
        post.downvotes.add(request.user)  # Add downvote
    else:
        post.downvotes.remove(request.user)  # Toggle off downvote
    return redirect('post_detail', id=post.id)

@login_required
def join_club(request, pk):
    club = get_object_or_404(Club, id=pk)
    club.members.add(request.user)
    return redirect('club_detail', club_id=club.id)

# Leave a Club
@login_required
def leave_club(request, pk):
    club = get_object_or_404(Club, id=pk)
    club.members.remove(request.user)
    return redirect('club_detail', club_id=club.id)


# Add these views to views.py
@login_required
def create_book_discussion(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    
    # Only moderator can create book discussions
    if request.user != club.moderator:
        return redirect('club_detail', club_id=club.id)
    
    if request.method == 'POST':
        form = BookDiscussionForm(request.POST, request.FILES)
        if form.is_valid():
            book_discussion = form.save(commit=False)
            book_discussion.club = club
            book_discussion.created_by = request.user
            book_discussion.save()
            return redirect('book_discussion_detail', book_discussion_id=book_discussion.id)
    else:
        form = BookDiscussionForm()
    
    return render(request, 'create_book_discussion.html', {
        'form': form, 
        'club': club
    })

def book_discussion_detail(request, book_discussion_id):
    is_moderator = is_Bookpost_moderator(request.user.id, book_discussion_id)
    book_discussion = get_object_or_404(BookDiscussion, id=book_discussion_id)

    
    # Handle comment submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = book_discussion  # This requires updating the Comment model
            comment.created_by = request.user
            comment.save()
            return redirect('book_discussion_detail', book_discussion_id=book_discussion.id)
    else:
        form = CommentForm()
    
    context = {
        'book_discussion': book_discussion,
        'comments': book_discussion.comments.all(),
        'form': form,
        'is_moderator': is_moderator,
    }
    
    return render(request, 'book_discussion_detail.html', context)


@login_required
def edit_book_discussion(request, book_discussion_id):
    book_discussion = get_object_or_404(BookDiscussion, id=book_discussion_id)
    if request.user != book_discussion.club.moderator:
        return redirect('book_discussion_detail', book_discussion_id=book_discussion.id)
    if request.method == 'POST':
        form = BookDiscussionForm(request.POST, request.FILES, instance=book_discussion)
        if form.is_valid():
            form.save()
            return redirect('book_discussion_detail', book_discussion_id=book_discussion.id)
    else:
        form = BookDiscussionForm(instance=book_discussion)
    return render(request, 'create_book_discussion.html', {'form': form, 'book_discussion': book_discussion, 'editing': True})


@login_required
def delete_book_discussion(request, book_discussion_id):
    book_discussion = get_object_or_404(BookDiscussion, id=book_discussion_id)
    if request.user != book_discussion.club.moderator:
        return redirect('club_detail', club_id=book_discussion.club.id)
    if request.method == 'POST':
        book_discussion.delete()
        return redirect('club_detail', club_id=book_discussion.club.id)
    return render(request, 'book_discussion_confirm_delete.html', {'book_discussion': book_discussion})

def member_profile(request, member_id):
    member = get_object_or_404(Profile, user__id=member_id)
    created_clubs = member.user.moderated_clubs.all()
    joined_clubs = member.user.joined_clubs.all()

    context = {
        'member': member,
        'created_clubs': created_clubs,
        'joined_clubs': joined_clubs,
    }

    return render(request, 'member_profile.html', context)
