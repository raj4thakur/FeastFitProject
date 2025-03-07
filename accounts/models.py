from mongoengine import Document, StringField, EmailField, BooleanField, DateTimeField, ReferenceField, ListField, IntField, ImageField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime


# User Manager (for MongoEngine)
class UserManager:
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = email.lower()
        user = User(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(email, password, **extra_fields)


# Custom User Model (MongoEngine)
class User(AbstractBaseUser, Document):
    meta = {'collection': 'users'}  # Define collection name in MongoDB

    email = EmailField(unique=True, required=True)
    username = StringField(max_length=50, unique=True, required=True)
    country = StringField(max_length=100, default="")
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    date_joined = DateTimeField(default=datetime.utcnow)
    last_login = DateTimeField(default=datetime.utcnow)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email


# Profile Model
class Profile(Document):
    meta = {'collection': 'profiles'}

    user = ReferenceField(User, required=True, unique=True)
    profile_pic = StringField(default="profile_pics/default.png")  # Image stored as a URL
    full_name = StringField(max_length=100, default="")
    gender = StringField(choices=['male', 'female', 'other'], default="")
    birthdate = DateTimeField(null=True)
    country = StringField(max_length=100, default="")
    allergies = StringField(default="")
    caloric_goals = IntField(default=2000)
    preferred_diet = ListField(StringField())  # Store diet names in a list

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Diet Model
class Diet(Document):
    meta = {'collection': 'diets'}

    name = StringField(max_length=50, required=True, unique=True)

    def __str__(self):
        return self.name


# Recipe Model
class Recipe(Document):
    meta = {'collection': 'recipes'}

    user = ReferenceField(User, required=True)
    title = StringField(max_length=100, required=True)
    description = StringField()
    ingredients = ListField(StringField())  # Store ingredients as a list
    procedure = StringField()
    cuisine = StringField()
    diet_type = StringField()
    allergens = ListField(StringField())  # Store allergens as a list
    preparation_time = IntField()
    cooking_time = IntField()
    servings = IntField()
    image = StringField()  # Store image as a URL or file path
    calories = IntField()
    protein = IntField()
    fat = IntField()
    carbs = IntField()
    likes = IntField(default=0)
    views = IntField(default=0)

    def __str__(self):
        return self.title


# MealPlan Model
class MealPlan(Document):
    meta = {'collection': 'meal_plans'}

    user = ReferenceField(User, required=True)
    name = StringField(max_length=100, required=True)
    details = StringField()

    def __str__(self):
        return self.name


# SavedRecipe Model
class SavedRecipe(Document):
    meta = {'collection': 'saved_recipes'}

    user = ReferenceField(User, required=True)
    recipe = ReferenceField(Recipe, required=True)

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.title}"
