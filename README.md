# Lunch Service API
## Project Overview

This project provides an internal service for employees to make decisions on lunch places by voting on daily restaurant menus. Restaurants upload their menus, and employees use a mobile app to vote. The API is built using Python and Django Rest Framework (DRF). The service supports both old and new versions of the mobile app and is containerized for easy deployment.

## Features

- Authentication: User authentication for employees and restaurant admins.
- Restaurant Management: Create and manage restaurant details.
- Menu Uploading: Restaurants can upload their daily menus through the API.
- Employee Management: Create employee records for voting and user management.
- Voting:
  - Old Version: Employees can vote for a single menu.
  - New Version: Employees can vote for their top three menus, assigning points from 1 to 3.
- Results: Retrieve the aggregated voting results for the current day.

## Technologies Used
- Backend: Python, Django Rest Framework (DRF)
- Database: PostgreSQL
- Containerization: Docker
- Documentation: Swagger (`drf-yasg`)
- Linting and Type Checking: `ruff`, `mypy`
- Testing: `pytest`, `pytest-django`

## Project Setup
### Prerequisites

- Docker & Docker Compose

### Running the Application with Docker
The application is fully containerized using Docker. You can use Docker Compose to build and run both the Django application and the PostgreSQL database in containers.

### Docker Compose Setup

1. Environment Configuration

Ensure you have a `.env` file in the root directory. This file contains all the necessary environment variables:

```.dotenv
LS_POSTGRES_NAME=
LS_POSTGRES_USER=
LS_POSTGRES_PASSWORD=
LS_POSTGRES_HOST=db
LS_POSTGRES_PORT=

```

2. Build and run docker containers


Run the following command to build and run the services defined in docker-compose.yml:

```bash
docker-compose up --build -d
```
This command will:

- Build the Docker images for both the web and database services.
- Run the containers in the background.

3. Accessing the Application

Once the containers are up and running, you can access:

- Admin Dashboard: http://localhost:8000/admin/
- Swagger Documentation: http://localhost:8000/swagger/

4. API Documentation
API documentation is available via Swagger:

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Permissions
### Role-Based Access

#### Admin:

- Can create, update, delete restaurants and employees.
- Can access all votes and view voting results.

#### Restaurant User:
- Can create, update, and delete their own restaurant menus.

#### Employee:
- Can vote for menus and manage their own votes.
- Can read restaurants and menus.

## Permissions Summary

| Role            | Permissions                    |
| --------------- | ------------------------------ |
| Admin           | Full access to all resources   |
| Restaurant User | Manage their own menus         |
| Employee        | Vote for menus, manage own votes |


## POPULATE_DATA
The `POPULATE_DATA` flag in the `.env` file controls whether the database should be populated with dummy data on startup. It is set to True by default. If you want to prevent dummy data from being added, set POPULATE_DATA to False in the .env file.

Example `.env`:
```dotenv
POPULATE_DATA=True
```

## Running Tests
To run the tests, you need to have a local version of the database running. You can use Docker to start a local PostgreSQL instance with the required credentials.

#### Dummy Script to Run Local Database with Docker
Use the same creds you defined in `.env`, so that the app can access the DB in test time.
```bash
docker run --name lunch_service_db_test \
  -e POSTGRES_DB=... \
  -e POSTGRES_USER=... \
  -e POSTGRES_PASSWORD=... \
  -p 5432:5432 \
  -d postgres:15
```
This script will:

Start a PostgreSQL container with the necessary environment variables.
The database will be available on port 5432.

#### Running the Tests
Once the database is up and running, you can run the tests using:

```bash
pytest core/tests.py
```
Shutting Down the Local Database
After running the tests, you can stop and remove the database container with:

```bash
docker stop lunch_service_db_test
docker rm lunch_service_db_test
```

## API Endpoints
Below are the key endpoints provided by the service:

- **Restaurant Management**

`/api/restaurants/` (POST, GET, PUT, DELETE): CRUD operations for restaurants.

- **Menu Management**

`/api/menus/` (POST, GET): Upload and retrieve menus.

- **Employee Management**

`/api/employees/` (POST, GET, PUT, DELETE): CRUD operations for employees.

- **Voting**

`/api/votes/` (POST): Vote for menus.
`/api/votes/results/today/` (GET): Get current day voting results.


## High Availability Cloud Architecture (Azure)
To ensure a robust and scalable deployment of the Lunch Service API, consider the following High Availability (HA) architecture using Azure components:

### Architecture Components

1. **Azure Kubernetes Service (AKS):**

Use AKS to manage Docker containers for the Django API and PostgreSQL, allowing for easy scaling and self-healing.

2. **Azure Database for PostgreSQL:**

Use Azure's managed PostgreSQL service to handle the database, ensuring automatic backups, scaling, and high availability.

3. **Azure Application Gateway:**

Use Application Gateway as a load balancer to distribute incoming requests evenly across AKS instances, ensuring reliable access.

4. **Azure Redis Cache:**

Use Azure Redis Cache to store frequently requested data, such as daily menus, to improve performance and reduce load on the database.

5. **Monitoring & Alerts:**

Use Azure Monitor for logging and performance monitoring.
Set up alerts for critical metrics such as CPU utilization, memory usage, and database connections.



                       +-----------------------------+
                       |     Azure Application       |
                       |         Gateway             |
                       +------------+----------------+
                                    |
                     +--------------v--------------+
                     |  Azure Kubernetes Service   |
                     | (Django Containers + Celery) |
                     +------+------------+----------+
                            |            |
                +-----------v+          +v-----------+
                |  Redis Cache|          | PostgreSQL  |
                | (Azure Redis)          |  (Managed)  |
                +------------+           +------------+


- Application Gateway: Handles incoming HTTP requests and distributes them among multiple instances of the Django app.
- Kubernetes Service: Hosts the Django API in containers, manages auto-scaling, and ensures resilience.
- Azure Redis Cache: Improves the speed of frequently requested data, like daily menus and voting results.
- Azure Managed PostgreSQL: Ensures a reliable and managed database with automated backup and scaling.


## Future Improvements
- Load Testing: Use a tool like Locust to identify bottlenecks and optimize performance.
- CI/CD Pipeline: Implement continuous integration and deployment using GitHub Actions or Azure DevOps.
- Improved Security: Use Azure Key Vault to store sensitive information such as database credentials.

## Contact
For further questions, contact:

- Developer: Evgenii Saurov
- Email: saurov.ev@gmail.com