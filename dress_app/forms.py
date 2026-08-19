from django import forms
from .models import StudentDressEntry, StandardPrice, STANDARD_CHOICES, MEDIUM_CHOICES, PACKAGE_CHOICES

class StudentDressEntryForm(forms.ModelForm):
    class Meta:
        model = StudentDressEntry
        fields = [
            'name', 'standard', 'medium', 'package_model',
            'has_dress', 'has_extra_dress', 'has_dupatta', 'has_extra_dupatta',
            'total_price'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Student Full Name',
                'required': 'required',
                'autocomplete': 'off',
                'id': 'student_name'
            }),
            'standard': forms.Select(attrs={
                'class': 'form-select',
                'id': 'student_standard'
            }),
            'medium': forms.Select(attrs={
                'class': 'form-select',
                'id': 'student_medium'
            }),
            'package_model': forms.Select(attrs={
                'class': 'form-select',
                'id': 'package_model_select'
            }),
            'has_dress': forms.CheckboxInput(attrs={
                'class': 'form-check-input dress-item-toggle',
                'id': 'toggle_has_dress'
            }),
            'has_extra_dress': forms.CheckboxInput(attrs={
                'class': 'form-check-input dress-item-toggle',
                'id': 'toggle_has_extra_dress'
            }),
            'has_dupatta': forms.CheckboxInput(attrs={
                'class': 'form-check-input dress-item-toggle',
                'id': 'toggle_has_dupatta'
            }),
            'has_extra_dupatta': forms.CheckboxInput(attrs={
                'class': 'form-check-input dress-item-toggle',
                'id': 'toggle_has_extra_dupatta'
            }),
            'total_price': forms.NumberInput(attrs={
                'class': 'form-control price-input',
                'step': '0.01',
                'id': 'calculated_total_price'
            }),
        }



class StandardPriceRowForm(forms.ModelForm):
    class Meta:
        model = StandardPrice
        fields = ['standard', 'dress_price', 'extra_dress_price', 'dupatta_price', 'extra_dupatta_price']
        widgets = {
            'standard': forms.HiddenInput(),
            'dress_price': forms.NumberInput(attrs={'class': 'form-control form-control-sm price-field', 'step': '1', 'min': '0'}),
            'extra_dress_price': forms.NumberInput(attrs={'class': 'form-control form-control-sm price-field', 'step': '1', 'min': '0'}),
            'dupatta_price': forms.NumberInput(attrs={'class': 'form-control form-control-sm price-field', 'step': '1', 'min': '0'}),
            'extra_dupatta_price': forms.NumberInput(attrs={'class': 'form-control form-control-sm price-field', 'step': '1', 'min': '0'}),
        }
