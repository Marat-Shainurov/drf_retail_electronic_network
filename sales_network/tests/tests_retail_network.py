from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from sales_network.models import ContactInfo, MainNetwork, Factory, RetailNetwork
from users.models import CustomUser


class RetailNetTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_data = {'email': "test_email@mail.com", "password": 123}
        self.test_user = CustomUser.objects.create(**self.user_data)
        self.client.force_authenticate(self.test_user)

        self.retail_contacts_data = {
            'email': 'london@mail.com', 'phone': '89998336677', 'country': 'UK',
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

    def test_get_retail_network(self):
        response_retrieve = self.client.get(f"http://localhost:8000/retail-networks/get/{self.test_retail_network.pk}/")
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)
        self.assertEqual(response_retrieve.json()['name'], self.test_retail_network.name)
        self.assertEqual(response_retrieve.json()['id'], self.test_retail_network.pk)
        self.assertEqual(response_retrieve.json()['main_network']['id'], self.test_main_network.pk)
        self.assertEqual(response_retrieve.json()['factory_supplier']['id'], self.test_factory.pk)

    def test_create_retail(self):
        product_data = {"name": "test product", "product_model": "test model", "launch_date": "2023-10-07"}
        test_product = Product.objects.create(**product_data)
        new_product_data = {"name": "new product", "product_model": "new model", "launch_date": "2023-10-07"}

        contacts_data = self.retail_contacts_data.copy()
        contacts_data['email'], contacts_data['phone'] = 'new_email@mail.com', '89998888888'

        retail_network_data = self.test_retail_data.copy()
        retail_network_data['name'], retail_network_data['contact_info'] = 'new network', contacts_data
        retail_network_data['product_ids_to_add'], retail_network_data['main_network'] = [
            test_product.pk], self.test_main_network.pk
        retail_network_data['new_products'] = [new_product_data]
        retail_network_data['factory_supplier'] = self.test_factory.pk

        response_create = self.client.post(
            "http://localhost:8000/retail-networks/create/", data=retail_network_data, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create.json()['main_network'], self.test_main_network.pk)
        self.assertEqual(response_create.json()['factory_supplier'], self.test_factory.pk)
        self.assertEqual(response_create.json()['name'], retail_network_data['name'])
        self.assertEqual(response_create.json()['contact_info']['email'], contacts_data['email'])
        new_retail_network = RetailNetwork.objects.get(pk=response_create.json()['id'])
        self.assertEqual(new_retail_network.products.get(pk=test_product.id), test_product)
        self.assertEqual(
            new_retail_network.products.get(name=new_product_data['name']),
            Product.objects.get(name=new_product_data['name']))

    def test_get_retail_networks(self):
        response_get = self.client.get("http://localhost:8000/retail-networks/")
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(response_get.json()['results'], list), True)
        self.assertEqual(len(response_get.json()['results']), 1)
        self.assertEqual(response_get.json()['results'][0]['id'], self.test_retail_network.pk)
        self.assertEqual(response_get.json()['results'][0]['main_network']['name'], self.test_main_network.name)
        self.assertEqual(response_get.json()['results'][0]['factory_supplier']['name'], self.test_factory.name)
        self.assertEqual(response_get.json()['next'], None)
        self.assertEqual(response_get.json()['previous'], None)
        self.assertEqual(response_get.json()['count'], 1)

    def test_update_retail_network(self):
        product_data = {"name": "test product", "product_model": "test model", "launch_date": "2023-10-07"}
        product = Product.objects.create(**product_data)
        data_to_update = {
            "name": "UPDATED", 'is_active': False, 'product_ids_to_add': [product.pk], 'product_ids_to_remove': [],
            "factory_supplier": self.test_factory.pk
        }

        self.assertEqual(self.test_retail_network.products.all().count(), 0)
        response_update = self.client.put(
            f"http://localhost:8000/retail-networks/update/{self.test_retail_network.pk}/", data=data_to_update)

        updated_retail_network = RetailNetwork.objects.get(pk=self.test_retail_network.pk)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_retail_network.name, data_to_update['name'])
        self.assertEqual(updated_retail_network.is_active, data_to_update['is_active'])
        self.assertEqual(updated_retail_network.products.all().count(), 1)
        self.assertEqual(updated_retail_network.products.get(name=product_data['name']), product)
        self.assertEqual(updated_retail_network.factory_supplier, self.test_factory)

    def test_partial_update_retail_net(self):
        data_to_update = {"name": "partially UPDATED"}
        response_update = self.client.patch(
            f"http://localhost:8000/retail-networks/update/{self.test_retail_network.pk}/", data=data_to_update)

        updated_retail_network = RetailNetwork.objects.get(pk=self.test_retail_network.pk)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_retail_network.name, data_to_update['name'])

    def test_delete_retail_network(self):
        stored_retail_net = RetailNetwork.objects.get(pk=self.test_retail_network.pk)
        self.assertEqual(stored_retail_net.is_active, True)

        response_delete = self.client.delete(
            f"http://localhost:8000/retail-networks/delete/{self.test_retail_network.pk}/")
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        deleted_retail_net = RetailNetwork.objects.get(pk=self.test_retail_network.pk)
        self.assertEqual(deleted_retail_net.is_active, False)
        self.assertEqual(deleted_retail_net.contact_info.is_active, False)
