#An Alpine image inherits from python
FROM python:3.10.0a6-alpine3.13

LABEL author="Rajesh B"

# Set the Python unbuffered environment variable.
ENV PYTHONUNBUFFERED 1

# Install the deps in requirements.txt file and copy from local .txt file to docker image
COPY ./requirements.txt /requirements.txt
#  Add this line before postgresql to avoid warnings.
RUN apk update
# Add deps for psycopg2 package for Django/Postgres
RUN apk add --update --no-cache postgresql-client jpeg-dev
# Add temp packages needed to install requirements. Assigning alias
RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
# -- Installs the requirements into the Docker image
RUN pip install -r /requirements.txt
# Delete the temporary dependencies we just added
RUN apk del .tmp-build-deps

# Create a 'app' file and make it the working DIR
RUN mkdir /app
# Make it as working directory
WORKDIR /app

# Copy the app file contents to our Docker image. 
COPY ./app /app

# Create a user that gonna run our app using Docker
RUN adduser -D user

# Finally switch to that user using USER
USER user