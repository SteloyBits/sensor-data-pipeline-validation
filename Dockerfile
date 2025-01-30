# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files into the container
COPY requirements.txt .
COPY data_cleaning.py .
COPY sample_data.json .
COPY test_data_cleaning.py .

# Install dependencies
RUN pip install pandas

# Run the data cleaning script
CMD ["python", "test_data_cleaning.py"]
