from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import json

from .models import Recipe, RecipeInteraction, RecipeRating
from django.conf import settings

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/') 
db = client['FeastFit_DataBase']
users_profiles = db['accounts_profile']


# Recipes List View
def recipes(request):
    recipes_query = Recipe.objects()
    search = request.GET.get('search', '')
    if search:
        recipes_query = recipes_query.filter(title__icontains=search)
    cuisine = request.GET.get('cuisine', '')
    if cuisine:
        recipes_query = recipes_query.filter(cuisine__iexact=cuisine)
    ingredient = request.GET.get('ingredient', '')
    if ingredient:
        recipes_query = recipes_query.filter(ingredients__contains=ingredient)
    diet = request.GET.get('diet', '')
    if diet:
        recipes_query = recipes_query.filter(diet_type__iexact=diet)

    paginator = Paginator(list(recipes_query), 8) 
    page_number = request.GET.get('page')
    all_recipes = paginator.get_page(page_number)

    user_profile_pic = None
    if request.user.is_authenticated:
        user_profile = users_profiles.find_one({'user_id': request.user.id})
        if user_profile and 'profile_pic' in user_profile:
            user_profile_pic = user_profile['profile_pic']

    recipe_profiles = []
    for recipe in all_recipes:
        user_profile = users_profiles.find_one({'user_id': recipe.created_by.id})
        if user_profile:
            recipe_profiles.append({
                'recipe_id': str(recipe.id),
                'username': user_profile.get('full_name'),
                'profile_pic': user_profile.get('profile_pic'),
            })

    context = {
        'all_recipes': all_recipes,
        'profile_pic': user_profile_pic,
        'recipe_profiles': recipe_profiles,
    }
    return render(request, 'feast_recipes/recipes.html', context)


# Upload Recipe View
def upload_recipe(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        procedure = request.POST.get('procedure')
        cuisine = request.POST.get('cuisine')
        diet_type = request.POST.get('diet_type')
        ingredients = request.POST.get('ingredients').split(',')
        allergens = request.POST.get('allergens', '').split(',')
        prep_time = request.POST.get('prep_time')
        cook_time = request.POST.get('cook_time')
        servings = request.POST.get('servings')
        image = request.FILES.get('image')
        calories = request.POST.get('calories', None)
        protein = request.POST.get('protein', None)
        fat = request.POST.get('fat', None)
        carbs = request.POST.get('carbs', None)

        if not request.user.is_authenticated:
            messages.error(request, "You need to be logged in to upload a recipe.")
            return redirect('accounts:login')

        recipe = Recipe(
            title=title,
            description=description,
            procedure=procedure,
            cuisine=cuisine,
            diet_type=diet_type,
            ingredients=ingredients,
            allergens=allergens,
            preparation_time=int(prep_time),
            cooking_time=int(cook_time),
            servings=int(servings),
            image=str(image) if image else None,
            calories=int(calories) if calories else None,
            protein=float(protein) if protein else None,
            fat=float(fat) if fat else None,
            carbs=float(carbs) if carbs else None,
            created_by=request.user
        )

        recipe.save()
        messages.success(request, "Recipe uploaded successfully!")
        return redirect('home:home')

    return render(request, 'feast_recipes/upload_recipe.html')


# Recipe Content View
def recipe_content(request, recipe_id):
    recipe = Recipe.objects(id=recipe_id).first()
    if not recipe:
        return JsonResponse({"error": "Recipe not found"}, status=404)

    recipe.views += 1
    recipe.save()

    return render(request, 'feast_recipes/recipe_content.html', {
        'recipe': recipe,
        'MEDIA_URL': settings.MEDIA_URL
    })


# Like Recipe API
@csrf_exempt
def like_recipe(request, recipe_id):
    if request.method == "POST":
        recipe = Recipe.objects(id=recipe_id).first()
        if not recipe:
            return JsonResponse({"success": False, "error": "Recipe not found"})

        interaction = RecipeInteraction.objects(user=request.user, recipe=recipe).first()
        if not interaction:
            interaction = RecipeInteraction(user=request.user, recipe=recipe)

        interaction.toggle_like()

        return JsonResponse({"success": True, "liked": interaction.liked, "likes": recipe.likes})

    return JsonResponse({"success": False})


# Save Recipe API
@csrf_exempt
def save_recipe(request, recipe_id):
    if request.method == "POST":
        recipe = Recipe.objects(id=recipe_id).first()
        if not recipe:
            return JsonResponse({"success": False, "error": "Recipe not found"})

        interaction = RecipeInteraction.objects(user=request.user, recipe=recipe).first()
        if not interaction:
            interaction = RecipeInteraction(user=request.user, recipe=recipe)

        interaction.toggle_save()

        return JsonResponse({"success": True, "saved": interaction.saved})

    return JsonResponse({"success": False})


# Increment View Count API
def increment_view_count(request, recipe_id):
    recipe = Recipe.objects(id=recipe_id).first()
    if not recipe:
        return JsonResponse({"success": False, "error": "Recipe not found"})

    recipe.views += 1
    recipe.save()
    return JsonResponse({'status': 'success', 'views': recipe.views})
