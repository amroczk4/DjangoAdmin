#!/bin/bash
docker compose -f /opt/foodrle/docker-compose.prod.yml down && docker compose -f /opt/foodrle/docker-compose.prod.yml up -d --no-deps --build