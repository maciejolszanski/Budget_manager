import datetime
import calendar

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Budget, Category, SubCategory, Month
from .forms import *
from .charts import get_pie_div

# names of default categories an subcategories
CATEGORIES_NAMES = {
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


def index(request):
    return render(request, 'budget/index.html')

@login_required
def budget(request, month_id=None):
    '''Main user site'''

    # post will only happen when there is no budget 
    # and user creates it with "create default budget" button, 
    # so when user has already its own budget, it will just be displayed
    if request.method != 'POST':
        return display_budget(request, month_id)

    else:
        if 'create' in request.POST:
            # Only if the 'create default budget' button was clicked
            budget, month, months, sub_dict = create_default_budget(request)

            context = {'budget': budget, 'month': month, 'months': months,
                       'sub_dict': sub_dict}
            return render(request, 'budget/budget.html', context)

def display_budget(request, month_id):
    '''displays the budget'''

    try:
        budget = Budget.objects.filter(owner=request.user)[0]
        months = Month.objects.filter(budget=budget).order_by('year', 'month')
        if month_id:
            month = months.get(id=month_id)
        else:
            month = months.last()

        categories = month.category_set.all()
        sub_dict = {}
        for category in categories:
            sub_dict[category] = category.subcategory_set.all()
        graph = get_pie_div(month)
    except:
        # this None values are used when there is no budget created for the user
        budget = None
        sub_dict = {}
        graph = None
        month = None
        months = None

    context = {
        'budget': budget,
        'month': month,
        'months': months,
        'sub_dict': sub_dict,
        'graph': graph
        }
    return render(request, 'budget/budget.html', context)

def create_default_budget(request):
    '''create budget with default categories and subcategories'''

    budget = Budget(name=str(request.user)+' budget', owner=request.user)
    budget.save()

    date = datetime.datetime.today()
    month_int = date.month
    month = calendar.month_name[month_int]
    year_int = date.year

    month = Month(month=month, year=year_int, budget=budget)
    month.save()

    months = Month.objects.all()

    sub_dict = create_default_categories(month)

    return budget, month, months, sub_dict

def create_default_categories(month):
    '''create a dictionary of categories and subcategories'''
    sub_dict = {}

    # creating default objects of categories and subcategories
    for cat, subs in CATEGORIES_NAMES.items() :

        category = Category(month=month, name=cat)
        category.save()

        # list of subcategories objects
        subs_list = []
        
        for sub in subs:
            sub_cat = SubCategory(category=category, name=sub)
            sub_cat.save()
            subs_list.append(sub_cat)

        sub_dict[category] = subs_list
    
    return sub_dict

@login_required            
def edit_subcategory(request, subcategory_id):
    '''editing data of goals and spendings in category'''

    subcat = SubCategory.objects.get(id=subcategory_id)
    category = subcat.category
    month = category.month

    if request.method != 'POST':
        form = EditSubCategoryForm(instance=subcat)
    else:
        form = EditSubCategoryForm(instance=subcat, data=request.POST)
        if form.is_valid():
            form.save()

            return redirect('budget:budget', month_id=month.id)
    
    context = {'subcat': subcat, 'category': category, 'form': form}
    return render(request, "budget/edit_subcategory.html", context)

@login_required
def edit_category(request, category_id):
    '''editing the name of category'''

    category = Category.objects.get(id=category_id)
    month = category.month

    if request.method != 'POST':
        form = EditCategoryForm(instance=category)
    
    else:
        form = EditCategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save()

            if 'return' in request.POST:
                return redirect('budget:budget', month_id=month.id)

            elif 'add' in request.POST:
                return redirect('budget:add_subcategory', 
                                category_id=category_id)
    
    context = {'category': category, 'form': form}
    return render(request, 'budget/edit_category.html', context)

@login_required
def add_subcategory(request, category_id):
    '''add subcategory to category'''

    category = Category.objects.get(id=category_id)
    month = category.month

    if request.method != 'POST':
        form = AddSubcategoryForm()
    
    else:
        form = AddSubcategoryForm(data=request.POST)
        if form.is_valid():
            new_sub = form.save(commit=False)
            new_sub.category = category
            new_sub.save()

            if 'return' in request.POST:
                return redirect('budget:budget', month_id=month.id)

            elif 'next' in request.POST:
                return redirect('budget:add_subcategory',
                                category_id=category_id)
    
    context = {'category': category, 'form': form}
    return render(request, 'budget/add_subcategory.html', context)

@login_required
def add_category(request, month_id):
    '''add category to budget'''

    month = Month.objects.get(id=month_id)

    if request.method != 'POST':
        form = AddCategoryForm()
    
    else:
        form = AddCategoryForm(data=request.POST)
        if form.is_valid():
            new_cat = form.save(commit=False)
            new_cat.month = month
            new_cat.save()
        
            if 'return' in request.POST:
                return redirect('budget:budget', month_id=month_id)

            elif 'next' in request.POST:
                return redirect('budget:add_category', month_id=month_id)
    
    context = {'month': month, 'form': form}
    return render(request, 'budget/add_category.html', context)

@login_required
def add_month(request):
    '''add a new month to a budget'''

    budget = Budget.objects.filter(owner=request.user)[0]

    if request.method != 'POST':
        form = AddMonthForm()
    else:
        form = AddMonthForm(data=request.POST)
        if form.is_valid():
            new_month = form.save(commit=False)
            new_month.budget = budget
            new_month.save()
   
            if 'default' in request.POST:
                create_default_categories(new_month)

            return redirect('budget:budget', month_id=new_month.id)

    context = {'budget': budget, 'form': form}
    return render(request, 'budget/add_month.html', context)
