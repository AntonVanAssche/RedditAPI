# Test the app in a Python environment.
FROM python:3.11-alpine3.15

# Create app directory.
WORKDIR /usr/src/redditapi/

# Install app dependencies.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code to the container.
COPY src/* .
COPY .env .

# Set environment variable.
ENV FLASK_APP main.py

# Expose port 5000 (default Flask port).
EXPOSE 5000

# Define the command to run the app.
ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]
