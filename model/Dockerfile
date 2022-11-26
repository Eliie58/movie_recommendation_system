FROM python:3.9
WORKDIR /model

COPY ./requirements.txt /model/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /model/requirements.txt

EXPOSE 5000

COPY . /model

RUN chmod 777 /model/start.sh
RUN mkdir /model/models

CMD /model/start.sh

