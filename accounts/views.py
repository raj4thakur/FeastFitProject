from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, ProfileForm, ProfilePicForm, DietaryPreferencesForm
from .models import User, Profile, Recipe, SavedRecipe, MealPlan
from pymongo import MongoClient

# -------------------- LOGIN VIEW --------------------
def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home:home')  # Redirect to home page
        else:
            error = "Invalid email or password. Please try again."

    return render(request, 'accounts/login.html', {'error': error})


# -------------------- REGISTER VIEW --------------------
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login
            messages.success(request, 'Registration successful! Welcome to FeastFit.')
            return redirect('home:home')
        else:
            messages.error(request, 'Please fix the errors below.')

    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


# -------------------- LOGOUT VIEW --------------------
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home:home')


# -------------------- PROFILE VIEW --------------------
@login_required
def profile_view(request):
    """Display user profile, including uploaded recipes."""
    # Fetch user profile from MongoDB
    profile = Profile.objects(user=request.user).first()
    if not profile:
        profile = Profile(user=request.user)
        profile.save()

    # MongoDB connection
    client = MongoClient('mongodb://localhost:27017/')
    db = client['FeastFit_DataBase']
    recipes_collection = db['feast_recipes_recipe']

    # Get recipes created by the user
    user_id = str(request.user.id)  # Convert to string for MongoDB lookup
    recipes = list(recipes_collection.find({"user_id": user_id}))

    context = {
        'user': request.user,
        'profile': profile,
        'recipes': recipes,
    }
    return render(request, 'accounts/profile.html', context)


# -------------------- UPDATE PROFILE --------------------
@login_required
def update_profile(request):
    """Update user profile information."""
    profile = Profile.objects(user=request.user).first()

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
        else:
            messages.error(request, "Error updating profile. Please check your inputs.")

    return redirect('accounts:profile')


# -------------------- UPLOAD PROFILE PICTURE --------------------
@login_required
def upload_profile_pic(request):
    """Upload or update user profile picture."""
    profile = Profile.objects(user=request.user).first()

    if request.method == 'POST':
        new_pic = request.FILES.get('new_profile_pic')
        if new_pic:
            profile.profile_pic = new_pic
            profile.save()
            messages.success(request, 'Profile picture updated successfully.')
        else:
            messages.error(request, 'Please select a valid image.')

    return redirect('accounts:profile')


# -------------------- UPDATE DIETARY PREFERENCES --------------------
@login_required
def update_dietary_preferences(request):
    """Update dietary preferences."""
    profile = Profile.objects(user=request.user).first()

    if request.method == 'POST':
        dietary_form = DietaryPreferencesForm(request.POST, instance=profile)
        if dietary_form.is_valid():
            dietary_form.save()
            messages.success(request, "Dietary preferences updated successfully!")
        else:
            messages.error(request, "Error updating dietary preferences.")

    return redirect('accounts:profile')


# -------------------- PLACEHOLDER FUNCTIONS --------------------
@login_required
def feedback(request):
    """User feedback submission (to be implemented)."""
    pass


def help_support(request):
    """Help and support page (to be implemented)."""
    pass


def update_security_settings(request):
    """Update security settings (to be implemented)."""
    pass
