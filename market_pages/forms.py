from django import forms
from .models.ProductModel import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'type', 'description', 'price', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Categoría'}),
            'type': forms.Select(choices=[('product', 'Producto'), ('service', 'Servicio')], attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
