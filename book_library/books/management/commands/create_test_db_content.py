import random

from django.apps import apps
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
fake = Faker()


class Command(BaseCommand):
    help = "Создаёт тестовые данные: магазины, издательства, авторы, книги и отзывы к ним"

    def handle(self, *args, **kwargs):
        Author = apps.get_model('books', 'Author')
        Book = apps.get_model('books', 'Book')
        Publisher = apps.get_model('books', 'Publisher')
        Store = apps.get_model('books', 'Store')
        Review = apps.get_model('books', 'Review')

        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("Не найден ни один пользователь. Создайте хотя бы одного."))
            return

        self.stdout.write("Создание магазинов...")
        stores = [Store.objects.create(name=fake.company(), city=fake.city()) for _ in range(10)]
        self.stdout.write(self.style.SUCCESS(f"Создано {len(stores)} магазинов."))

        self.stdout.write("Создание издательств...")
        publishers = [
            Publisher.objects.create(
                name=fake.company(),
                country=fake.country(),
                creator=user
            ) for _ in range(5)
        ]
        self.stdout.write(self.style.SUCCESS(f"Создано {len(publishers)} издательств."))

        self.stdout.write("Создание авторов...")
        authors = [
            Author.objects.create(
                name=fake.name(),
                bio=fake.text(),
                creator=user
            ) for _ in range(20)
        ]
        self.stdout.write(self.style.SUCCESS(f"Создано {len(authors)} авторов."))

        self.stdout.write("Создание книг...")
        books = []
        for i in range(1000):
            book = Book.objects.create(
                title=fake.sentence(nb_words=5),
                author=random.choice(authors),
                published_date=fake.date_between(start_date='-10y', end_date='today'),
                description=fake.text(max_nb_chars=1000),
                publisher=random.choice(publishers),
                creator=user
            )
            book.stores.set(random.sample(stores, k=random.randint(1, 3)))
            books.append(book)
            if (i + 1) % 100 == 0:
                self.stdout.write(f"  → Создано книг: {i + 1}/1000")
        self.stdout.write(self.style.SUCCESS("Все книги успешно созданы."))

        self.stdout.write("Генерация отзывов к книгам...")
        total_reviews = 0
        for i, book in enumerate(books, start=1):
            review_count = random.randint(50, 100)
            reviews = [
                Review(
                    rate=random.randint(0, 10),
                    comment=fake.text(max_nb_chars=300),
                    book=book,
                    creator=user
                ) for _ in range(review_count)
            ]
            Review.objects.bulk_create(reviews)
            total_reviews += review_count
            if i % 100 == 0:
                self.stdout.write(f"  → Обработано книг: {i}/1000")
        self.stdout.write(self.style.SUCCESS(f"Создано ~{total_reviews} отзывов."))

        self.stdout.write(self.style.SUCCESS("Генерация тестовых данных завершена."))
