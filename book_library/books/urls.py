from django.urls import path

from .views import start_page, get_books_by_country, get_books_by_city, get_books_by_rating, get_shop_report, get_store, \
    get_shop_report_by_published_date

app_name = "books"

urlpatterns = [
    path('', start_page, name='start_page'),
    path('books/by_country/<str:country>', get_books_by_country, name='books_country'),
    path('books/by_city/<str:city>', get_books_by_city, name='books_city'),
    path('books/by_rating/<str:rating>', get_books_by_rating, name='books_rating_gt'),
    path('stores/report', get_shop_report, name='stores_report'),
    path('stores/report/by_published_date/<int:year>', get_shop_report_by_published_date,
         name='stores_report_by_published_date'),
    path('store/<int:pk>', get_store, name='store'),
]
