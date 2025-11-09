from django.urls import path
from . import views

urlpatterns = [
    path('', views.CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/add/', views.CarCreateView.as_view(), name='car_add'),
    path('cars/<int:pk>/edit/', views.CarUpdateView.as_view(), name='car_edit'),
    path('cars/<int:pk>/delete/', views.CarDeleteView.as_view(), name='car_delete'),

    path('compare/', views.compare_view, name='compare'),
    path('compare/add/<int:pk>/', views.add_to_compare, name='add_to_compare'),
    path('compare/remove/<int:pk>/', views.remove_from_compare, name='remove_from_compare'),

    path('ajax/models/', views.load_models, name='ajax_load_models'),

    # Избранное
    path('favorites/', views.FavoriteListView.as_view(), name='favorite_list'),
    path('favorites/toggle/<int:pk>/', views.favorite_toggle, name='favorite_toggle'),
    # алиас на тот же вью — чтобы шаблоны, где используется 'fav_toggle', тоже работали
    path('fav/toggle/<int:pk>/', views.favorite_toggle, name='fav_toggle'),
    path('toggle_favorite/<int:pk>/', views.favorite_toggle, name='toggle_favorite'),
]
