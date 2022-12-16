# Movie Recommendation System

Movie Recommendation System, built using AI

## Components

This system contains 6 main services:

- Database [PostgreSQL]("https://www.postgresql.org/")
- Api [FastAPI]("https://fastapi.tiangolo.com/")
- Web Interface [Streamlit]("https://streamlit.io/")
- Prediction model [surpriselib]("https://surpriselib.com/")
- Job scheduling [Apache Airflow](https://airflow.apache.org/)

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

In order to automate the job scheduling we are using airflow.
We have 2 scheduled jobs:

- Data Ingestion:<br>
  Copy B2B incoming files from b2b-input folder, to prediction-pipeline folder.
- Batch Prediction:<br>
  Use [great expectations](https://greatexpectations.io/) to validate b2b data quality, and discard any invalid inputs, after sending notifications.<br>
  Calling the batch prediction api endpoint to get the prediction, and output the results under b2b-output folder

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

- Start the scheduler

```
./start.sh
```

- To view the airflow web interface, you can go to `http://localhost:9091`

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
