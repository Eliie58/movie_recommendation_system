# Movie Recommendation System

Movie Recommendation System, built using AI

## Components

This system contains 6 main services:

- Database [PostgreSQL]("https://www.postgresql.org/")
- Api [FastAPI]("https://fastapi.tiangolo.com/")
- Web Interface [Streamlit]("https://streamlit.io/")
- Prediction model [surpriselib]("https://surpriselib.com/")
- Job scheduling [Apache Airflow](https://airflow.apache.org/)
- Monitoring Dashboard [Grafana](https://grafana.com/)

## System Design

Ever felt not sure regarding which movie to watch next?<br>
This project aims to solve this problem.<br>

- The streamlit frontend shows the users movies, that can be filtered by genre and movie name. The user will pick a movie, and request others similar to it.
- The frontend will send http request to the fastapi backend, with the movie id. In the backend, we will use a pretrained model for inference. The predicted information will be stored in the database, and the user will be directed to a page to see the prediction results.
- We have a grafana dashboard, for monitoring system performances as well.
- The frontend also supports Batch predictions, where users can upload a file with a list of movie ids.

The system also supports B2B batch predictions, where business will upload their batch predictions to a shared folder, and we will output the predictions to a different folder.

- Job scheduling. We have 3 scheduled jobs:
  1. B2B Simulation: We simulate the B2B requests with randomly generated request files.
  2. Data Ingestion: We validate the input files using [great expectations](https://greatexpectations.io/), and move the valid files to the Prediction folder.
  3. Prediction Job: Read all files in the prediction job, and for each, call api batch prediction endpoint, and write the result to output folder.

![System Design](System%20Design.svg)

## Run

The movie recommendation system can be run in 2 ways

### Docker compose

To start the system, follow these steps:

- Download the code
- Navigate to the root directory of the project
- Build the image

```
docker-compose build
```

- Start the container

```
docker-compose up
```

### Individual services

To start the services individually, follow these steps:

#### Database

If you already have a [PostgreSQL]("https://www.postgresql.org/") database running locally, run the `init.sql` script under `streamlit` directory to create the tables.
<br>
In you don't want to install [PostgreSQL]("https://www.postgresql.org/") locally, you can run it using docker compose.
<br>
Follow these steps:

- Download the code
- Navigate to the root directory of the project
- Build the image

```
docker-compose build
```

- Start the postgres service from container

```
docker-compose up postgres
```

#### Api

To start the api, follow these steps:

- Download the code
- Navigate to the root directory of the project
- Create and activate a new conda environment

```
conda create --name fastapi
conda activate fastapi
```

- Install the requirements

```
pip install -r api/requirements.txt
```

- Set the environemnt variable. For linux

```
export DATABASE_URL=postgresql://fastapi:fastapi@localhost:5432/movies
```

- Start the api

```
./start.sh
```

- To test the api, you can go to `http://localhost:8080/genres`

#### Web Interface

To start the api, follow these steps:

- Download the code
- Navigate to the root directory of the project
- Create and activate a new conda environment

```
conda create --name streamlit
conda activate streamlit
```

- Install the requirements

```
pip install -r streamlit/requirements.txt
```

- Set the environemnt variable. For linux

```
export API_URL=http://localhost:8080
export BASE_URL=http://localhost:8501
```

- Start the Web Interface

```
streamlit run streamlit/Home.py
```

- Navigate to `http://localhost:8501`

#### Model

Steps for training and using the prediction model are in the model [README.MD](model/README.md)

#### Job Scheduling

To run the job scheduler, follow these steps:

- Download the code
- Navigate to the airflow directory of the project
- Create and activate a new conda environment

```
conda create --name airflow
conda activate airflow
```

- Install the requirements

```
pip install -r requirements.txt
```

- Set the environemnt variable. For linux

```
export API_URL=http://localhost:8080
```

- Create the data folders

```
mkdir data/b2b_input
mkdir data/validation_input
mkdir data/prediction_input
mkdir data/rejected
mkdir data/output
```

- Start the scheduler

```
./start.sh
```

- To view the airflow web interface, you can go to `http://localhost:9091`

#### Grafana

Follow the steps to setup grafana from the official sources `https://grafana.com/docs/grafana/latest/setup-grafana/installation/`.<br>
After installing and running the local grafana instance, create a new postgres datasource, and dashboards to visualize sysem performance.
Example dashboard:
![Example dashboard](Example_dashboard.png)

### Useful command

In order to reseed the database at container startup, run the following from the root of the project:

```
docker-compose down --volumes
docker-compose build
docker-compose up
```

This will remove the volumes used to store the database, and will trigger the `init.sql` script at startup.
<br>
When the api receives the first call, the seeder will run and populate `genre` and `movie` tables.
