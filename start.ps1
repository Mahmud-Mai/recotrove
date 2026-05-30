# start.ps1 - Windows PowerShell startup script
Write-Host "Starting RecoTrove Development Environment" -ForegroundColor Green

# Check if Docker is running
$dockerRunning = docker info 2>$null
if (-not $dockerRunning) {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Check if Python virtual environment exists
if (-not (Test-Path "backend\venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    cd backend
    python -m venv venv
    cd ..
}

# Activate virtual environment and install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ..

# Start Docker services
Write-Host "Starting Docker Compose services..." -ForegroundColor Yellow
docker-compose up -d

# Wait for database to be ready
Write-Host "Waiting for database to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Run database migrations (we'll add this in Sprint 2)
# docker-compose exec backend alembic upgrade head

# Seed admin user
Write-Host "Seeding admin user..." -ForegroundColor Yellow
docker-compose exec backend python seed_admin.py

Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host "API running at: http://localhost:8030" -ForegroundColor Cyan
Write-Host "API docs: http://localhost:8030/docs" -ForegroundColor Cyan
Write-Host "MinIO console: http://localhost:9001 (minioadmin/minioadmin123)" -ForegroundColor Cyan
Write-Host "MailHog: http://localhost:8025" -ForegroundColor Cyan
Write-Host ""
Write-Host "To stop everything: docker-compose down" -ForegroundColor Yellow