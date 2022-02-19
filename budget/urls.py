from django.urls import path

from . import views


app_name = 'budget'

urlpatterns = [
    # main site
    path('', views.index, name='index'),
    # path('budget', views.budget, name='budget'),
    path('budget', views.budget, name='budget'),
]