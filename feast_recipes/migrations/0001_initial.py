# Generated by Django 3.1.12 on 2024-12-29 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('cuisine', models.CharField(max_length=100)),
                ('diet_type', models.CharField(max_length=50)),
                ('ingredients', models.TextField()),
                ('procedure', models.TextField()),
                ('allergens', models.TextField(blank=True, null=True)),
                ('prep_time', models.PositiveIntegerField()),
                ('cook_time', models.PositiveIntegerField()),
                ('servings', models.PositiveIntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipe_images/')),
                ('calories', models.PositiveIntegerField(blank=True, null=True)),
                ('protein', models.PositiveIntegerField(blank=True, null=True)),
                ('fat', models.PositiveIntegerField(blank=True, null=True)),
                ('carbs', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
