# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install system dependencies for mysqlclient and other tools
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    netcat-openbsd \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app/backend"

# Copy the backend directory contents and entrypoint script into the container
COPY backend /app/backend
COPY entrypoint.sh /app/
# COPY ./migrations /app/migrations

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install gunicorn python-dotenv

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=development

# Specify the script to be executed when the container starts
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "--log-level", "debug", "backend.app:app"]
