# back-lab4
Варіант 2 (= 1301 mod 3)

## Installation and starting of the service

    docker compose up

The web service will be available under http://localhost:8080 <br>
The postgres server will be available under `postgresql://postgres:<password>@localhost:5432/postgres` <br>


DB user, password, name and host can be configured in `docker-compose.yaml`

## Deployed instance
A deployed instance of this web service is available under https://back-lab4.onrender.com
(The new web service uses the same db instance as in back-lab3, hence different table names)

## Postman collection
The Postman collection of all API requests is under `postman/Lab 4.postman_collection.json`
link: https://www.postman.com/joint-operations-operator-59334073/workspace/my-workspace/overview

## Postman flow
To test the API, a corresponding postman flow was created
link: https://www.postman.com/joint-operations-operator-59334073/workspace/my-workspace/overview