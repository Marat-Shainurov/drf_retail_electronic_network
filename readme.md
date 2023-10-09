# Описание проекта drf_retail_electronics
drf_retail_electronics это django-rest-framework проект. \
Данное серверное приложение создано для работы с базой данных по созданию, управлению сетью по продажам электроники.


# Запуск проекта
1. Установить docker, выбрав соответствующую ОС:
   https://docs.docker.com/get-docker/

2. Клонировать в IDE проект https://github.com/Marat-Shainurov/drf_retail_electronics на вашу локальную машину.

3. Запустить процесс создания и запуска образа приложения, с помощью команд:
   - docker-compose build
   - docker-compose up

4. Изучить документацию проекта (swagger или redoc):
   - swagger http://127.0.0.1:8000/docs/
   - redoc http://127.0.0.1:8000/redoc/

5. Открыть в браузере главную страницу проекта http://127.0.0.1:8000/ , и начать работу с эндпоинтами.


# Тестовые данные
При необходимости можно загрузить тестовые данные, с помощью *фикстуры*:
  - docker-compose exec app_sales_networks python manage.py loaddata test_fixture.json
  - После загрузки фикстур в admin интерфейс можно авторизоваться под: 
    {
      "email": "test@mail.com",
      "password": "123"
    }


# Приложения и модели
1. *products*
   - *Product* - модель продукта, производимого/закупаемого сетью и звеньями ее иерархии.

2. *sales_network* - приложение для работы с сущностями сети.
   - *ContactInfo* - модель контакты и адрес. 
   - *MainNetwork* - модель основной сети (вершина иерархии сети).\
     Остальные звенья сети связаны с моделью по ForeignKey.
   - *Factory* - модель завода. 
     'Нулевая' модель, с т.з. закупок (у завода могут закупать товар объекты более низкх по иерархии моделей).\
     Обязательно имеет основную сеть (MainNetwork по FK).\
     Связана с Product (ManyToMany)\
     Связана с ContactInfo (OneToOne)
   - *RetailNetwork* - модель розничная сеть.
     Обязательно имеет основную сеть (MainNetwork по FK).\
     Связана с Product (ManyToMany)\
     Связана с ContactInfo (OneToOne)\
     Может иметь завод-поставщик (связь по FK c Factory)
   - *SoleProprietor* - модель индивидуальный предприниматель.
     Обязательно имеет основную сеть (MainNetwork по FK).\
     Связана с Product (ManyToMany)\
     Связана с ContactInfo (OneToOne)\
     Может иметь поставщика либо завод, либо розничную суть (связь по FK). Валидация на уровне модели (clean()).

3. users.
   - CustomUser - кастомная модель пользователей.
   - Переопределен и кастомизирован также и UersManager класс (./users/manager.py)
   - Переопределен и кастомизировать admin interface. (./users/admin.py)

# Пагинация
- Для всех моделей реализована пагинация с выводом 10 объектов на страницу.
- Максимальное значение - 50 объектов на страницу.

# Фильтрация
- Для всех ListViews/endpoints всех моделей приложения sales_network реализована фильтрация по городу (contact_info__city).
  Пример http://127.0.0.1:8000/main-networks/?contact_info__city=London
- Фильтрация по городу добавлена и в admin interface.


# Тестирование
- Все endpoints проекта покрыты тестами.\
  Тесты описаны в модулях <app_name>/test.py. Total coverage - 91%.
- Проведена проверка синтаксиса и соблюдения PEP с помощью flake8.


# Эндпоинты и документация
- Настроена документация yasg-drf.
- Все endpoints можно изучить по ссылкам: \
  http://localhost:8000/docs/ \
  http://localhost:8000/redoc/

# Безопасность
- Для проекта настроен CORS.
- Все endpoints защищены IsAuthenticated permission на уровне проекта.
- На уровне views приложений отдельно добавлен кастомный IsUserActive permission.



