# Автосправочник (Django 4.2)

Веб-приложение для подбора автомобилей по параметрам, с CRUD-операциями, фильтрацией, сортировкой, сравнением, загрузкой фото и базовой аутентификацией.

## Стек
- Windows 10/11, Python 3.11
- Django 4.2, django-filter
- SQLite, Pillow (работа с изображениями)
- Bootstrap 5 (UI)

## Возможности
- Добавление / редактирование / удаление карточек авто (только для пользователей с правами).
- Фильтры: марка, модель, год (от/до), цена (от/до), тип двигателя, коробка.
- Сортировка по цене и году.
- Сравнение до 4 автомобилей (через сессию).
- Загрузка фото, хранение в `/media/`.
- Регистрация, вход/выход (django auth), скрытие кнопок редактирования для обычных пользователей.
- Админ-панель Django.

## Быстрый старт

```bash
# 1) Клонирование
git clone https://github.com/trofim7777/Autospr.git
cd Autospr

# 2) Виртуальное окружение
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

# 3) Зависимости
pip install -r requirements.txt

# 4) Миграции и (опц.) тестовые данные
python manage.py migrate
python manage.py loaddata seed.json  # опционально

# 5) Суперпользователь (опционально)
python manage.py createsuperuser

# 6) Запуск
python manage.py runserver
