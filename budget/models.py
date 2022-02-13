from email.policy import default
from tabnanny import verbose
from tkinter import CASCADE
from django.db import models


class Category(models.Model):
    '''Category of the spending eg. Food'''

    name = models.CharField(max_length=200)
    # it shoul be a sum of all subcategories goals, spending and balances
    # for example:
    # goal_total = sum([sub.goal for sub in food.subcategory_set.all()]) 

    def __str__(self):
        '''returns the model as a string'''
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    '''Subcategory of the spending eg. eating outside in Food category'''

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    goal = models.FloatField(default=0)
    spent = models.FloatField(default=0)
    # balance = goal - spent

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'SubCategories'


