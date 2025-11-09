import django_filters
from django_filters import NumberFilter, ChoiceFilter, ModelChoiceFilter
from .models import Car, Brand, CarModel

class CarFilter(django_filters.FilterSet):
    brand = ModelChoiceFilter(queryset=Brand.objects.all(), label='Марка')
    model = ModelChoiceFilter(queryset=CarModel.objects.none(), label='Модель')
    year_min = NumberFilter(field_name='year', lookup_expr='gte', label='Год от')
    year_max = NumberFilter(field_name='year', lookup_expr='lte', label='Год до')
    price_min = NumberFilter(field_name='price', lookup_expr='gte', label='Цена от')
    price_max = NumberFilter(field_name='price', lookup_expr='lte', label='Цена до')
    engine_type = ChoiceFilter(choices=Car.ENGINE_CHOICES, label='Двигатель')
    transmission = ChoiceFilter(choices=Car.TRANSMISSION_CHOICES, label='Коробка')

    class Meta:
        model = Car
        fields = ('brand', 'model', 'engine_type', 'transmission')

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data=data, queryset=queryset, request=request, prefix=prefix)
        # Подстраиваем список моделей под выбранную марку:
        brand_id = self.data.get('brand') if self.data else None
        if brand_id:
            self.filters['model'].queryset = CarModel.objects.filter(brand_id=brand_id)
        else:
            self.filters['model'].queryset = CarModel.objects.all()
