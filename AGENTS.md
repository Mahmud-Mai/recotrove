# RecoTrove — Agent Guide

## Quick start
```bash
# Start everything (Git Bash on Windows)
./start.bs

# Or step by step with Docker Compose
docker-compose up -d                              # start postgres + backend
docker-compose exec backend python seed_admin.py  # create initial admin user
docker-compose logs -f backend                    # tail backend logs
docker-compose down                               # stop everything
```

## API
- Base: `http://localhost:8030`
- Docs: `http://localhost:8030/docs`
- Health: `GET /health`
- Routes: `/api/v1/auth/*`, `/api/v1/categories`, `/api/v1/resources`, `/api/v1/resources/{id}/ratings`, `/api/v1/rooms`

## Key facts
- **PostgreSQL** via Docker, port `5462` on host (maps to `5432` in container)
- **Backend** port `8030` on host (maps to `8000` in container)
- DB tables auto-created on startup via `app.core.database.Base.metadata.create_all` inside FastAPI `lifespan`
- Two `.env` files: root `.env` (for Docker Compose) and `backend/.env` (for local runs)
- No alembic.ini found — alembic/ dir exists but migrations not wired yet
- No test suite, no lint/typecheck config — adding one must start from scratch

## Project layout
```
backend/
  app/
    main.py              # FastAPI app entrypoint
    core/                # config, database, security
    models/              # SQLAlchemy models (User, Category, Resource, Rating, Room, RoomMember, RoomResource, RoomRating)
    schemas/             # Pydantic schemas (user, category, resource, rating, room)
    api/v1/endpoints/    # route handlers (auth.py, categories.py, resources.py, ratings.py, rooms.py)
    services/            # service layer (category, resource, rating, room)
    utils/               # utilities — currently empty
  seed_admin.py          # Script to create initial admin user (Docker Compose: `docker-compose exec backend python seed_admin.py`)
```

## Notable conventions
- JWT tokens: access (30 min) + refresh (7 day), stored in `python-jose` HS256
- Password hashing: bcrypt via `passlib` — `bcrypt` pinned to `==4.0.1` for passlib 1.7.4 compat (4.1+ breaks passlib)
- User model uses UUID PK, `email` unique index, role field (`user` / `admin`)
- Auth dependency chain: `get_current_user` → `get_current_active_user` → `get_current_admin_user`
- Auth endpoints use `OAuth2PasswordRequestForm` for login (username field = email)
- CORS allows `localhost:3000`, `localhost:5173`, `localhost:8030`
- SQLAlchemy 2.0 async style throughout
- Pydantic v2 with `from_attributes = True` (not `orm_mode`)
- `python-dotenv` available but `pydantic-settings` loads `.env` via `env_file` config

## Bruno API collection
Collection at `bruno-collection/RecoTrove-API/` — uses OpenCollection YAML format (`.yml` files).

**Token flow**: run **Login** first, its post-response script auto-saves `access_token` and `refresh_token` into the environment. Requests to protected endpoints (e.g. **Get Me**) use `{{access_token}}` via bearer auth.
