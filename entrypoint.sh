#!/bin/bash
prisma generate --schema /db/schema.prisma
uvicorn main:app --host 0.0.0.0 --port 8000