FROM node:20-bookworm

# Install Python 3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN python3 -m venv .venv \
    && . .venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r backend/requirements.txt

# Copy backend
COPY backend ./backend

# Copy and build frontend
COPY frontend ./frontend
WORKDIR /app/frontend
RUN npm ci || npm install \
    && npm run build

# Expose ports
EXPOSE 3000 8000

# Start script
WORKDIR /app
COPY start.sh ./start.sh
RUN chmod +x start.sh

ENV PATH="/app/.venv/bin:${PATH}"
ENV API_PORT=8000
ENV FRONTEND_PORT=3000
ENV BACKEND_URL=http://localhost:8000

CMD ["./start.sh"]


