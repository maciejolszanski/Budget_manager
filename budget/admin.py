from django.contrib import admin
from budget.models import SubCategory

from .models import Category, SubCategory, Budget, Month

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Budget)
admin.site.register(Month)