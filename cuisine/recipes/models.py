from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Cuisine(models.Model):
    title = models.CharField(max_length=250)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Recipe.Status.PUBLISHED)


class Recipe(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'


    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes_recipe')
    cuisine = models.ManyToManyField(Cuisine,
                                     related_name='recipes_cuisine',
                                     blank=True)
    description = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=250,
                              choices=Status.choices,
                              default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Product(models.Model):
    title = models.CharField(max_length=250)


class Measure(models.Model):
    title = models.CharField(max_length=250)


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                                on_delete=models.CASCADE,
                                related_name='recipes_ingredient')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='recipes_product')
    amount = models.IntegerField()
    measure = models.ForeignKey(Measure,
                                on_delete=models.CASCADE,
                                related_name='recipes_measure')
