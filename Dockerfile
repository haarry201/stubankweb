FROM python:3.7
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install pipenv
COPY . /app
WORKDIR /app
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
