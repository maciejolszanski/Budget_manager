import datetime
import calendar

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Budget, Category, SubCategory, Month
from .forms import EditSubCategoryForm, EditCategory, AddSubcategory
from .charts import get_pie_div


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
            print(budget)
            month = budget.month_set.all().get()
            print('miesiac', month)
            categories = month.category_set.all()
            print(categories)
            sub_dict = {}
            for category in categories:
                sub_dict[category] = category.subcategory_set.all()

            graph = None #get_pie_div(budget)
            
        except:
            budget = None
            sub_dict = {}
            graph = None
            month = None

        context = {
            'budget': budget,
            'month': month,
            'sub_dict': sub_dict,
            'graph': graph
            }
        return render(request, 'budget/budget.html', context)

    else:
        # Only if the 'create default budget' button was clicked
        budget, month, sub_dict = create_default_budget(request)

        context = {'budget': budget, 'month': month, 'sub_dict': sub_dict}
        return render(request, 'budget/budget.html', context)

def create_default_budget(request):
    '''create budget with default categories and subcategories'''

    budget = Budget(name='moj', owner=request.user)
    budget.save()

    date = datetime.datetime.today()
    month_int = date.month
    month = calendar.month_name[month_int]
    year_int = date.year

    month = Month(month=month, year=year_int, budget=budget)
    month.save()

    # names of default categories an subcategories
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

        category = Category(month=month, name=cat)
        category.save()

        # list of subcategories objects
        subs_list = []
        
        for sub in subs:
            sub_cat = SubCategory(category=category, name=sub)
            sub_cat.save()
            subs_list.append(sub_cat)

        sub_dict[category] = subs_list

    return budget, month, sub_dict,

@login_required            
def edit_subcategory(request, subcategory_id):
    '''editing data of goals and spendings in category'''

    subcat = SubCategory.objects.get(id=subcategory_id)
    category = subcat.category

    if request.method != 'POST':
        form = EditSubCategoryForm(instance=subcat)
    else:
        form = EditSubCategoryForm(instance=subcat, data=request.POST)
        if form.is_valid():
            form.save()

            return redirect('budget:budget')
    
    context = {'subcat': subcat, 'category': category, 'form': form}
    return render(request, "budget/edit_subcategory.html", context)

@login_required
def edit_category(request, category_id):
    '''editing the name of category'''

    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        form = EditCategory(instance=category)
    
    else:
        form = EditCategory(instance=category, data=request.POST)
        if form.is_valid():
            form.save()

            if 'return' in request.POST:
                return redirect('budget:budget')

            elif 'add' in request.POST:
                return redirect('budget:add_subcategory', category_id=category_id)
    
    context = {'category': category, 'form': form}
    return render(request, 'budget/edit_category.html', context)

@login_required
def add_subcategory(request, category_id):
    '''add subcategory to category'''

    category = Category.objects.get(id=category_id)

    if request.method != 'POST':
        form = AddSubcategory()
    
    else:
        form = AddSubcategory(data=request.POST)
        if form.is_valid():
            new_sub = form.save(commit=False)
            new_sub.category = category
            new_sub.save()

            if 'return' in request.POST:
                return redirect('budget:budget')

            elif 'next' in request.POST:
                return redirect('budget:add_subcategory', category_id=category_id)
    
    context = {'category': category, 'form': form}
    return render(request, 'budget/add_subcategory.html', context)
