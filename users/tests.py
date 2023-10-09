from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser


class CustomUserTestCase(APITestCase):

    def setUp(self):
        data_user = {'email': 'test@mail.com', 'password': 123, 'is_staff': True}
        self.test_user = CustomUser.objects.create(**data_user)
        self.client.force_authenticate(user=self.test_user)

    def test_retrieve_user(self):
        response = self.client.get(f'http://localhost:8000/users/{self.test_user.pk}/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json()['id'], self.test_user.pk)
        self.assertEquals(response.json()['email'], self.test_user.email)

    def test_create_user(self):
        user_data = {'email': 'test_two@mail.com', 'password': 'qweasd123qwe'}
        response = self.client.post('http://localhost:8000/users/', data=user_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.json()['email'], user_data['email'])

    def test_create_user_wrong_email(self):
        user_data = {'email': 'wrong.com', 'password': 'qweasd123qwe'}
        response = self.client.post('http://localhost:8000/users/', data=user_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.json()['email'], ['Enter a valid email address.'])

    def test_list_users(self):
        user_data = {'email': 'test_two@mail.com', 'password': 'qweasd123qwe'}
        self.client.post('http://localhost:8000/users/', data=user_data)
        response_get = self.client.get('http://localhost:8000/users/')
        self.assertEquals(response_get.status_code, status.HTTP_200_OK)
        self.assertEquals(CustomUser.objects.all().count(), 2)
        self.assertEquals(response_get.json()['results'][0]['email'], self.test_user.email)
        self.assertEquals(response_get.json()['results'][1]['email'], user_data['email'])

    def test_patch_users(self):
        user_data = {'email': 'updated@mail.com'}
        response = self.client.patch(f'http://localhost:8000/users/{self.test_user.pk}/', data=user_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json()['email'], 'updated@mail.com')

    def test_put_users(self):
        user_data = {'email': 'updated@mail.com', 'password': 'new', 'is_active': False}
        response = self.client.put(f'http://localhost:8000/users/{self.test_user.pk}/', data=user_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json()['email'], 'updated@mail.com')
        self.assertEquals(response.json()['is_active'], False)

    def test_delete_user(self):
        response = self.client.delete(f'http://localhost:8000/users/{self.test_user.pk}/')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(CustomUser.objects.all().count(), 0)
