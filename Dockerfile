# Pin to a specific version — never use latest
FROM ubuntu:22.04

# Avoid interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive

# Install only what's needed
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only the scripts — not logs, testproject, etc.
COPY smart.sh deploy.sh pipeline.sh ./
COPY lib/ ./lib/

# Make scripts executable
RUN chmod +x smart.sh deploy.sh pipeline.sh

CMD ["bash", "pipeline.sh"]
