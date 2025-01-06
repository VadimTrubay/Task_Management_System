FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python task_management/manage.py migrate && python task_management/manage.py runserver 0.0.0.0:8000"]
