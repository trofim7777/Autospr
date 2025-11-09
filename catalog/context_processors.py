from .models import Favorite

def favorites_count(request):
    """
    Кол-во авто в избранном для отображения бейджа в шапке.
    Гостям показываем 0 (у нас избранное для залогиненных).
    """
    if not request.user.is_authenticated:
        return {'favorites_count': 0}
    return {
        'favorites_count': Favorite.objects.filter(user=request.user).count()
    }
