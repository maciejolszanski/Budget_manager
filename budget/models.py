from django.db import models
from django.contrib.auth.models import User

import datetime

# class BudgetManager(models.Manager):
#     '''class that enables creating budget'''
    
#     def create_budget(self, owner):
#         budget = self.create(owner=owner)
#         return budget

class Budget(models.Model):
    '''Class that represents the whole user's budget'''

    name = models.CharField(max_length=200, default='Budget')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Month(models.Model):
    '''Class that represents the month in a year'''

    class monthOfTheYear(models.TextChoices):
        JANUARY = 'January'
        FEBRUARY = 'February'
        MARCH = 'March'
        APRIL = 'April'
        MAY = 'May'
        JUNE = 'June'
        JULY = 'July'
        AUGUST = 'August'
        SEPTEMBER = 'September'
        OCTOBER = 'October'
        NOVEMBER = 'November'
        DECEMBER = 'December'
    
    class theYear(models.IntegerChoices):
        YEAR_2021 = 2021
        YEAR_2022 = 2022
        YEAR_2023 = 2023
        YEAR_2024 = 2024
        YEAR_2025 = 2025

    month = models.CharField(choices=monthOfTheYear.choices, max_length=200)
    year = models.IntegerField(choices=theYear.choices)

    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)

    def __str__(self):
        name = self.month  + ' ' + str(self.year)
        return name

class Category(models.Model):
    '''Category of the spending eg. Food'''

    name = models.CharField(max_length=200)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)

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
