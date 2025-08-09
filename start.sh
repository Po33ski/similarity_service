#!/usr/bin/env bash
set -euo pipefail

if [ -f ".env.local.sh" ]; then
  set -a
  source ./.env.local.sh
  set +a
fi

# Activate python venv
source ./.venv/bin/activate

# Start backend
uvicorn backend.api.main:app --host 0.0.0.0 --port "${API_PORT:-8000}" &

# Start frontend
cd frontend
BACKEND_URL="http://127.0.0.1:${API_PORT:-8000}" npm run start &

wait -n


