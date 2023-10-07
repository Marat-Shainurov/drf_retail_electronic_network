from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from sales_network.models import ContactInfo, MainNetwork, Factory
from users.models import CustomUser


class FactoryTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_data = {'email': "test_email@mail.com", "password": 123}
        self.test_user = CustomUser.objects.create(**self.user_data)
        self.client.force_authenticate(self.test_user)

        self.factory_contacts_data = {
            'email': 'london@mail.com', 'phone': '89998336677', 'country': 'UK',
            'city': 'London', 'street': 'Downing Street', 'building': 10
        }
        self.test_factory_contacts = ContactInfo.objects.create(**self.factory_contacts_data)

        self.main_net_contacts_data = {
            'email': 'nyc@mail.com', 'phone': '89998336688', 'country': 'USA',
            'city': 'New York City', 'street': 'Th 3rd Street', 'building': 10
        }
        self.test_main_net_contacts = ContactInfo.objects.create(**self.main_net_contacts_data)

        self.test_main_network = MainNetwork.objects.create(
            name="test network", contact_info=self.test_main_net_contacts)

        self.test_factory_data = {
            "name": "Factory setUp", "contact_info": self.test_factory_contacts, "main_network": self.test_main_network}
        self.test_factory = Factory.objects.create(**self.test_factory_data)

    def test_get_factory(self):
        response_retrieve = self.client.get(f"http://localhost:8000/factories/get/{self.test_factory.pk}/")
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)
        self.assertEqual(response_retrieve.json()['name'], self.test_factory.name)
        self.assertEqual(response_retrieve.json()['id'], self.test_factory.pk)
        self.assertEqual(response_retrieve.json()['main_network']['id'], self.test_main_network.pk)

    def test_create_factory(self):
        product_data = {"name": "test product", "product_model": "test model", "launch_date": "2023-10-07"}
        test_product = Product.objects.create(**product_data)
        new_prod_data = {"name": "new product", "product_model": "new model", "launch_date": "2023-10-07"}

        contacts_data = self.factory_contacts_data.copy()
        contacts_data['email'], contacts_data['phone'] = 'new_email@mail.com', '89998888888'

        factory_data = self.test_factory_data.copy()
        factory_data['name'], factory_data['contact_info'] = 'new factory', contacts_data
        factory_data['product_ids_to_add'], factory_data['main_network'] = [test_product.pk], self.test_main_network.pk
        factory_data['new_products'] = [new_prod_data]

        response_create = self.client.post(
            "http://localhost:8000/factories/create/", data=factory_data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create.json()['main_network'], self.test_main_network.pk)
        self.assertEqual(response_create.json()['name'], factory_data['name'])
        self.assertEqual(response_create.json()['contact_info']['email'], contacts_data['email'])
        new_factory = Factory.objects.get(pk=response_create.json()['id'])
        self.assertEqual(new_factory.products.get(pk=test_product.id), test_product)
        self.assertEqual(
            new_factory.products.get(name=new_prod_data['name']), Product.objects.get(name=new_prod_data['name']))

    def test_get_factories(self):
        response_get = self.client.get("http://localhost:8000/factories/")
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(response_get.json(), list), True)
        self.assertEqual(response_get.json()[0]['id'], self.test_factory.pk)
        self.assertEqual(response_get.json()[0]['main_network']['name'], self.test_main_network.name)

    def test_update_factory(self):
        product_data = {"name": "test product", "product_model": "test model", "launch_date": "2023-10-07"}
        product = Product.objects.create(**product_data)
        data_to_update = {
            "name": "UPDATED", 'is_active': False, 'product_ids_to_add': [product.pk], 'product_ids_to_remove': []}

        self.assertEqual(self.test_factory.products.all().count(), 0)
        response_update = self.client.put(
            f"http://localhost:8000/factories/update/{self.test_factory.pk}/", data=data_to_update)

        updated_factory = Factory.objects.get(pk=self.test_factory.pk)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_factory.name, data_to_update['name'])
        self.assertEqual(updated_factory.is_active, data_to_update['is_active'])
        self.assertEqual(updated_factory.products.all().count(), 1)
        self.assertEqual(updated_factory.products.get(name=product_data['name']), product)

    def test_partial_update(self):
        data_to_update = {"name": "partially UPDATED"}
        response_update = self.client.patch(
            f"http://localhost:8000/factories/update/{self.test_factory.pk}/", data=data_to_update)

        updated_factory = Factory.objects.get(pk=self.test_factory.pk)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_factory.name, data_to_update['name'])

    def test_delete_factory(self):
        stored_factory = Factory.objects.all()
        self.assertEqual(stored_factory.count(), 1)
        self.assertEqual(stored_factory.first(), self.test_factory)

        response_delete = self.client.delete(f"http://localhost:8000/factories/delete/{self.test_factory.pk}/")
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Factory.objects.all().count(), 0)
