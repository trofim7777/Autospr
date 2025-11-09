# catalog/views.py
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.generic import FormView

from .models import Car, CarModel
from .forms import CarForm
from .filters import CarFilter


# Список + фильтрация + сортировка + пагинация
class CarListView(FilterView):
    model = Car
    template_name = 'catalog/car_list.html'
    context_object_name = 'cars'
    filterset_class = CarFilter
    paginate_by = 9

    def get_queryset(self):
        qs = super().get_queryset()
        sort = self.request.GET.get('sort')
        if sort in {'price', '-price', 'year', '-year'}:
            qs = qs.order_by(sort)
        else:
            qs = qs.order_by('-created_at')  # по умолчанию — новые выше
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_sort'] = self.request.GET.get('sort', '')
        return ctx


class CarDetailView(DetailView):
    model = Car
    template_name = 'catalog/car_detail.html'
    context_object_name = 'car'


# --- Создание/редактирование/удаление ТОЛЬКО для пользователей с правами ---
class CarCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.add_car'
    model = Car
    form_class = CarForm
    template_name = 'catalog/car_form.html'
    success_url = reverse_lazy('car_list')


class CarUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.change_car'
    model = Car
    form_class = CarForm
    template_name = 'catalog/car_form.html'
    success_url = reverse_lazy('car_list')


class CarDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.delete_car'
    model = Car
    template_name = 'catalog/car_confirm_delete.html'
    success_url = reverse_lazy('car_list')


# --- AJAX: модели по марке ---
def load_models(request):
    brand_id = request.GET.get('brand_id')
    data = list(CarModel.objects.filter(brand_id=brand_id).values('id', 'name')) if brand_id else []
    return JsonResponse(data, safe=False)


# --- Сравнение ---
def _get_compare_ids(request):
    return set(request.session.get('compare_ids', []))

def add_to_compare(request, pk):
    car = get_object_or_404(Car, pk=pk)
    ids = _get_compare_ids(request)
    if len(ids) >= 4 and pk not in ids:
        messages.warning(request, 'Можно сравнивать не более 4 автомобилей.')
    else:
        ids.add(pk)
        request.session['compare_ids'] = list(ids)
        messages.success(request, f'{car} добавлен(а) к сравнению.')
    return redirect(request.META.get('HTTP_REFERER', reverse_lazy('car_list')))

def remove_from_compare(request, pk):
    ids = _get_compare_ids(request)
    ids.discard(pk)
    request.session['compare_ids'] = list(ids)
    return redirect('compare')

def compare_view(request):
    ids = request.session.get('compare_ids', [])
    cars = Car.objects.filter(id__in=ids)
    return render(request, 'catalog/compare.html', {'cars': cars})

class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'  # после регистрации на главную (можешь сменить)

    def form_valid(self, form):
        # создаём пользователя
        user = form.save()
        # сразу логиним
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
