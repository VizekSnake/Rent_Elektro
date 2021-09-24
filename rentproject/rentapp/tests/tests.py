from django.contrib.auth import get_user_model
from django.test import TestCase
from rentapp.models import PowerTool, User
from django.urls import reverse
import pytest


@pytest.mark.django_db
class SignUpPageTests(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser12345'
        self.email = 'testuser@email.com'
        self.first_name = 'Jarek'
        self.last_name = 'Kostrzewa'
        self.password = 'password1222'

    def test_signup_page_url(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='signup.html')

    def test_signup_page_view_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='signup.html')

    def test_signup_form(self):
        response = self.client.post((reverse('signup')), data={
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password1': self.password,
            'password2': self.password
        })
        self.assertEqual(response.status_code, 302)

        users = get_user_model().objects.filter(username=self.username)
        self.assertEqual(users.count(), 1)


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser1',
            'password': 'secret123'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)


@pytest.mark.django_db
def test_addtool(client, django_user_model, brandfx, conditionfx, typefx):
    username = "testuser"
    password = "polska12"
    user = django_user_model.objects.create_user(username=username, password=password)
    client.force_login(user)
    response = client.post('/profile/add_tool',
                           {
                            'brand': 1,
                            'type': typefx,
                            'description': 'Nodesc',
                            'power': 1000,
                            'condition': conditionfx,
                            'deposit': 1000,
                            'price': 1000})
    tool = PowerTool.objects.filter(type=typefx)
    # print(tool.type)
    assert response.status_code == 301

@pytest.mark.django_db
class SearchPageTests(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser12345'
        self.email = 'testuser@email.com'
        self.first_name = 'Jarek'
        self.last_name = 'Kostrzewa'
        self.password = 'password1222'
        self.credentials = {
            'username': self.username,
            'password': self.password}
        User.objects.create_user(**self.credentials)

    def test_search_tool_url(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get("/search/tool")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='search_tool.html')

    def test_search_tool_view_name(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='search_tool.html')

    def test_signup_form(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.post((reverse('search')), data={
            'type': 'CD',
        })
        self.assertEqual(response.status_code, 200)

@pytest.mark.django_db
class SearchPageTests(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser12345'
        self.email = 'testuser@email.com'
        self.first_name = 'Jarek'
        self.last_name = 'Kostrzewa'
        self.password = 'password1222'
        self.credentials = {
            'username': self.username,
            'password': self.password}
        User.objects.create_user(**self.credentials)

    def test_search_tool_url(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get("/search/tool")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='search_tool.html')

    def test_search_tool_view_name(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='search_tool.html')

    def test_signup_form(self):
        self.client.post('/login/', self.credentials, follow=True)
        response = self.client.post((reverse('search')), data={
            'type': 'CD',
        })
        self.assertEqual(response.status_code, 200)