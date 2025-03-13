from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.registration_url = reverse('users:registration')
        self.valid_user_data = {
            'email': 'test@mirea.ru',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }

    def test_registration_page_loads(self):
        """Тест 1: Проверка загрузки страницы регистрации"""
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)

    def test_successful_registration(self):
        """Тест 2: Проверка успешной регистрации пользователя"""
        response = self.client.post(self.registration_url, self.valid_user_data)
        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse('xaki'))

    def test_registration_with_invalid_email(self):
        """Тест 3: Проверка регистрации с неверным форматом email"""
        invalid_data = self.valid_user_data.copy()
        invalid_data['email'] = 'invalid_email'
        response = self.client.post(self.registration_url, invalid_data)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_registration_with_existing_email(self):
        """Тест 4: Проверка регистрации с уже существующим email"""
        User.objects.create_user(username='existing@mirea.ru', email='existing@mirea.ru', password='testpass123')
        data = self.valid_user_data.copy()
        data['email'] = 'existing@mirea.ru'
        response = self.client.post(self.registration_url, data)
        self.assertContains(response, 'Пользователь с такой почтой уже существует')

class UserLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.user = User.objects.create_user(
            username='test@mirea.ru',
            email='test@mirea.ru',
            password='testpass123'
        )

    def test_login_page_loads(self):
        """Тест 5: Проверка загрузки страницы входа"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        """Тест 6: Проверка успешного входа"""
        response = self.client.post(self.login_url, {
            'username': 'test@mirea.ru',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('xaki'))

    def test_login_with_wrong_password(self):
        """Тест 7: Проверка входа с неверным паролем"""
        response = self.client.post(self.login_url, {
            'username': 'test@mirea.ru',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)

class UserProfileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test@mirea.ru',
            email='test@mirea.ru',
            password='testpass123'
        )
        self.client.login(username='test@mirea.ru', password='testpass123')
        self.profile_url = reverse('users:profile')
        self.edit_profile_url = reverse('users:editprofile')

    def test_profile_page_loads(self):
        """Тест 8: Проверка загрузки страницы профиля"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_profile_page_requires_login(self):
        """Тест 9: Проверка доступа к профилю без авторизации"""
        self.client.logout()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_page_loads(self):
        """Тест 10: Проверка загрузки страницы редактирования профиля"""
        response = self.client.get(self.edit_profile_url)
        self.assertEqual(response.status_code, 200)

   

    def test_user_str_method(self):
        """Тест 13: Проверка строкового представления пользователя"""
        self.assertEqual(str(self.user.email), 'test@mirea.ru')

    def test_get_full_name(self):
        """Тест 14: Проверка метода получения полного имени"""
        self.user.first_name = 'Иван'
        self.user.last_name = 'Иванов'
        self.user.save()
        self.assertEqual(self.user.get_full_name(), 'Иван Иванов')

    def test_set_full_name(self):
        """Тест 15: Проверка метода установки полного имени"""
        self.user.set_full_name('Петр Петров')
        self.assertEqual(self.user.first_name, 'Петр')
        self.assertEqual(self.user.last_name, 'Петров')

    def test_email_unique(self):
        """Тест 16: Проверка уникальности email"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='test2@mirea.ru',
                email='test@mirea.ru',
                password='testpass123'
            )

    def test_optional_fields(self):
        """Тест 17: Проверка необязательных полей"""
        user = User.objects.create_user(
            username='test2@mirea.ru',
            email='test2@mirea.ru',
            password='testpass123'
        )
        self.assertIsNone(user.date_of_birth)
        self.assertEqual(user.phone_number, '')
        self.assertEqual(user.technology_stack, '')

    def test_course_choices(self):
        """Тест 18: Проверка выбора курса"""
        self.user.course = 2
        self.user.save()
        self.assertEqual(self.user.get_course_display(), '2 курс')

    def test_gender_choices(self):
        """Тест 19: Проверка выбора пола"""
        self.user.gender = 'M'
        self.user.save()
        self.assertEqual(self.user.get_gender_display(), 'Мужской')

    def test_profile_photo_upload(self):
        """Тест 20: Проверка загрузки фото в правильную директорию"""
        photo = SimpleUploadedFile("test_photo.jpg", b"file_content", content_type="image/jpeg")
        self.user.profile_photo = photo
        self.user.save()
        self.assertTrue(self.user.profile_photo.name.startswith('users_images/'))
