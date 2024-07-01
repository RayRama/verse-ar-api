# Use the official Python 3.10 image as the base image
FROM python:3.10-bullseye

# Author
LABEL author="Ray Ramadita"

# Set the working directory inside the container
WORKDIR /verse-ar

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 7025

# Set the entrypoint command to run the Flask app
CMD ["python", "main.py"]
