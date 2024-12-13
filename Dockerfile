FROM python:3.11.11

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY ./littlelemon .


# Start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--chdir", "littlelemon","littlelemon.wsgi:application"]