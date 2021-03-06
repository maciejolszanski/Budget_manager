from django.urls import path

from . import views


app_name = 'budget'

urlpatterns = [
    # main site
    path('', views.index, name='index'),

    # site with user's budget
    path('budget', views.budget, name='budget'),
    
    # site with user's budget for a particular month
    path('budget/<int:month_id>', views.budget, name='budget'),

    # editing the subcategory
    path(
        'edit_subcategory/<int:subcategory_id>', 
        views.edit_subcategory,
        name='edit_subcategory'
        ),

    # editing category
    path(
        'edit_category/<int:category_id>',
        views.edit_category,
        name='edit_category',
    ),

    # add subcategory to category
    path(
        'add_subcategory/<int:category_id>',
        views.add_subcategory,
        name='add_subcategory'
    ),

    # add category to month
    path('add_category/<int:month_id>',
        views.add_category,
        name='add_category'
    ),

    # add month
    path('add_month', views.add_month, name='add_month'),
]