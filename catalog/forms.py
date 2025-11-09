from django import forms
from .models import Car, CarModel

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('brand', 'model', 'year', 'engine_type', 'transmission', 'price', 'image', 'description')
        widgets = {
            'year': forms.NumberInput(attrs={'min': 1950, 'max': 2100, 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Базовые классы Bootstrap
        for name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.FileInput)):
                field.widget.attrs.setdefault('class', 'form-select' if name in ('brand', 'model', 'engine_type', 'transmission') else 'form-control')

        # Динамический queryset для 'model'
        self.fields['model'].queryset = CarModel.objects.none()
        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model'].queryset = CarModel.objects.filter(brand_id=brand_id)
            except (TypeError, ValueError):
                pass
        elif self.instance.pk:
            self.fields['model'].queryset = CarModel.objects.filter(brand=self.instance.brand)
