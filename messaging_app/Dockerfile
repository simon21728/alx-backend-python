# Use Python 3.10 as the base image
FROM python:3.10

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . /app/

# Expose Django port
EXPOSE 8000

# Start Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
