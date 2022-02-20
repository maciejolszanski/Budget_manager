from django.urls import path

from . import views


app_name = 'budget'

urlpatterns = [
    # main site
    path('', views.index, name='index'),
    # site with user's budget
    path('budget', views.budget, name='budget'),
    # editing the subcategory
    path(
        'edit_subcategory/<int:subcategory_id>', 
        views.edit_subcategory,
        name='edit_subcategory'
        )
]