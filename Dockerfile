# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    netcat-openbsd \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY ./backend /app/backend
COPY entrypoint.sh /entrypoint.sh

# Specify the script to be executed when the container starts
ENTRYPOINT ["/entrypoint.sh"]

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install python-dotenv

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World
# ENV FLASK_APP backend/app.py

# Run app.py when the container launches
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "--log-level", "debug", "backend.app:app"]
