from django import forms
from .models import MainCategory, SubCategory, Source, Expense, Income, Patience
from .models import UserInfo

class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory  # これはmodels.pyに定義されているモデルです
        fields = ['name']
class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['main_category', 'name']

class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['name']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'amount', 'main_category', 'sub_category', 'payment_method']

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['date', 'amount', 'source']

class PatienceForm(forms.ModelForm):
    class Meta:
        model = Patience
        fields = ['date', 'amount',  'main_category', 'sub_category', 'description']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['mbti', 'occupation', 'income', 'expenses', 'payment', 'savings', 'goal', 'personality', 'awareness']
