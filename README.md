# Account Management System

## Quick Start
### Pulling the Docker Image
To get started, pull the Docker image from Docker Hub:[yuandata/acct-mamt-image](https://hub.docker.com/r/yuandata/acct-mamt-image)
```sh
docker pull yuandata/acct-mamt-image
```

### Running the Container
After pulling the image, run the container using the following command:
```sh
docker run -d -p 8000:8000 yuandata/acct-mamt-image
```
This command starts the application and exposes it on port 8000 of your localhost.

## Testing the APIs
Once the application is running, you can test the APIs using `curl`.

- **Create Account:**
```sh
curl -X POST http://localhost:8000/account/create/ -d '{"username": "Urban", "password": "123456Ab"}' -H "Content-Type: application/json"
```
- **Verify Account and Password:**
```sh
curl -X POST http://localhost:8000/account/verify/ -d '{"username": "Urban", "password": "123456Ab"}' -H "Content-Type: application/json"
```

## API Documentation
For a comprehensive guide and interactive documentation, visit:
- **Online Documentation:** [yuandata.github.io/acct-mgmt-swagger](https://yuandata.github.io/acct-mgmt-swagger/)
- **Local Documentation:** To view the API documentation locally, follow these steps:

1. Clone the repository and navigate to the project directory:
    ```sh
    git clone git@github.com:YuanData/acct_mamt.git
    cd acct_mamt
    ```
2. Start the Django project:
    ```sh
    python manage.py runserver
    ```
3. Open your browser and navigate to [http://localhost:8000/swagger/](http://localhost:8000/swagger/) to access the Restful API documentation.


## Running Unit Tests
To run the unit tests, execute the following command in the project directory:
```sh
python manage.py test account
```
