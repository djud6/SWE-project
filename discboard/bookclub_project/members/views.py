from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import logout, login
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import UserProfileEditForm #, CustomUserCreationForm 
from django.contrib.auth.decorators import login_required
from discussion.models import Profile, User, Theme
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from .forms import RegisterForm, ProfileSetupForm, ThemeSelectionForm, BooksPerYearForm, ProfilePictureForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_setup')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

def profile_setup(request):
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('theme_selection')
    else:
        form = ProfileSetupForm()
    return render(request, 'profile/profile_setup.html', {'form': form} )

def theme_selection(request):
    if request.method == 'POST':
        form = ThemeSelectionForm(request.POST)
        if form.is_valid():
            themes = form.cleaned_data['themes']
            profile = request.user.profile
            profile.selected_themes.set(themes)
            return redirect('books_per_year')
    else:
        form = ThemeSelectionForm()
        themes = Theme.objects.all()
    return render(request, 'profile/theme_selection.html', {'form': form, 'themes': themes})

def books_per_year(request):
    if request.method == 'POST':
        form = BooksPerYearForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            profile.books_per_year = form.cleaned_data['books_per_year']
            profile.save()
            return redirect('home')
    else:
        form = BooksPerYearForm()
    return render(request, 'profile/books_per_year.html', {'form': form})



# class UserRegisterView(generic.CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'registration/register.html'
#     success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('home')


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile  # The model to update
    form_class = UserProfileEditForm  # The form to use for editing
    template_name = 'profile/edit_profile.html'
    
    
    def get_object(self):
        # Ensure the view gets the profile of the currently logged-in user
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get_form_kwargs(self):
        # Pass the user instance to the form
        kwargs = super().get_form_kwargs()
        kwargs['user_instance'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})

    

def profile_view(request, user_id):
    if request.user.id != user_id:
        messages.error(request, "You can only edit your own profile.")
        return redirect('home')
    
    profile = get_object_or_404(Profile, user__id=user_id)
    created_clubs = profile.user.moderated_clubs.all()
    joined_clubs = profile.user.joined_clubs.all()

    # Handle profile picture upload
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('profile', user_id=user_id)

    else:
        form = ProfilePictureForm(instance=profile)

    context = {
        'profile': profile,
        'created_clubs': created_clubs,
        'joined_clubs': joined_clubs,
        'profile_picture_form': form,
    }
    return render(request, 'profile/profile.html', context)