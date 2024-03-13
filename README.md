# Backend clone  of social media app by using FastAPI

#### This API  has 4 routes

## 1) Post route

#### This route is reponsible for creating post, deleting post, updating post and retrieving post

## 2) Users route

#### This route is about creating users and searching user by id

## 3) Auth route

#### This route is about logging into the system

## 4) Vote route

 #### This route is about likes or vote system. This route contains code to upvote or remove vote. There is not logic for down vote.

# How to run locally
First clone this repo by using following command
````

git clone https://github.com/yazmintorres/learn-fastapi.git

````
then 
````

cd fastapi-project

````

Then install all dependencies

````

pip install -r requirements.txt

````

Then cd into app folder and run the following command
````

uvicorn main:app --reload

````

Then you can use following link to use the  API

````

http://127.0.0.1:8000/docs 

````

## This API requires a database in PostgreSQL
Create a database in postgres then create a file name .env in the root folder and write the following things in the file 

````
DB_HOSTNAME = localhost
DB_PORT = 5432
DB_PASSWORD = passward_that_you_set
DB_NAME = name_of_database
DB_USERNAME = User_name
SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60

````
Then, run the following command from the root folder to create the necessary tables

````

alembic upgrade head

````
### Note: SECRET_KEY in this exmple is just a pseudo key. You need to get a key for youself and you can get the SECRET_KEY from [FastAPI Documentation - Obtain a Secret Key](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=secret+key#handle-jwt-tokens)

