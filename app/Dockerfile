

# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8.10-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

EXPOSE 8080

CMD python app.py