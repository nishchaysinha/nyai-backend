# Use the official Python 3.12.2 image as the base image
FROM python:3.12.2

# Set the working directory inside the container
WORKDIR /app

# copy all the files from the current directory to the working directory
COPY . .

#expose the port
EXPOSE 8000


# Make the setup.sh script executable
RUN chmod +x setup.sh

# Install the required dependencies
RUN apt update
RUN apt install tesseract-ocr libtesseract-dev -y

# Run the setup.sh script when the container starts
CMD ["./setup.sh"]
