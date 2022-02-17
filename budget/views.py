from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Budget, Category, SubCategory

# Create your views here.
def index(request):
    return render(request, 'budget/index.html')

@login_required
def budget(request):
    '''Main user site'''

    budget = Budget.objects.filter(owner=request.user).get(id=1)
    categories = budget.category_set.all()
    context = {'budget': budget, 'categories': categories}

    return render(request, 'budget/budget.html', context)