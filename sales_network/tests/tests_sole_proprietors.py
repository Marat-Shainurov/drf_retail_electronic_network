from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from sales_network.models import ContactInfo, MainNetwork, Factory, RetailNetwork, SoleProprietor
from users.models import CustomUser


class SoleProprietorNetTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_data = {'email': "test_email@mail.com", "password": 123}
        self.test_user = CustomUser.objects.create(**self.user_data)
        self.client.force_authenticate(self.test_user)

        self.proprietor_contacts_data = {
            'email': 'london@mail.com', 'phone': '89998336677', 'country': 'UK',
            'city': 'London', 'street': 'Downing Street', 'building': 9
        }
        self.test_sole_proprietor_contacts = ContactInfo.objects.create(**self.proprietor_contacts_data)

        self.retail_contacts_data = {
            'email': 'retail@mail.com', 'phone': '89998336633', 'country': 'UK',
            'city': 'London', 'street': 'Downing Street', 'building': 10
        }
        self.test_retail_contacts = ContactInfo.objects.create(**self.retail_contacts_data)

        self.factory_contacts_data = {
            'email': 'factory@mail.com', 'phone': '89998336699', 'country': 'UK',
            'city': 'London', 'street': 'Downing Street', 'building': 11
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

        self.test_retail_data = {
            "name": "Retail net setUp", "contact_info": self.test_retail_contacts,
            "main_network": self.test_main_network, "factory_supplier": self.test_factory}
        self.test_retail_network = RetailNetwork.objects.create(**self.test_retail_data)

        self.test_sole_proprietor_data = {
            "name": "SP setUp", "contact_info": self.test_sole_proprietor_contacts,
            "main_network": self.test_main_network, "retail_network_supplier": self.test_retail_network
        }
        self.test_sole_proprietor = SoleProprietor.objects.create(**self.test_sole_proprietor_data)

    def test_get_sole_proprietor(self):
        response_retrieve = self.client.get(
            f"http://localhost:8000/sole-proprietors/get/{self.test_sole_proprietor.pk}/")
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)
        self.assertEqual(response_retrieve.json()['name'], self.test_sole_proprietor.name)
        self.assertEqual(response_retrieve.json()['id'], self.test_sole_proprietor.pk)
        self.assertEqual(response_retrieve.json()['main_network']['id'], self.test_main_network.pk)
        self.assertEqual(response_retrieve.json()['retail_network_supplier']['id'], self.test_retail_network.pk)
        self.assertEqual(response_retrieve.json()['factory_supplier'], None)

    def test_create_sole_proprietor(self):
        product_data = {"name": "test product", "product_model": "test model", "launch_date": "2023-10-07"}
        test_product = Product.objects.create(**product_data)
        new_product_data = {"name": "new product", "product_model": "new model", "launch_date": "2023-10-07"}

        contacts_data = self.proprietor_contacts_data.copy()
        contacts_data['email'], contacts_data['phone'] = 'new_email@mail.com', '89998888888'

        sole_proprietor_data = self.test_sole_proprietor_data.copy()
        sole_proprietor_data['name'], sole_proprietor_data['contact_info'] = 'new proprietor', contacts_data
        sole_proprietor_data['product_ids_to_add'], sole_proprietor_data['main_network'] = [
            test_product.pk], self.test_main_network.pk
        sole_proprietor_data['new_products'] = [new_product_data]
        sole_proprietor_data['retail_network_supplier'] = self.test_retail_network.pk

        response_create = self.client.post(
            "http://localhost:8000/sole-proprietors/create/", data=sole_proprietor_data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create.json()['main_network'], self.test_main_network.pk)
        self.assertEqual(response_create.json()['factory_supplier'], None)
        self.assertEqual(response_create.json()['retail_network_supplier'], self.test_retail_network.pk)
        self.assertEqual(response_create.json()['name'], sole_proprietor_data['name'])
        self.assertEqual(response_create.json()['contact_info']['email'], contacts_data['email'])
        new_sole_proprietor = SoleProprietor.objects.get(pk=response_create.json()['id'])
        self.assertEqual(new_sole_proprietor.products.get(pk=test_product.id), test_product)
        self.assertEqual(
            new_sole_proprietor.products.get(name=new_product_data['name']),
            Product.objects.get(name=new_product_data['name']))

    def test_get_sole_proprietors(self):
        response_get = self.client.get("http://localhost:8000/sole-proprietors/")
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(response_get.json(), list), True)
        self.assertEqual(len(response_get.json()), 1)
        self.assertEqual(response_get.json()[0]['id'], self.test_sole_proprietor.pk)
        self.assertEqual(response_get.json()[0]['main_network']['name'], self.test_main_network.name)
        self.assertEqual(response_get.json()[0]['factory_supplier'], None)
        self.assertEqual(response_get.json()[0]['retail_network_supplier']['name'], self.test_retail_network.name)

    def test_update_sole_proprietor(self):
        product_data = {"name": "test product", "product_model": "test model", "launch_date": "2023-10-07"}
        product = Product.objects.create(**product_data)
        data_to_update = {
            "name": "UPDATED", 'is_active': False, 'product_ids_to_add': [product.pk], 'product_ids_to_remove': [],
            "retail_network_supplier": None, "factory_supplier": self.test_factory.pk
        }

        self.assertEqual(self.test_sole_proprietor.products.all().count(), 0)
        response_update = self.client.put(
            f"http://localhost:8000/sole-proprietors/update/{self.test_sole_proprietor.pk}/", data=data_to_update,
            format='json')
        updated_sole_proprietor = SoleProprietor.objects.get(pk=self.test_sole_proprietor.pk)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_sole_proprietor.name, data_to_update['name'])
        self.assertEqual(updated_sole_proprietor.is_active, data_to_update['is_active'])
        self.assertEqual(updated_sole_proprietor.products.all().count(), 1)
        self.assertEqual(updated_sole_proprietor.products.get(name=product_data['name']), product)
        self.assertEqual(updated_sole_proprietor.factory_supplier, self.test_factory)
        self.assertEqual(updated_sole_proprietor.retail_network_supplier, None)

    def test_partial_update_sole_proprietor(self):
        data_to_update = {"name": "partially UPDATED"}
        response_update = self.client.patch(
            f"http://localhost:8000/sole-proprietors/update/{self.test_sole_proprietor.pk}/", data=data_to_update)
        updated_sole_proprietor = SoleProprietor.objects.get(pk=self.test_sole_proprietor.pk)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_sole_proprietor.name, data_to_update['name'])

    def test_delete_sole_proprietor(self):
        stored_sole_proprietor = SoleProprietor.objects.all()
        self.assertEqual(stored_sole_proprietor.count(), 1)
        self.assertEqual(stored_sole_proprietor.first(), self.test_sole_proprietor)

        response_delete = self.client.delete(
            f"http://localhost:8000/sole-proprietors/delete/{self.test_sole_proprietor.pk}/")
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SoleProprietor.objects.all().count(), 0)
