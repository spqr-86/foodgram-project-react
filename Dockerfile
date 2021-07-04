FROM python:3.8.5


RUN mkdir /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
WORKDIR /code
COPY entrypoint.sh .
ENTRYPOINT ["sh", "entrypoint.sh"]
