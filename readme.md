# General description
drf_retail_electronics is a django-rest-framework project. \
The project is created for work with a database for creating and managing electronics sales networks.

# Install and usage
1. Clone the project from https://github.com/Marat-Shainurov/drf_retail_electronics to your local machine.

2. Build a new image and run the project container from the root project directory:
   - docker-compose build
   - docker-compose up

3. Read the project's documentation (swagger or redoc format):
   - http://127.0.0.1:8000/docs/
   - http://127.0.0.1:8000/redoc/

4. Go to the main page on your browser http://127.0.0.1:8000/docs and start working with the app's endpoints.


# Testing fixture
You can load the fixture with several testing objects:
  - docker-compose exec app_sales_networks python manage.py loaddata test_fixture.json
  - Credentials: 
    {
      "email": "test@mail.com",
      "password": "123"
    }

# Project structure and models
1. *products* - products app.
   - *Product* - product model, being produced/ordered by the project's entities.

2. *sales_network* - sales networks app.
   - *ContactInfo* - contacts model (contact info, address). 
   - *MainNetwork* - main network model (top of the network hierarchy).\
     The rest of the network's models are related to the main networks via ForeignKey.
   - *Factory* - factory model. 
     'Zero' model, in terms of supply chain and orders.\
     Has its MainNetwork (FK relation).\
     Related to Product (ManyToMany relation)\
     Connected with the ContactInfo model (OneToOne relation)
   - *RetailNetwork* - модель розничная сеть.
     Has its MainNetwork (FK relation).\
     Related to Product (ManyToMany relation)\
     Connected with the ContactInfo model (OneToOne relation)
     May have a factory as a factory-supplier (related to Factory via FK)
   - *SoleProprietor* - sole proprietor model.
    Has its MainNetwork (FK relation).\
     Related to Product (ManyToMany relation)\
     Connected with the ContactInfo model (OneToOne relation)
     May have either a factory-supplier or a retail-network-supplier. Validated on the model level (clean method)

3. users.
   - CustomUser.
   - UersManager class is overridden and customised (./users/manager.py)
   - Admin interface is overridden and customised. (./users/admin.py)

# Testing
-All the endpoints are covered by pytest tests in /tests/test_main.py \
- Run tests:\
  docker-compose exec app_sales_networks python manage.py test

