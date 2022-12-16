FROM python:3.10
WORKDIR /home

COPY ./requirements.txt /home/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /home/requirements.txt

COPY . /home

WORKDIR /home/data/b2b_input
WORKDIR /home/data/validation_input
WORKDIR /home/data/prediction_input
WORKDIR /home/data/rejected
WORKDIR /home/data/output
WORKDIR /home

RUN chmod 777 /home/start.sh

EXPOSE 9091

CMD /home/start.sh
