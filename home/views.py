from django.shortcuts import render
from .db import recipes_collection, users_profiles  # Import the MongoDB collections
from feast_recipes.models import RecipeInteraction  # Import the RecipeInteraction model

def home(request):
    # Fetch recipes from MongoDB
    # recipes = list(recipes_collection.find().limit(8))  # Convert cursor to list for Django templates

    # # Fetch interactions from the Django database for the logged-in user
    # interactions = RecipeInteraction.objects.filter(user=request.user)
    # interaction_dict = {str(interaction.recipe.id): interaction for interaction in interactions}  # Match MongoDB ID with Django model ID

    # # Loop through MongoDB recipes and add `liked` and `is_saved` based on interactions
    # for recipe in recipes:
    #     # Convert the MongoDB _id to a string (if necessary) for comparison
    #     recipe['_id'] = str(recipe['_id'])  # Ensure MongoDB _id is a string for comparison

    #     # Get the interaction for the recipe, if it exists
    #     interaction = interaction_dict.get(recipe['_id'])

    #     # Assign the `liked` and `saved` flags based on the interaction or default to False
    #     recipe['liked'] = interaction.liked if interaction else False
    #     recipe['is_saved'] = interaction.saved if interaction else False

    # print("Got recipes for home template!")

    # # Fetch profile picture for the logged-in user
    # user_profile_pic = None
    # if request.user.is_authenticated:
    #     # Find the profile associated with the logged-in user
    #     user_profile = users_profiles.find_one({'user_id': request.user.id})
    #     if user_profile and 'profile_pic' in user_profile:  # Ensure 'profile_pic' key exists
    #         user_profile_pic = user_profile['profile_pic']

    # return render(request, 'home/home.html', {
    #     'recipes': recipes,
    #     'profile_pic': user_profile_pic,  # Pass profile picture to template
    # })
    return render(request,'home/home.html')