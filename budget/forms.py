from django import forms
from .models import Month, SubCategory, Category

class EditSubCategoryForm(forms.ModelForm):
    '''Edit goals and spendings of the subcategory'''

    class Meta:
        model = SubCategory
        fields = ['name', 'goal', 'spent']
        labels = {
            'name': 'You can rename this subcategory',
            'goal': 'Your month goal',
            'spent': 'Your current spendings',
            }

class EditCategoryForm(forms.ModelForm):
    '''Edit name of the category'''

    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Rename this category'}

class AddCategoryForm(forms.ModelForm):
    '''Edit name of the category'''

    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Name this category'}

class AddSubcategoryForm(forms.ModelForm):
    '''Add subcategory to category'''

    class Meta:
        model = SubCategory
        fields = ['name', 'goal', 'spent']
        labels = {
            'name': 'Name this subcategory',
            'goal': 'Set your goal',
            'spent': 'Type all your recent spendings in this subcategory'
            }

class AddMonthForm(forms.ModelForm):
    '''Add a month to a budget'''

    class Meta:
        model = Month
        fields = ['month', 'year']
        labels = {'month': 'Choose a month',
                  'year': 'Choose a year'}
