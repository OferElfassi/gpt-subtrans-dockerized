# Stage 1: Builder
FROM alpine:latest AS builder

# Install required packages
RUN apk add --no-cache curl tar

# Set environment variables
ENV VERSION=0.8.3
ENV REPO_URL=https://github.com/machinewrapped/gpt-subtrans/archive/refs/tags/v${VERSION}.tar.gz

# Download and extract the repository
WORKDIR /tmp
RUN curl -L ${REPO_URL} -o gpt-subtrans-${VERSION}.tar.gz && \
    tar -xzf gpt-subtrans-${VERSION}.tar.gz

# Stage 2: Runtime
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files from builder stage
COPY --from=builder /tmp/gpt-subtrans-0.8.3 /app

# Copy necessary files from current directory to container
COPY .env /app/
COPY entrypoint.sh /app/
COPY folder-subtrans.py /app/scripts/

# Install dependencies
RUN python3 -m venv envsubtrans \
    && . envsubtrans/bin/activate \
    && pip install --upgrade pip \
    && pip install openai \
    && pip install --upgrade -r requirements.txt
    # install other providers if needed

# Make entrypoint.sh executable
RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
