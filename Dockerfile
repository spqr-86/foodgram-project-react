FROM python:3.8.5

WORKDIR /code
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
COPY entrypoint.sh .
ENTRYPOINT ["sh", "entrypoint.sh"]
