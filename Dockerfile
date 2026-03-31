# Use a simple Linux base
FROM ubuntu:latest

# Set working directory inside container
WORKDIR /app

# Copy all your project files into container
COPY . .

# Install required tools
RUN apt-get update && apt-get install -y \
    bash \
    git \
    && apt-get clean

# Give permission to your scripts
RUN chmod +x smart.sh deploy.sh pipeline.sh

# Run your pipeline when container starts
CMD ["bash", "pipeline.sh"]
