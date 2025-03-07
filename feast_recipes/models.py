from mongoengine import (
    Document, StringField, IntField, FloatField, BooleanField, 
    ReferenceField, DateTimeField, ListField, CASCADE
)
import datetime

# Recipe Model
class Recipe(Document):
    title = StringField(max_length=100, required=True)
    description = StringField()
    procedure = StringField()
    cuisine = StringField(max_length=50)
    diet_type = StringField(max_length=50)
    preparation_time = IntField()  # Time in minutes
    cooking_time = IntField()  # Time in minutes
    servings = IntField(default=3)  
    ingredients = ListField(StringField())  # Store ingredients as a list
    allergens = ListField(StringField(), default=[])  # Store allergens as a list
    calories = IntField()
    fat = FloatField()
    protein = FloatField()
    carbs = FloatField()
    views = IntField(default=0)
    average_rating = FloatField(default=0.0)
    total_reviews = IntField(default=0)
    likes = IntField(default=0)
    image = StringField()  # Store image URL or path
    saved = IntField(default=0)

    created_by = ReferenceField("User", reverse_delete_rule=CASCADE)  # Using AUTH_USER_MODEL
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    def update_average_rating(self):
        total_ratings = RecipeRating.objects(recipe=self).count()
        if total_ratings > 0:
            self.average_rating = sum(r.rating for r in RecipeRating.objects(recipe=self)) / total_ratings
        else:
            self.average_rating = 0
        self.save()

    def __str__(self):
        return self.title


# Recipe Interaction Model
class RecipeInteraction(Document):
    user = ReferenceField("User", required=True, reverse_delete_rule=CASCADE)
    recipe = ReferenceField(Recipe, required=True, reverse_delete_rule=CASCADE)
    liked = BooleanField(default=False)
    saved = BooleanField(default=False)
    shared = BooleanField(default=False)

    def toggle_like(self):
        if self.liked:
            self.liked = False
            self.recipe.likes -= 1
        else:
            self.liked = True
            self.recipe.likes += 1
        self.recipe.save()
        self.save()

    def toggle_save(self):
        self.saved = not self.saved
        self.save()

    def __str__(self):
        return f"{self.user} - {self.recipe} ({'Liked' if self.liked else 'Not Liked'})"


# Recipe Rating Model
class RecipeRating(Document):
    user = ReferenceField("User", required=True, reverse_delete_rule=CASCADE)
    recipe = ReferenceField(Recipe, required=True, reverse_delete_rule=CASCADE)
    rating = IntField(choices=[1, 2, 3, 4, 5], required=True)
    comment = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return f"Rating by {self.user} on {self.recipe.title}"
