#FROM colesbury/python-nogil
FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
WORKDIR /app/kitchen_api

EXPOSE 5000
CMD ["python", "kitchen.py"]