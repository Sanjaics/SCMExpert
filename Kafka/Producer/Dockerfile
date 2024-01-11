# Use the official Python runtime as a parent image
FROM python:3.12.0
 
# Set the working directory to /app
WORKDIR /SCMXPERTLITE/Kafka/Producer
 
# Install any needed packages specified in requirements.txt
RUN pip install python-dotenv confluent-kafka 
 
 
 
# Copy the rest of the application code into the container at /app
COPY . /SCMXPERTLITE/Kafka/Producer
 
 
# Define the command to run your FastAPI application when the container starts
CMD ["python", "producer.py"]