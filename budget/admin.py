from django.contrib import admin
from budget.models import SubCategory

from .models import Category, SubCategory

admin.site.register(Category)
admin.site.register(SubCategory)