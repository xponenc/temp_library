from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class AuditModel(models.Model):
    """Абстрактная модель для хранения информации о создании и изменении."""

    creator = models.ForeignKey(User, verbose_name="создал/изменил", on_delete=models.PROTECT)
    created_at = models.DateTimeField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="дата редактирования", auto_now=True)
    deleted_at = models.DateTimeField(verbose_name="дата удаления", blank=True, null=True)

    class Meta:
        abstract = True


class Author(AuditModel):
    """Модель Автора"""
    objects = models.Manager()

    name = models.CharField(verbose_name="фио", max_length=100)
    bio = models.TextField(verbose_name="биография")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "автор"
        verbose_name_plural = "авторы"
        ordering = ("name", )


class Book(AuditModel):
    """Модель издателя"""
    objects = models.Manager()

    title = models.CharField(verbose_name="название", max_length=200)
    author = models.ForeignKey('Author',  verbose_name="автор", on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField(verbose_name="дата издания")
    description = models.TextField(verbose_name="описание")

    publisher = models.ForeignKey('Publisher', verbose_name='издательство', on_delete=models.PROTECT)
    stores = models.ManyToManyField('Store', verbose_name="магазины")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "книга"
        verbose_name_plural = "книги"
        ordering = ("title", )


class Review(AuditModel):
    """Модель Отзыв"""
    rate = models.SmallIntegerField(verbose_name="оценка", validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.CharField(verbose_name="комментарий", max_length=1000)

    book = models.ForeignKey('Book', verbose_name="отзыв", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"
        ordering = ("book__title", "rate")

    def __str__(self):
        return f"{self.book.title} - {self.rate}"


class Publisher(AuditModel):
    """Модель Издательства"""
    objects = models.Manager()

    name = models.CharField(verbose_name="название", max_length=100)
    country = models.CharField(verbose_name="страна", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "издательство"
        verbose_name_plural = "издательства"
        ordering = ("name", "country")


class Store(models.Model):
    """Модель Магазина"""
    objects = models.Manager()

    name = models.CharField(verbose_name="название", max_length=100)
    city = models.CharField(verbose_name="город", max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:store', args=[str(self.id)])

    class Meta:
        verbose_name = "магазин"
        verbose_name_plural = "магазины"
        ordering = ("name", "city")
