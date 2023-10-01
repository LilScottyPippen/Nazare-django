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
    title = models.CharField(unique=True, max_length=100, verbose_name="Название")
    title_en = models.CharField(max_length=100, verbose_name="Название (English)")
    icon = models.CharField(max_length=255, verbose_name="Иконка (Font awesome)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    slug = models.SlugField(unique=True, max_length=100, verbose_name="Псевдоним (English)")
    page_slug = models.ForeignKey(PageSlug, on_delete=models.CASCADE, verbose_name="Псевдоним страницы")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.title

#
# ======== UNDER REVISION ==========
#
# def getImageUploadPath(instance, filename):
#     base_path = f"static/img/apartments/{instance.apartment.title}"
#     extension = os.path.splitext(filename)[1]
#     new_filename = f"{instance.nameImage}{extension}"
#     return os.path.join(base_path, new_filename)
#
# class ApartmentPhoto(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     apartment = models.ForeignKey(Apartment, verbose_name='Аппартамент', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=getImageUploadPath)
#     nameImage = models.CharField(max_length=50)

#     class Meta:
#         verbose_name = "Фото апартамента"
#         verbose_name_plural = "Фото апартаментов"

#     def __str__(self):
#         return self.nameImage

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)

#         photo_path = self.image.path
#         photo_filename = os.path.basename(photo_path)

#         staticfiles_build_path = os.path.join(settings.BASE_DIR, 'staticfiles_build', 'static', 'img', 'apartments', self.apartment.title)
#         if not os.path.exists(staticfiles_build_path):
#             os.makedirs(staticfiles_build_path)

#         staticfiles_build_photo_path = os.path.join(staticfiles_build_path, photo_filename)
#         copyfile(photo_path, staticfiles_build_photo_path)

#     def delete(self, *args, **kwargs):
#         photo_path = self.image.path
#         photo_filename = os.path.basename(photo_path)

#         static_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'apartments', self.apartment.title, photo_filename)
#         staticfiles_build_path = os.path.join(settings.BASE_DIR, 'staticfiles_build', 'static', 'img', 'apartments', self.apartment.title, photo_filename)

#         if os.path.exists(static_path):
#             os.remove(static_path)

#         if os.path.exists(staticfiles_build_path):
#             os.remove(staticfiles_build_path)

#         super().delete(*args, **kwargs)