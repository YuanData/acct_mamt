# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Make sure the start.sh script is executable
RUN chmod +x start.sh

# Use start.sh as the entrypoint to initialize DB and run the server
ENTRYPOINT ["/bin/bash", "start.sh"]
