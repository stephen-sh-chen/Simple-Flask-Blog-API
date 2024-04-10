<h1 align = 'center'> Simple blog API backend</h1>

<p align="center">
  <a href="https://flask.palletsprojects.com/en/3.0.x/">
    <img src="https://img.shields.io/badge/Language-Python_3.12.2-blue?style=for-the-badge&logo=Python" alt="Language Python 3.12.3 Badge">
  </a>
  <a href="https://flask.palletsprojects.com/en/3.0.x/">
    <img src="https://img.shields.io/badge/Framework-Flask_3.0.3-blue?style=for-the-badge&logo=Flask" alt="Framework Flask 3.0.3 Badge">
  </a>
  <a href="https://www.jetbrains.com/pycharm/" title="PyCharm">
    <img src="https://img.shields.io/badge/IDE-PyCharm-red?style=for-the-badge&logo=pycharm" alt="IDE PyCharm Badge">
  </a>
</p>

## Requirements
* Create APIs that support:
  1. Creating a new blog post 
  2. Retrieving a list of all blog posts 
  3. Retrieving a single blog post by its ID 
  4. Updating an existing blog post 
  5. Deleting a blog post 
  6. Implement basic authentication for the API. Users should be able to sign up, sign in, and authenticate their requests to create, update, or delete blog posts.

## Project Structure
```
├── README.md
├── app
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── post.py
│   │   └── user.py
│   ├── resources
│   │   ├── __init__.py
│   │   ├── post.py
│   │   └── user.py
│   └── tests
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_config.py
│       ├── test_post.py
│       └── test_user.py
├── config.py
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── 8a5273f4d630_initial_migration.py
├── run.py
└── screenshots
    ├── app_launched.png
    ├── create_a_new_post.png
    ├── delete_a_post.png
    ├── retrieve_a_list_posts.png
    ├── retrieve_a_single_post.png
    ├── update_a_post.png
    ├── user_login_got_token.png
    └── user_sign_up.png
```

## Install
### Step 1 - Install dependency
`pip install flask-restful flask-sqlalchemy flask-jwt-extended psycopg2-binary pytest flask-testing`

### Step 2 - Setup PostgresSQL
1. Install PostgrsSQL: `brew install postgresql`
2. Start the PostgreSQL `brew services start postgresql`
3. `brew install postgresql`
4. `psql postgres`
5. `CREATE ROLE stephen_oa WITH LOGIN PASSWORD 'stephen1123';`
6. `ALTER ROLE stephen_oa CREATEDB;`
7. `\q`
8. `psql postgres -U stephen_oa`
9. `CREATE DATABASE fpp_db;`
10. `GRANT ALL PRIVILEGES ON DATABASE fpp_db TO stephen_oa;`

### Step 3 - Configurations
In your-blog-app/config.py, define your configurations
```
    SECRET_KEY = 'your_secret_key'  # Change this to a random secret key
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/your_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Change this to a random JWT secret key
```
### Step 4 - Create database and tables
  * `flask db init`
  * `flask db migrate -m "Initial migration."`
  * `flask db upgrade`

### Step 5 - Run the application
```shell
export FLASK_APP=run.py
flask run
```
* 📷 Successfully launched the application:
![img.png](screenshots/app_launched.png)

## Usage

### Prerequisite
* Install json pretty print tool "jq".
  * `brew install jq`

### User Sign Up
```shell
curl -X POST http://127.0.0.1:5000/register \
-H "Content-Type: application/json" \
-d '{"username": "newuser", "password": "newpassword", "email": "newuser@example.com"}' \
| jq
```
* 📷 Response:
* ![img.png](screenshots/user_sign_up.png)

### User Login
```shell
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "newuser", "password": "newpassword", "email": "newuser@example.com"}' \
| jq
```
* 📷 Response:
* ![img.png](screenshots/user_login_got_token.png)

### Refresh token
* Once the token is expired, execute the commands to refresh it.
```shell
response=$(curl -s -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "newuser", "password": "newpassword", "email": "newuser@example.com"}')

export JWT_TOKEN=$(echo $response | jq -r '.access_token')
export REFRESH_JWT_TOKEN=$(echo $response | jq -r '.refresh_token')

echo "JWT_TOKEN=$JWT_TOKEN"
echo
echo "REFRESH_JWT_TOKEN=$REFRESH_JWT_TOKEN"
```

### Create a new blog post
```shell
curl -X POST http://127.0.0.1:5000/posts \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $JWT_TOKEN" \
-d '{"title": "New Post Title", "body": "Content of the new post."}' \
| jq
```
* 📷 Response:
* ![img.png](screenshots/create_a_new_post.png)

### Retrieving a list of blog posts
```shell
curl -X GET http://127.0.0.1:5000/posts | jq
```
* 📷 Response:
* ![img.png](screenshots/retrieve_a_list_posts.png)

### Retrieving a single blog post by its ID
```shell
curl -X GET http://127.0.0.1:5000/posts/8 \
-H "Authorization: Bearer $JWT_TOKEN" \
| jq
```
* 📷 Response:
* ![img.png](screenshots/retrieve_a_single_post.png)

### Updating an existing blog post
```shell
curl -X PUT http://127.0.0.1:5000/posts/8 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $JWT_TOKEN" \
-d '{"title": "Updated Title", "body": "Updated content of the post."}' \
| jq
```
* 📷 Response:
* ![img.png](screenshots/update_a_post.png)

### Deleting a blog post
```shell
curl -X DELETE http://127.0.0.1:5000/posts/9 \
-H "Authorization: Bearer $JWT_TOKEN" \
| jq
```
* 📷 Response:
* ![img.png](screenshots/delete_a_post.png)

## Future improvements
1. More comprehensive logs.
1. Error handling with retry mechanism.
1. Emit metrics:
   1. API latency
   1. 4XX error
   1. 5XX error
   1. Throughput (TPS)
   1. Host CPU, Memory, Disk usages
1. Make the project Installable
1. Containerize the application and deploy to EKS
1. Store the credentials in an independent secret vault, like AWS Secrete Manager