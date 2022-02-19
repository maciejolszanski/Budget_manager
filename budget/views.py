from asyncio.windows_events import NULL
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

    # post will only happen when there is no budget 
    # and user creates it with "create default budget" button, 
    # so when user has already its own budget, it will just be displayed
    if request.method != 'POST':
        # Display the budget
        try:
            budget = Budget.objects.filter(owner=request.user).all()[0]
            categories = budget.category_set.all()
            sub_dict = {}
            for category in categories:
                sub_dict[category] = category.subcategory_set.all()
        except:
            budget = NULL
            sub_dict = {}

        context = {'budget': budget, 'sub_dict': sub_dict}
        return render(request, 'budget/budget.html', context)

    else:
        # Only if the 'create default budget' button was clicked
        budget = Budget(name='moj', owner=request.user)
        budget.save()

        # names of defaul categories an subcategories
        categories_names = {
            'Food': [
                'Grocery shopping',
                'Eating outside',
                'Alcohol',
                ], 
            'Culture': [
                'Cinema/Theaters',
                'Gym',
                'Books',
                ],
            'Hygiene': [
                'Cosmetics',
                'Barber',
                ],
            }
        sub_dict = {}

        # creating default objects of categories and subcategories
        for cat, subs in categories_names.items() :
            category = Category(budget=budget, name=cat)
            category.save()

            # list of subcategories objects
            subs_list = []
            
            for sub in subs:
                sub_cat = SubCategory(category=category, name=sub)
                sub_cat.save()
                subs_list.append(sub_cat)

            sub_dict[category] = subs_list

        context = {'budget': budget, 'sub_dict': sub_dict}
        return render(request, 'budget/budget.html', context)
            
