In order to run the solution, one should use the following command:

docker compose up

Which will build two containers and initialize them with the correct configurations:
* Container with python3.8 image, running the server
* Container with postgres image, running the DB


Then the different endpoints (create, update, get and delete)
can be called using the following url:

http://127.0.0.1:5000/

The parameters should be supplied in the request body.