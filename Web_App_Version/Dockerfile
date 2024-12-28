# Base image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    APP_HOME=/app

# Set working directory
WORKDIR $APP_HOME

# Copy project files into container
COPY . $APP_HOME/

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Command to run the app
CMD ["python", "web_app.py"]
