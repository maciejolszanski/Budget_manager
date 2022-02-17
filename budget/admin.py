from django.contrib import admin
from budget.models import SubCategory

from .models import Category, SubCategory, Budget

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Budget)