import json
import shutil
import tempfile
from index.views import *
from index.constants import *
from django.urls import reverse
from django.test import override_settings
from unittest import TestCase, main, skip
from django.test import RequestFactory, Client


@skip("Skipping GenericPageViewTest")
class GenericPageViewTest(TestCase):
    def test_get_context_data(self, view_class, page_type):
        request = RequestFactory().get('/fake-path/')
        view = view_class.as_view()
        response = view(request)
        context = response.context_data

        self.assertIn('pageType', context)
        self.assertEqual(context['pageType'], page_type)
        self.assertEqual(response.status_code, 200)


class IndexPageViewTest(TestCase):
    def test_get_context_data(self):
        view_class = IndexPageView
        page_type = "Главная страница"
        GenericPageViewTest().test_get_context_data(view_class, page_type)

        request = RequestFactory().get('/fake-path/')
        view = IndexPageView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)


class DevelopPageViewTest(TestCase):

    def test_get_context_data(self):
        request = RequestFactory().get('/fake-path/')
        view = DevelopPageView.as_view()
        context = view(request, pageType='example').context_data

        self.assertIn('pageType', context)
        self.assertIn('description', context)

        page_type = context['pageType']
        description = context['description']

        self.assertEqual(page_type, "Страница в разработке")
        self.assertEqual(description, DEVELOP_DESCRIPTION.get('example', ''))


class PrivacyPageViewTest(TestCase):

    def test_get_context_data(self):
        view_class = PrivacyPageView
        page_type = "Политика конфиденциальности"
        GenericPageViewTest().test_get_context_data(view_class, page_type)


class CatalogPageViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.page_slug = PageSlug.objects.get(slug="catalogPage")
        self.category = Category.objects.create(title="Тест", title_en="Test", slug="test")
        self.category2 = Category.objects.create(title="Тест2", title_en="Тест2", slug="subtest")
        self.subcategory = Subcategory.objects.create(title_en="ПодТест", title="SubTest", icon="<i></i>",
                                                      category=self.category, slug="subtest", page_slug=self.page_slug)

    def tearDown(self):
        self.subcategory.delete()
        self.category.delete()
        self.category2.delete()

    def test_valid_category(self):
        resp = self.client.get(f'/catalog/{self.category.slug}')
        self.assertEqual(resp.status_code, 200)

    def test_valid_subcategory(self):
        resp = self.client.get(f'/catalog/{self.subcategory.slug}')
        self.assertEqual(resp.status_code, 200)

    def test_invalid_catalog(self):
        resp = self.client.get('/catalog/invalid_test')
        self.assertEqual(resp.status_code, 404)

    @override_settings(LANGUAGE_CODE='ru')
    def test_catalog_page_title_in_russian(self):
        response = self.client.get(reverse('catalogPage', kwargs={'pageType': 'test'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.category.title, response.content.decode())

    @override_settings(LANGUAGE_CODE='en')
    def test_catalog_page_title_in_english(self):
        response = self.client.get(reverse('catalogPage', kwargs={'pageType': 'test'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.category.title_en, response.content.decode())


class ApartHomePageViewTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.temp_image_folder = os.path.join(settings.STATIC_ROOT, 'img', 'apartments', 'Apartment')
        os.makedirs(self.temp_image_folder)

        self.apartment = Apartment.objects.create(title="Apartment", guests=5, square=100, sleepPlace=5, dailyPrice=100)

    def tearDown(self):
        shutil.rmtree(self.temp_image_folder)
        self.apartment.delete()

    def test_valid_apartment(self):
        response = self.client.get(reverse('apartHomePage', kwargs={'title': self.apartment.title}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists(self.temp_image_folder))

    @override_settings(LANGUAGE_CODE='ru')
    def test_home_title_and_share_title_in_russian(self):
        response = self.client.get(reverse('apartHomePage', kwargs={'title': self.apartment.title}))
        self.assertIn(f'ДОМ {self.apartment.title.upper()}', response.content.decode())
        self.assertIn(f'Забронировать дом {self.apartment.title.upper()}', response.content.decode())

    @override_settings(LANGUAGE_CODE='en')
    def test_home_title_and_share_title_in_english(self):
        response = self.client.get(reverse('apartHomePage', kwargs={'title': self.apartment.title}))
        self.assertIn(f'{self.apartment.title.upper()} HOME', response.content.decode())
        self.assertIn(f'Book an {self.apartment.title.upper()} house', response.content.decode())

    def test_invalid_apartment(self):
        response = self.client.get(reverse('apartHomePage', kwargs={'title': "test"}))
        self.assertEqual(response.status_code, 404)


class OrderCallViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        for callback in Callback.objects.filter(name='John'):
            callback.delete()
        for user in User.objects.filter(username="test"):
            user.delete()

    def test_valid_phone_numbers(self):
        view = OrderCallView()
        valid_phone_numbers = ['+375291234567', '375291234567', '+79123456789', '79123456789']

        for phone_number in valid_phone_numbers:
            self.assertTrue(view.is_valid_phone(phone_number))

    def test_invalid_phone_numbers(self):
        view = OrderCallView()
        invalid_phone_numbers = ['123456789', '+123456789', '37529123456', '+791234567890']

        for phone_number in invalid_phone_numbers:
            self.assertIsNone(view.is_valid_phone(phone_number))

    @override_settings(LANGUAGE_CODE="en")
    def test_valid_order_call(self):
        callback = Callback.objects.create(name='John', phone='+375291234567', placeApplication='home')
        response = self.client.post(reverse('orderCallFunc'),
                                    {'name': callback.name, 'phone': callback.phone,
                                     'pageType': 'home'})
        json_response = json.loads(response.content.decode())

        self.assertEqual(json_response['success'], True)
        self.assertEqual(json_response['message'], SUCCESS_MESSAGES['success_callback'])

    @override_settings(LANGUAGE_CODE="en")
    def test_empty_name(self):
        callback = Callback.objects.create(name='John', phone='+375291234567', placeApplication='home')
        response = self.client.post(reverse('orderCallFunc'),
                                    {'name': '', 'phone': callback.phone, 'pageType': 'home'})
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response['success'], False)
        self.assertEqual(json_response['message'], ERROR_MESSAGES['empty_name'])

    @override_settings(LANGUAGE_CODE="en")
    def test_invalid_name(self):
        callback = Callback.objects.create(name='John', phone='+375291234567', placeApplication='home')
        response = self.client.post(reverse('orderCallFunc'),
                                    {'name': '123abc', 'phone': callback.phone, 'pageType': 'home'})
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response['success'], False)
        self.assertEqual(json_response['message'], ERROR_MESSAGES['invalid_name'])

    @override_settings(LANGUAGE_CODE="en")
    def test_invalid_phone(self):
        callback = Callback.objects.create(name='John', phone='+375291234567', placeApplication='home')
        response = self.client.post(reverse('orderCallFunc'),
                                    {'name': callback.name, 'phone': 'abc', 'pageType': 'home'})
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response['success'], False)
        self.assertEqual(json_response['message'], ERROR_MESSAGES['invalid_phone'])


class ContactsPageViewTest(TestCase):

    def test_get_context_data(self):
        view_class = ContactsPageView
        page_type = "Контакты"
        GenericPageViewTest().test_get_context_data(view_class, page_type)


class SaveEmailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.valid_email = 'test@example.com'

    def tearDown(self):
        Mail.objects.filter(address=self.valid_email).delete()

    def test_valid_email(self):
        response = self.client.post(reverse('saveEmailFunc'), {'email': self.valid_email})
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['success'], True)
        self.assertEqual(json_response['message'], SUCCESS_MESSAGES['success_mailing'])
        self.assertTrue(Mail.objects.filter(address=self.valid_email).exists())

    def test_empty_email(self):
        response = self.client.post(reverse('saveEmailFunc'), {'email': ''})
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['success'], False)
        self.assertEqual(json_response['message'], ERROR_MESSAGES['empty_email'])
        self.assertFalse(Mail.objects.filter(address='').exists())

    def test_invalid_email(self):
        invalid_email = 'invalid_email'
        response = self.client.post(reverse('saveEmailFunc'), {'email': invalid_email})
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['success'], False)
        self.assertEqual(json_response['message'], ERROR_MESSAGES['invalid_email'])
        self.assertFalse(Mail.objects.filter(address='').exists())

    def test_existing_email(self):
        Mail.objects.create(address=self.valid_email)
        response = self.client.post(reverse('saveEmailFunc'), {'email': self.valid_email})
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['success'], False)
        self.assertEqual(json_response['message'], ERROR_MESSAGES['exists_email'])
        self.assertEqual(Mail.objects.filter(address=self.valid_email).count(), 1)


class ServicePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.temp_image_folder = os.path.join(settings.STATIC_ROOT, 'img', 'services', 'service')
        os.makedirs(self.temp_image_folder)

        self.service = Services.objects.create(title="Сервис", title_en="Service", slug="service",
                                               description="Это тестовый сервис", description_en="This is test service",
                                               hourlyPrice=999)

    def tearDown(self):
        shutil.rmtree(self.temp_image_folder)
        self.service.delete()

    def test_valid_service(self):
        response = self.client.get(reverse('servicePage', kwargs={'slug': self.service.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists(self.temp_image_folder))

    def test_invalid_service(self):
        response = self.client.get(reverse('servicePage', kwargs={'slug': "Not found"}))
        self.assertEqual(response.status_code, 404)


class GalleryPageViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.temp_image_folder_territory = tempfile.mkdtemp()
        self.temp_image_folder_apartment = tempfile.mkdtemp()
        self.category = Category.objects.create(title="Тестовая категория", title_en="Test category", slug="test_category")

    def tearDown(self):
        shutil.rmtree(self.temp_image_folder_territory)
        shutil.rmtree(self.temp_image_folder_apartment)
        self.category.delete()

    def test_valid_territory_category(self):
        response = self.client.get(reverse('galleryPage', kwargs={'category': 'territory'}))
        self.assertEqual(response.status_code, 200)
        self.assertIn('ТЕРРИТОРИЯ', response.content.decode())

    def test_valid_apartment_category(self):
        response = self.client.get(reverse('galleryPage', kwargs={'category': self.category.slug}))
        self.assertEqual(response.status_code, 200)

    # def test_invalid_category(self):
    #     response = self.client.get(reverse('galleryPage', kwargs={'category': 'non_existing_category'}))
    #     self.assertEqual(response.status_code, 404)

    @override_settings(LANGUAGE_CODE="en")
    def test_language_en(self):
        response_en = self.client.get(reverse('galleryPage', kwargs={'category': self.category.slug}), HTTP_ACCEPT_LANGUAGE='en')
        self.assertEqual(response_en.status_code, 200)
        self.assertIn('TERRITORY', response_en.content.decode())

    @override_settings(LANGUAGE_CODE="ru")
    def test_language_ru(self):
        response_ru = self.client.get(reverse('galleryPage', kwargs={'category': self.category.slug}),
                                      HTTP_ACCEPT_LANGUAGE='ru')
        self.assertEqual(response_ru.status_code, 200)
        self.assertIn('ТЕРРИТОРИЯ', response_ru.content.decode())


if __name__ == '__main__':
    main()
