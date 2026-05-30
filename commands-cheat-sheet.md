# Start everything

.\start.ps1

# Or manually start Docker services

docker-compose up -d

# View logs

docker-compose logs -f backend

# Stop everything

docker-compose down

# Stop and remove volumes (WARNING: deletes database data)

docker-compose down -v

# Run Python commands inside container

docker-compose exec backend python seed_admin.py

# Open PostgreSQL shell

docker-compose exec postgres psql -U recotrove_user -d recotrove_db

# Test API (from Windows PowerShell)

Invoke-RestMethod -Uri http://localhost:8030/health

# Rebuild backend (if Dockerfile changes)

docker-compose build backend
docker-compose up -d

# Stop everything

docker-compose down

# Remove old volumes (optional, but clean)

docker-compose down -v

# Rebuild with new config

docker-compose up -d --build

# Check backend logs

docker-compose logs backend
