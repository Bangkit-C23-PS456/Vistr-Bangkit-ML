# Use a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the entire project directory into the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port your FastAPI app is listening on
EXPOSE 8000

# Start the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]