# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    udev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create a group with the same GID as the host's dialout group
RUN groupadd -g 20 dockerdialout

# Create a non-root user and add to the dockerdialout group
RUN useradd -m myuser && usermod -a -G dockerdialout myuser

# Set up USB device access
RUN mkdir /dev/bus && mkdir /dev/bus/usb

# Run as non-root user
USER myuser

# Run the application
CMD ["python", "app.py"]
