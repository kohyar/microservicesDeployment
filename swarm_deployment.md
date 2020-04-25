# Sample microservices architecture using python flask and sql alchemy

https://docs.docker.com/engine/swarm/stack-deploy/
https://docs.docker.com/network/network-tutorial-overlay/

# Docker deployment
## Deploy using Swarm, Docker, Gunicorn and MySQL
### Setup
To deploy multiple instances of the microservices on a cluster of hosts use the following
instructions.

* Install docker: https://docs.docker.com/install/linux/docker-ce/ubuntu/
* Install docker-compose: https://docs.docker.com/compose/install/
* Clone repository: <code>$ git clone https://github.com/elbuco1/microservices.git</code>
* Go in the **microservices** directory: <code>$ cd microservices</code>
* Go in **movies/config.py** and **evaluations/config.py** and set
```python
class Config(object):
    deploy = 'docker'
```

* The databases run on separate containers. They need some time to initialized. We need a
way to make evaluations service and movie service to wait for their respective databases
to be up. To that end we use the bash command <code> sleep x </code> where x is a number of 
seconds. You should go in the files **movies/boot.sh** and **evaluations/boot.sh** and set 
the waiting time. 60 seconds should be enough:
```bash
echo "Waiting for MySQL..."
sleep 60
echo "Resume..."
```


* In **docker-compose-swarm.yml**, you can set for each service the number of instances required:

```bash
services: 
  movies:
    image: 127.0.0.1:5000/movies-app
      ...
    deploy:
      mode: replicated
      replicas: 3
```
Default is 3 instances for the movies service and the evaluation service. One instance for the
movies database container and for the evaluations database container.


### Deploy

* You need multiple hosts available. One is going to be the manager. The other ones will be the workers.
We deploy from the manager.

* First open a terminal on the manager and find its ip adress using:

<code>$ ifconfig </code>

```bash
enp0s31f6:  ...
        inet 132.207.x.x  ...
            ...
```
Here the manager ip address is 132.207.x.x .

* On the manager initialize the swarm: 

<code>$ sudo docker swarm init --advertise-addr 132.207.x.x </code>

on the ouput you can find a command looking like:

<code>$ sudo docker swarm join --token [ some-id ] 132.207.x.x:2377 </code>

* On every worker, open a terminal and paste it there. This will make the workers join the swarm.


#### Create a local registry for images

* We need to create a local repository of docker images on the manager. This way we can build and store
the docker images of our services using docker. We will need the already built images for the swarm deployment.

<code>$ sudo docker service create --name registry --publish published=5000,target=5000 registry:2</code>

* You can test the registry using: 

<code>$ curl http://localhost:5000/v2/ </code>


#### Building images for swarm 

* We then build and run the docker images using docker-compose:

sudo docker-compose -f docker-compose-swarm.yml up -d --build

* Wait aroud 60 seconds and test the app:

<code>$ curl http://localhost:8081/evaluations/movies/1 </code>

The result should be:

<code> {"evaluations":[{"description":"What a baaad movie!","id":1,"movie_id":1}]} </code>

* Now shut down the app:

<code>$ sudo docker-compose down --volumes </code>

* And push the built docker images to the local registry 

<code>$ sudo docker-compose -f docker-compose-swarm.yml push </code>

#### Deploying on the swarm 

* Deploy the stack on the swarm
<code>$ sudo docker stack deploy --compose-file docker-compose-swarm.yml [ stack-name ] </code>

* You can check the deployment of every service using: 

<code>$ sudo docker stack services [ stack-name ] </code>

* Again wait around 60 seconds and test the app:

<code>$ curl http://localhost:8081/evaluations/movies/1 </code>

The result should be:

<code> {"evaluations":[{"description":"What a baaad movie!","id":1,"movie_id":1}]} </code>


* You can test the app from another host connected to the network using the ip address of the manager:

<code>$ curl http://132.207.x.x:8081/evaluations/movies/1 </code>

* You can see on what worker the service instances are deployed:

<code>$  sudo docker service ps stack_db_evaluations  </code>

<code>$  sudo docker service ps stack_movies </code>

<code>$  sudo docker service ps stack_db_movies </code>

<code>$  sudo docker service ps stack_evaluations </code>


#### Stop and clean





* Stop the stack: 

<code>$ sudo docker stack rm stack </code>

* Stop local registry 
<code>$ sudo docker service rm registry </code>


* Make manager leave the swarm:

<code>$ sudo docker swarm leave --force </code>

* Make worker leave the swarm:

<code>$ sudo docker swarm leave </code>
