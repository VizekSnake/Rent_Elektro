from django.contrib.auth import get_user_model
from django.contrib.sites import requests
from django.test import TestCase
from rentapp.models import PowerTool, RentToolProposition, Profile
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


@pytest.mark.django_db
def test_with_authenticated_client(client, django_user_model):
    username = "testuser"
    password = "polska12"
    user = django_user_model.objects.create_user(username=username, password=password)
    # Use this:
    client.force_login(user)
    # Or this:
    client.login(username=username, password=password)
    response = client.get(f'/profile/')
    assert response.status_code == 200

@pytest.mark.django_db
class ToolAddPageTests(TestCase):
    def setUp(self) -> None:
        self.username = 'testuser12345'
        self.email = 'testuser@email.com'
        self.first_name = 'Jarek'
        self.last_name = 'Kostrzewa'
        self.password = 'password1222'

    def test_addtool_page_url(self):
        response = self.client.get("/profile/add_tool")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, template_name='add_user_tool.html')

    def test_addtool_page_view_name(self):
        response = self.client.get(reverse('add_user_tool'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, template_name='add_user_tool.html')

    def test_addtool_form(self):
        response = self.client.post((reverse('add_user_tool')), data={
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