# catalog/views.py
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView, ListView, FormView
)
from django_filters.views import FilterView

from .forms import CarForm
from .filters import CarFilter
from .models import Car, CarModel, Favorite


# ---------- Список + фильтрация + сортировка + пагинация ----------
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
        # Идентификаторы авто в избранном — для подсветки ⭐
        if self.request.user.is_authenticated:
            ids = set(
                Favorite.objects.filter(user=self.request.user)
                .values_list('car_id', flat=True)
            )
        else:
            ids = set()
        ctx['fav_ids'] = ids           # чтобы работали твои текущие шаблоны
        ctx['favorite_ids'] = ids      # и альтернативное имя на будущее
        return ctx


# ---------- Детальная ----------
class CarDetailView(DetailView):
    model = Car
    template_name = 'catalog/car_detail.html'
    context_object_name = 'car'


# ---------- CRUD (по правам) ----------
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


# ---------- AJAX: модели по марке ----------
def load_models(request):
    brand_id = request.GET.get('brand_id')
    data = list(CarModel.objects.filter(brand_id=brand_id)
                .values('id', 'name')) if brand_id else []
    return JsonResponse(data, safe=False)


# ---------- Сравнение ----------
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


# ---------- Регистрация ----------
class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=user.username, password=raw_password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


# ---------- ИЗБРАННОЕ ----------
@login_required
def favorite_toggle(request, pk):
    """
    Добавить/убрать авто в избранное для текущего пользователя.
    Возвращает JSON для AJAX (status, count), а при обычном запросе — редирект.
    """
    car = get_object_or_404(Car, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, car=car)
    if created:
        status = 'added'
        messages.success(request, f'{car} добавлен(а) в избранное.')
    else:
        fav.delete()
        status = 'removed'
        messages.info(request, f'{car} удалён(а) из избранного.')

    # AJAX?
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        count = Favorite.objects.filter(user=request.user).count()
        return JsonResponse({'status': status, 'count': count})

    # обычный переход
    return redirect(request.META.get('HTTP_REFERER', reverse_lazy('car_list')))


class FavoriteListView(LoginRequiredMixin, ListView):
    template_name = 'catalog/favorites.html'
    context_object_name = 'cars'

    def get_queryset(self):
        return (Car.objects
                .filter(favorited_by__user=self.request.user)
                .select_related('brand', 'model'))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ids = set(self.get_queryset().values_list('id', flat=True))
        ctx['fav_ids'] = ids
        ctx['favorite_ids'] = ids
        return ctx
git add -A