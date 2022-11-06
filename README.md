# Foodrle
 Food-based Wordle-like web game using Django

## Development
Development is mainly done within app (backend + frontend) and web (static frontend)
When adding new modules to python, use pip to freeze the current state of the packages installed. 
```shell
pip freeze > app/requirements.txt
```

## Installation
Development and deployment is done with Docker. 

docker-compose.yml defines the three different services that are needed for the application:
* app - the core application, writen in Python
  * Django
  * Gunicorn
* web - Web Proxy allowing for requests to be forwarded to either gunicorn or locally hosted files
  * nginx
* db - Database for storing application data
  * PostgreSQL

docker-compose.prod.yml is slightly different, and is used for production deployment. 

To bring up the deployment, simply execute the following:
```shell
docker compose up -d
```
If changes have been made, and the deployment needs to be relaunched, bring down the containers with the following:
```shell
docker compose down
docker compose up -d --no-deps --build
```

## Testing 
Testing is done by entering into the `app` docker image, and executing Django's built in test framework. You can do this with the following command:
```shell
docker exec -it foodrle-app-1 python manage.py test
```
This should execute tests and produce a general coverage report. If you would like to view a more detailed html version, you can find it at `app/cover/index.html`. These files are ignored by git.