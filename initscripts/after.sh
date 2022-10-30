#!/bin/bash
docker compose -f /opt/foodrle/docker-compose.yml down && docker compose -f /opt/foodrle/docker-compose.yml up -d --no-deps --build