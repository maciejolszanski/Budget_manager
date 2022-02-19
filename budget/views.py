from re import sub, template
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Budget, Category, SubCategory
from django.views.generic.list import ListView

# Create your views here.
def index(request):
    return render(request, 'budget/index.html')

@login_required
def budget(request):
    '''Main user site'''

    budget = Budget.objects.filter(owner=request.user).get(id=1)
    categories = budget.category_set.all()
    sub_dict = {}
    for category in categories:
        sub_dict[category] = category.subcategory_set.all()

    context = {'budget': budget, 'sub_dict': sub_dict}

    return render(request, 'budget/budget.html', context)
