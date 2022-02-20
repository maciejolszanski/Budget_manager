from django import forms
from .models import SubCategory

class EditSubCategoryForm(forms.ModelForm):
    '''Edit goals and spendings of the subcategory'''

    class Meta:
        model = SubCategory
        fields = ['goal', 'spent']
        labels = {
            'goal': 'Your month goal',
            'spent': 'Your current spendings',
            }
