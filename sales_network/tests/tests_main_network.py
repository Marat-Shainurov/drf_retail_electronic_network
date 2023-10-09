# todo: install and flake8
# todo: add a new fixture


from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from sales_network.models import ContactInfo, MainNetwork, Factory
from users.models import CustomUser


class MainNetworkTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_data = {'email': "test_email@mail.com", "password": 123}
        self.test_user = CustomUser.objects.create(**self.user_data)
        self.client.force_authenticate(self.test_user)

        self.main_net_contacts_data = {
            'email': 'nyc@mail.com', 'phone': '89998336688', 'country': 'USA',
            'city': 'New York City', 'street': 'Th 3rd Street', 'building': 10
        }
        self.test_main_net_contacts = ContactInfo.objects.create(**self.main_net_contacts_data)

        self.test_main_network = MainNetwork.objects.create(
            name="test network", contact_info=self.test_main_net_contacts)

    def test_get_main_network(self):
        response_retrieve = self.client.get(f"http://localhost:8000/main-networks/get/{self.test_main_network.pk}/")
        self.assertEqual(response_retrieve.status_code, status.HTTP_200_OK)
        self.assertEqual(response_retrieve.json()['name'], self.test_main_network.name)
        self.assertEqual(response_retrieve.json()['id'], self.test_main_network.pk)
        self.assertEqual(response_retrieve.json()['products'], [])

    def test_create_main_network(self):
        product_data = {"name": "test product", "product_model": "test model", "launch_date": "2023-10-07"}
        test_product = Product.objects.create(**product_data)
        new_prod_data = {"name": "new product", "product_model": "new model", "launch_date": "2023-10-07"}

        contacts_data = self.main_net_contacts_data.copy()
        contacts_data['email'], contacts_data['phone'] = 'new_email@mail.com', '89998888888'

        main_network = dict()
        main_network['name'], main_network['contact_info'] = 'New Sales Network', contacts_data
        main_network['product_ids_to_add'], main_network['main_network'] = [test_product.pk], self.test_main_network.pk
        main_network['new_products'] = [new_prod_data]

        response_create = self.client.post(
            "http://localhost:8000/main-networks/create/", data=main_network, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_create.json()['name'], main_network['name'])
        self.assertEqual(response_create.json()['contact_info']['email'], contacts_data['email'])
        new_network = MainNetwork.objects.get(pk=response_create.json()['id'])
        self.assertEqual(new_network.products.get(pk=test_product.id), test_product)
        self.assertEqual(
            new_network.products.get(name=new_prod_data['name']), Product.objects.get(name=new_prod_data['name']))

    def test_get_retail_networks(self):
        response_get = self.client.get("http://localhost:8000/main-networks/")
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(response_get.json()['results'], list), True)
        self.assertEqual(response_get.json()['results'][0]['id'], self.test_main_network.pk)
        self.assertEqual(response_get.json()['next'], None)
        self.assertEqual(response_get.json()['previous'], None)
        self.assertEqual(response_get.json()['count'], 1)

    def test_update_main_network(self):
        product_data = {"name": "test product", "product_model": "test model", "launch_date": "2023-10-07"}
        product = Product.objects.create(**product_data)
        data_to_update = {
            "name": "UPDATED", 'is_active': False, 'product_ids_to_add': [product.pk], 'product_ids_to_remove': []}

        self.assertEqual(self.test_main_network.products.all().count(), 0)
        response_update = self.client.put(
            f"http://localhost:8000/main-networks/update/{self.test_main_network.pk}/", data=data_to_update)

        updated_main_network = MainNetwork.objects.get(pk=self.test_main_network.pk)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_main_network.name, data_to_update['name'])
        self.assertEqual(updated_main_network.is_active, data_to_update['is_active'])
        self.assertEqual(updated_main_network.products.all().count(), 1)
        self.assertEqual(updated_main_network.products.get(name=product_data['name']), product)

    def test_partial_update(self):
        data_to_update = {"name": "partially UPDATED"}
        response_update = self.client.patch(
            f"http://localhost:8000/main-networks/update/{self.test_main_network.pk}/", data=data_to_update)

        updated_main_network = MainNetwork.objects.get(pk=self.test_main_network.pk)
        self.assertEqual(response_update.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_main_network.name, data_to_update['name'])

    def test_delete_main_network(self):
        stored_main_network = MainNetwork.objects.get(pk=self.test_main_network.pk)
        self.assertEqual(stored_main_network.is_active, True)

        response_delete = self.client.delete(f"http://localhost:8000/main-networks/delete/{self.test_main_network.pk}/")
        self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)
        deleted_main_network = MainNetwork.objects.get(pk=self.test_main_network.pk)
        self.assertEqual(deleted_main_network.is_active, False)
        self.assertEqual(deleted_main_network.contact_info.is_active, False)
