from django.db import models


class Callback(models.Model):
    name = models.CharField(max_length=20, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    placeApplication = models.CharField(default='', max_length=200, verbose_name='Место подачи заявки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    is_answered = models.BooleanField(default=False, verbose_name='Статус')

    class Meta:
        verbose_name = "Обратный звонок"
        verbose_name_plural = "Обратные звонки"

    def __str__(self):
        return self.phone


class Apartment(models.Model):
    title = models.CharField(unique=True, max_length=20, verbose_name='Название')
    guests = models.IntegerField(verbose_name='Кол-во гостей')
    square = models.FloatField(verbose_name='Площадь')
    sleepPlace = models.IntegerField(verbose_name='Кол-во спальных мест')
    dailyPrice = models.IntegerField(default=0, verbose_name='Суточная стоимость (BYN)')

    class Meta:
        verbose_name = "Апартаменты"
        verbose_name_plural = "Апартаменты"

    def __str__(self):
        return self.title


class Mail(models.Model):
    address = models.EmailField(unique=True, verbose_name="Адрес")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = "Электронная почта"
        verbose_name_plural = "Электронные почты"

    def __str__(self):
        return self.address


class Services(models.Model):
    title = models.CharField(unique=True, max_length=100, verbose_name="Название")
    title_en = models.CharField(default="", max_length=100, verbose_name="Название (English)")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="Псевдоним (English)")
    description = models.TextField(default="", verbose_name="Описание")
    description_en = models.TextField(default="", verbose_name="Описание (English)")
    hourlyPrice = models.IntegerField(default=0, verbose_name="Часовая стоимость (BYN)")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.title


class PageSlug(models.Model):
    title = models.CharField(unique=True, max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="Псевдоним (English)")

    class Meta:
        verbose_name = "Псевдоним страницы"
        verbose_name_plural = "Псевдонимы страниц"

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(unique=True, max_length=100, verbose_name="Название")
    title_en = models.CharField(max_length=100, verbose_name="Название (English)")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="Псевдоним (English)")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Subcategory(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    title_en = models.CharField(max_length=100, verbose_name="Название (English)")
    icon = models.CharField(max_length=255, verbose_name="Иконка (Font awesome)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    slug = models.SlugField(null=False, blank=True, max_length=100, verbose_name="Псевдоним (English)")
    page_slug = models.ForeignKey(PageSlug, on_delete=models.CASCADE, verbose_name="Псевдоним страницы")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.title
