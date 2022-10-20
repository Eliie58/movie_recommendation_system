FROM python:3.9
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 8501

COPY . /app
CMD ["streamlit", "run", "streamlit/Home.py"]