#!/bin/bash
docker compose down -f ../docker-compose.yml && docker compose up -d --no-deps --build -f ../docker-compose.yml