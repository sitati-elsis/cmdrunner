# CMDRunner
Welcome to CMDRunner, your web based SSH platform. 

This is an API which can run SSH commands on remote machines.


# Environment Variables
- DJANGO_SETTINGS_MODULE (defaults to `cmdrunner.settings.prod_settings`)

The rest of these environment variables will be required if  `DJANGO_SETTINGS_MODULE` has been set to `cmdrunner.settings.prod_settings`
-  SECRET_KEY 
-  DATABASE_URL
-  POSTGRES_USER
-  POSTGRES_PASSWORD
-  POSTGRES_DB


# Setup Development Environment
## Prerequisite Services
Running a development server as described below will require the following services to be installed on your bare-metal machine.
  * rabbitmq
    - Download and install [instructions can be found here](https://www.rabbitmq.com/download.html).
    - The service should run on port `5672`.
  * sqlite3
    - Ensure that the `DJANGO_SETTINGS_MODULE` environment variable has been set to `cmdrunner.settings.dev_settings`.
    - Usually installed by default. This can be confirmed via the following command.
      ```bash
      sqlite3 --version

      3.31.1 2020-01-27 19:55:54 3bfa9cc97da10598521b342961df8f5f68c7388fa117345eeb516eaa837balt1
      ```
    - If it's not installed, download and install [instructions can be found here](https://www.sqlite.org/download.html).

## Running the Development Environment
1. Clone the repo:

    ```bash
    git clone git@github.com:sitati-elsis/cmdrunner.git
    ```

2. `cd` into the repo you have just cloned.

    ```bash
    cd cmdrunner/
    ```
3. Set the environment variables as described above.
3. Install pipenv
4. Create a pipenv virtual environment through the following command.
    ```bash
    pipenv shell
    ```
5. Install project dependencies.
    ```bash
    pipenv install
    ```
6. Start the development server.
    ```bash
    python manage.py runserver
    ```
    This runs on http://localhost:8000/ by default.
7. Create a user via an API client e.g. Postman or curl

    ```bash
    curl -X POST http://localhost:8000/api/signup/ -H "Content-Type: application/json" -d '{"username":"stevo", "password":"stevo123"}'
    ```
8. Create and/or retrieve your access token through the following route.

    ```bash
    curl -X POST http://localhost:8000/api/login/ -H "Content-Type: application/json" -d '{"username":"stevo", "password":"stevo123"}'
    ```
9. With the access token, subsequent authenticated requests can be made to the rest of this API's endpoints. The access token must be passed to the `Authorization` header with the `Token <token>` string format e.g.

    ```bash
    curl -X GET http://localhost:8000/api/machine/ -H "Content-Type: application/json" -H "Authorization: Token 49072f4a93b5fe9bed37551f951e9aba2a786397"
    ```

# Setup Development Environment Using docker-compose
`docker-compose` comes in handy when you don't want to clutter your bare-metal machine with additional services. Those services can instead be made available through docker containers.

## Prerequisites
* docker
  - This is the software platform that runs and manages containers.
  - Download and install [instructions can be found here](https://docs.docker.com/engine/install/).
* docker-compose
  - This is a tool that runs on docker.
  - It is used for defining and running a multi-container Docker application.
  - Download and install [instructions can be found here](https://docs.docker.com/compose/install/)

## Running the docker-compose Development Environment
Use the following command to run the app.
```bash
docker-compose up
```

To stop the app, use Ctrl + C on the terminal.
```bash
^CGracefully stopping... (press Ctrl+C again to force)
```

To stop the app and remove containers created by `docker-compose up`, run the following.
```bash
docker-compose down
```

`docker-compose` can also be used to build a new api image after new changes have been made to the code.
```bash
docker-compose build
```
# Running on Kubernetes
## Prerequisites
  * minikube
    - minikube is a local Kubernetes cluster, focusing on making it easy to learn and develop for Kubernetes.
    - This will allow us to run the app and secure sensitive data like database passwords and secret keys.
    - Download and install [instructions can be found here](https://minikube.sigs.k8s.io/docs/start/).
  * kubectl
    - This is a command line tool that allows you to run commands against a Kubernetes cluster.
    - Download and install [instructions can be found here](https://kubernetes.io/docs/tasks/tools/).
  * gettext
    - This is a linux based utility that provides the `envsubst` command.
    - This command allows us to pass in sensitive data to kubernetes without hardcoding this data in code.
    - A simple `envsubst` example.

## Starting the app

1. Run `minikube start`.
2. Deploy the secrets.
    * This step requires that the `SECRET_KEY`, `DATABASE_URL`, `POSTGRES_PASSWORD`, `POSTGRES_USER` and `POSTGRES_DB` be defined as base64 environment variables.
    * Encoding an environment variable to base64 can be done as follows.
        ```bash
        EXPORT SECRET_KEY=$(echo -n "strong secret key"|base64)
        ```
    * Once all the required environment variables are encoded, the following command can be executed.
        ```bash
        cat k8s/env-secret.yml | envsubst | kubectl apply -f -
        ```
3. Deploy the configuration map.
    * This step requires that the `DJANGO_SETTINGS_MODULE` environment variable is defined.
    * base64 encoding will not be required here since config maps are not meant to store sensitive data.
    * To deploy the config map to Kubernetes, run the following.
        ```bash
        kubectl apply -f k8s/env-configmap.yml
        ```
4. Deploy the Kubernetes Deployment objects.
    ```bash
    kubectl apply -f k8s/nginx-deployment.yml
    kubectl apply -f k8s/postgresql-deployment.yml
    kubectl apply -f k8s/rabbitmq-deployment.yml
    kubectl apply -f k8s/api-deployment.yml
    ```
5. Deploy the Kubernetes Service objects.
    ```bash
    kubectl apply -f k8s/nginx-service.yml
    kubectl apply -f k8s/postgresql-service.yml
    kubectl apply -f k8s/rabbitmq-service.yml
    kubectl apply -f k8s/api-service.yml
    ```
6. Use port forwarding to connect port 8080 on your bare-metal machine to port 8080 on the nginx-service.
    ```bash
    kubectl port-forward service/nginx-service 8000:8080
    ```
7. Access the api.
    ```bash
    # signup to create a user
    curl -X POST http://localhost:8000/api/signup/ -H "Content-Type: application/json" -d '{"username":"stevo", "password":"stevo123"}'
    # response
    { 'message': 'User signup successful.' }

    # login to get the access token
    curl -X POST http://localhost:8000/api/login/ -H "Content-Type: application/json" -d '{"username":"stevo", "password":"stevo123"}'
    # response
    { 'token': 49072f4a93b5fe9bed37551f951e9aba2a786397 }
    ```




# API Documentation
This can be accessed through an authenticated request at the http://localhost:8000/api/docs/ endpoint.

# Tests
Tests can be run through via `coverage`.

```bash
coverage run manage.py test
```

Test coverage can be viewed by running

```bash
coverage report -m
```