# Use a lightweight Python base image compatible with linux/amd64
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY solution.py .

# Command to run the script
CMD ["python", "solution.py"]