
# Use the official Python runtime as a parent image
FROM python:3.11.3

# Set the working directory to /app
WORKDIR /SCMXPERTLITE/Back

# Install any needed packages specified in requirements.txt
RUN pip install pymongo python-dotenv requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /SCMXPERTLITE/Back

# Expose port 80 for the FastAPI app to listen on
EXPOSE 8000

# Define the command to run your FastAPI application when the container starts
CMD ["uvicorn","main:app","--reload"]