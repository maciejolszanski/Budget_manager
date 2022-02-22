from django import forms
from .models import SubCategory, Category

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

class EditCategory(forms.ModelForm):
    '''Edit name of the category'''

    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Rename this category'}
    