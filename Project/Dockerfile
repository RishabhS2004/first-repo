# Start with Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run full pipeline before starting Flask app
RUN python preprocess.py && \
    python train.py

# Expose port for Flask API
EXPOSE 5000

# Start API when container runs
CMD ["python", "app.py"]
