# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the dependencies file first (to leverage Docker cache)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire FastAPI app to the container
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Set environment variables for the database
ENV DATABASE_URL=postgresql://postgres:postgres@db:5432/resumes_db

# Command to start FastAPI when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
