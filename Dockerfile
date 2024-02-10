# continuumio/anaconda3: This image is a Docker container with a bootstrapped installation of Anaconda (based on Python 3.X) that is ready to use.
FROM python:3.9.18

# The dot(.) tells docker to copy all the files and folders (except the ones we wrote in the .dockerignore file) and create a path
# which is (/usr/app) then paste them all in the app dirctory
WORKDIR /usr/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "./API using flask and Swagger.py"]



