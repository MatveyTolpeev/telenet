FROM python:3.8

WORKDIR /telenet

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app_telenet ./src

CMD ["python", "./src/manage.py", "runserver", "0.0.0.0:8000"]