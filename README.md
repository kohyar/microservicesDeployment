# Sample microservices architecture using python flask and sql alchemy
* This is an example of a microservices application. It is implemented using flask and sql_alchemy. 
* The microservices are implemented as REST APIs and can be queried using http. On some requests, the services
interact over http.
* We deploy the application through three different ways:
    * A basic development deployment on a single host using the native server provided with flask
    * A deployment on a single host using docker. We use gunicorn as app server and mysql as database server.
    * Finally, using swarm we deploy the application on multiple hosts using multiple instances for each service.

A tutorial for each deployment type is available in the repository.


## Global architecture

There are two services:
* Movies: allows to manage movie informations. Each movie has two attributes: the movie name and its release year. The service is implemented as a REST API. All required requests are implemented.
* Evaluations: allows to manage the movie evaluations. Each movie can have any number of evaluation. An evaluation has two attributes: the description and the evaluated movie id. The service is implemented as a REST API. All required requests are implemented.

Each service interacts with its own database.

The two services interact through HTTP protocol for some of the requests.

## Single host dev deployment

To deploy the application on a single host for development purposes, follow the instructions in the file: **local_deployment.md**.


## Deploy using Docker, Gunicorn and MySQL
To deploy the microservices app using docker service using  gunicorn as application server on a single host, follow the instructions
in the file **docker_deployment.md**.


## Multi-host, multi instance deployment using swarm and compose
To deploy the microservices app on multiple hosts, using multiple instances for each service, follow the instructions
in the file **swarm_deployment.md**.
