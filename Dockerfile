FROM python:3.10-alpine
WORKDIR .
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000

CMD python manage.py runserver 127.0.0.0:8000