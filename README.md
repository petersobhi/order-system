# order-system

### Start the project:
1. `docker-compose up` 
2. Database migration: `docker-compose run server python manage.py migrate`

### API Docs:
- Swagger: `localhost:8000/swagger`
- Postman collection: https://www.getpostman.com/collections/caa8fbab6883191ab976

### Run tests:
```
docker-compose run server python manage.py test
```

### Check code coverage:
```
docker-compose run server bash -c "coverage run manage.py test; coverage report"
```
