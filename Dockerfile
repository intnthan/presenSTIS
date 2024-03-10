# dockerfile
FROM python:3.12.1-bookworm

# allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True
# copy local code to the container image
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade pip 

# run the web service on container startup. here we use the gunicorn webserver, with one worker process and 8 threads
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
