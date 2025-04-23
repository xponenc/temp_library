from django.db.models import Avg, Sum, Count, Q, Prefetch
from django.db.models.functions import Round
from django.shortcuts import render
from . import models
from .models import Book, Store


def start_page(request):
    data = models.Book.objects.all()
    return render(request, 'index.html', context={'data': data})


def get_books_by_country(request, country):
    """Список книг по стране"""
    books = (Book.objects.select_related("author", "publisher")
             .prefetch_related("stores").filter(publisher__country=country)).annotate(
        average_review_rate=Round(Avg("review__rate"), 2),
        available_in_stores=Count("stores", distinct=True)
    )
    context = {
        "book_list": books,
        "title": f"Поиск по стране {country}"
    }
    return render(request=request, template_name="books/book_list.html", context=context)


def get_books_by_city(request, city):
    """Список книг по наличию в магазинах города"""
    stores = Prefetch("stores", queryset=Store.objects.filter(city=city))
    books = (Book.objects.select_related("author", "publisher")
             .prefetch_related(stores).filter(stores__city=city)).annotate(
        average_review_rate=Round(Avg("review__rate"), 2),
        available_in_stores=Count("stores", filter=Q(stores__city=city), distinct=True)
    )

    context = {
        "book_list": books,
        "title": f"Поиск по городу {city}",
    }
    return render(request=request, template_name="books/book_list.html", context=context)


def get_books_by_rating(request, rating):
    """Список книг по рейтингу"""
    try:
        rating = float(rating)
        books = (Book.objects.select_related("author", "publisher")
                 .prefetch_related("stores").annotate(
            average_review_rate=Round(Avg("review__rate"), 2),
            available_in_stores=Count("stores", distinct=True)
        ).filter(average_review_rate__gt=rating)).order_by("-average_review_rate", "title")

        context = {
            "book_list": books,
            "title": f"Поиск по рейтингу выше {rating}",
        }
    except ValueError:
        context = {
            "book_list": None,
            "title": f"Ошибка поиску по рейтингу '{rating}'. Задано некорректное значение '{rating}' "
                     f"Задайте число",
        }
    return render(request=request, template_name="books/book_list.html", context=context)


def get_shop_report(request):
    """Отчет по магазинам"""
    book_set = Prefetch("book_set", queryset=Book.objects.select_related("author").all())
    stores = Store.objects.prefetch_related(book_set).all().annotate(
        books_counter=Count("book", distinct=True)
    )

    context = {
        "store_list": stores,
        "title": f"Отчет по книгам в магазинах",
    }

    return render(request=request, template_name="books/store_list.html", context=context)


def get_shop_report_by_published_date(request, year):
    """Отчет по магазинам"""
    book_set = Prefetch("book_set",
                        queryset=Book.objects
                        .select_related("author", "publisher")
                        .filter(published_date__year__gte=year)
                        )
    stores = (
        Store.objects
        .prefetch_related(book_set)
        .annotate(
            books_counter=Count(
                'book',
                filter=Q(book__published_date__year__gte=year),
                distinct=True
            )
        )
        .filter(books_counter__gt=0)
        .order_by('-books_counter')
    )

    context = {
        "store_list": stores,
        "title": f"Отчет по книгам в магазинах выпущенных не позднее {year} года",
    }

    return render(request=request, template_name="books/store_list.html", context=context)


def get_store(request, pk):
    """Отчет по магазинам"""
    book_set = Prefetch("book_set", queryset=Book.objects.select_related("author", "publisher").all().annotate(
            average_review_rate=Round(Avg("review__rate"), 2)))

    store = Store.objects.prefetch_related(book_set).get(pk=pk)
    books_counter = Store.objects.filter(pk=pk).aggregate(count=Count('book'))['count']
    # books_counter = Book.objects.filter(stores=store).count()
    # books_counter = store.book_set.count()

    context = {
        "store": store,
        "books_counter": books_counter,
        "title": f"Отчет по магазину",
    }

    return render(request=request, template_name="books/store_detail.html", context=context)