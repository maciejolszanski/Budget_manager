from django.db import models
from django.contrib.auth.models import User


class Budget(models.Model):
    '''Class that represents the whole user's budget'''

    name = models.CharField(max_length=200, default='Budget')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Category(models.Model):
    '''Category of the spending eg. Food'''

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    # it shoul be a sum of all subcategories goals, spending and balances
    # for example:
    # goal_total = sum([sub.goal for sub in food.subcategory_set.all()]) 

    def __str__(self):
        '''returns the model as a string'''
        return self.name

    def sum_goals(self):
        '''sum all of the subcategories goals'''
        goal_total = sum([sub.goal for sub in self.subcategory_set.all()])
        return goal_total

    def sum_spendings(self):
        '''sum all of the subcategories spendings'''
        spent_total = sum([sub.spent for sub in self.subcategory_set.all()])
        return spent_total

    def calc_balance(self):
        '''calculate the balance of whole category'''
        return self.sum_goals() - self.sum_spendings()

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    '''Subcategory of the spending eg. eating outside in Food category'''

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    goal = models.FloatField(default=0)
    spent = models.FloatField(default=0)
    
    def calc_balance(self):
        '''calculate the balance of subcategory'''
        return self.goal - self.spent

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'SubCategories'
