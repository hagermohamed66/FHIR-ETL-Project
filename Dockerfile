# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install any required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run your script
CMD ["python", "main.py"]
