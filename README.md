# RecoTrove

#### Video Demo: <URL HERE>

#### Description:

RecoTrove is a full-stack web application for cataloging, rating, and sharing personal recommendations. Users can create curated collections of books, movies, TV shows, courses, and other media — each tagged and categorized — and share them with friends through private rooms with invite codes. Think of it as a personal recommendation engine where you track what you love, rate it on a 1-10 scale, organize it into categories, and share access with trusted circles.

The project was built as my CS50x final project to demonstrate full-stack development with FastAPI (Python) on the backend, React with TypeScript on the frontend, and PostgreSQL for persistence. It runs locally with Docker Compose for the database and backend server, while the frontend uses Vite for hot-reload development.

#### Backend Architecture

The backend is organized into a layered architecture in the `backend/app/` directory:

**`main.py`** — The FastAPI application entry point. It configures CORS middleware, registers all API routers under the `/api/v1` prefix, and defines a lifespan handler that auto-creates database tables on startup and seeds the initial admin user.

**`core/config.py`** — Application settings using Pydantic Settings with nested model support. The `AppSettings` class contains `DatabaseSettings` and `SecuritySettings` as sub-models, loaded from environment variables with `env_nested_delimiter = "__"`. This means the database URL is set via `database__DATABASE_URL` rather than a flat `DATABASE_URL` — a deliberate design choice to keep settings organized and to resolve conflicts between Docker environment variables and the mounted `.env` file.

**`core/database.py`** — Database engine and session configuration using SQLAlchemy 2.0's async engine with psycopg (the modern async PostgreSQL driver). The `get_db` dependency yields an async session that services use for all database operations.

**`core/security.py`** — Password hashing with bcrypt and JWT token management using python-jose. Access tokens expire after 30 minutes; refresh tokens expire after 7 days. Passwords are hashed with passlib's bcrypt context (pinned to bcrypt 4.0.1 for compatibility).

**`core/seeding.py`** — A reusable `seed_admin` function that checks if an admin user exists and creates one from `FIRST_ADMIN_*` settings if not. Called automatically on every app startup via the lifespan handler.

**`models/`** — SQLAlchemy ORM models. `user.py` defines the User model with UUID primary key, unique email index, and role field (user/admin). `category.py` implements a hierarchical taxonomy with a self-referential `parent_category_id` foreign key, enabling nested categories. `resource.py` models the recommendation items with a many-to-many relationship to tags via the `resource_tags` association table. `rating.py` stores user ratings (1-10 scale) with a unique constraint on `(user_id, resource_id)` so each user can only rate a resource once. `room.py` implements the private room system with `Room`, `RoomMember`, `RoomResource`, and `RoomRating` models — representing the shared spaces where users collaborate on recommendations.

**`schemas/`** — Pydantic v2 schemas using `from_attributes = True` for ORM compatibility. Each schema corresponds to a model and defines request/response shapes for the API. The resource schemas include `ResourceCreate`, `ResourceUpdate`, and `ResourceListResponse` (which enriches resources with computed rating aggregates). Similarly, tag schemas define `TagCreate` and `TagResponse`.

**`services/`** — The business logic layer. Each service class contains static async methods that encapsulate database operations. `ResourceService` handles listing, creating, updating, deleting resources, and searching by title. `CategoryService` manages the hierarchical category tree with parent-child relationships. `RatingService` provides upsert behavior (create or update a rating, never duplicate). `RoomService` handles room CRUD, membership (join/leave via invite codes), and room-scoped resource operations.

**`api/v1/endpoints/`** — Route handlers are thin wrappers that parse path/query parameters, call the appropriate service method, and return the response. `auth.py` handles registration, login (using `OAuth2PasswordRequestForm` with email as the username), token refresh, and user profile retrieval. The protected endpoints use a dependency chain: `get_current_user` → `get_current_active_user` → `get_current_admin_user`.

**`seed_admin.py`** — Standalone script to create the initial admin user, usable directly or via Docker Compose exec.

#### Frontend Architecture

The frontend lives in `frontend/` and is built with React 19, TypeScript, Vite, and Tailwind CSS.

**`src/context/auth-context.tsx`** — Authentication context that manages JWT token state, auto-fetches user profile on mount if a token exists, and provides login/logout functions to the entire component tree.

**`src/components/`** — Reusable UI components. `navbar.tsx` displays navigation links and auth status. `resource-card.tsx` renders individual resource previews with title, description, thumbnail, tags, and average rating. `rating-modal.tsx` provides the star-based rating interface. `add-resource-modal.tsx` lets users search and add resources to rooms. `theme-toggle.tsx` switches between light and dark modes.

**`src/pages/`** — Page components mapped to routes. `resources.tsx` lists all resources with loading/error states, fetched via React Query's `useQuery`. `login.tsx` handles form submission with application/x-www-form-urlencoded encoding (matching FastAPI's OAuth2 expectations). `register.tsx` creates new user accounts. `rooms.tsx` lists rooms the current user belongs to. `room-detail.tsx` shows a room's resources and members. `new-resource.tsx` and `new-room.tsx` provide creation forms.

**`vite.config.ts`** — Configured with a dev proxy that forwards `/api` requests to `http://localhost:8030`, avoiding CORS issues during development.

#### Design Decisions

One of the key design decisions was the layered service architecture. Rather than putting business logic directly in route handlers (which would make testing and reuse difficult), I extracted all database operations into service classes. Route handlers become simple adapters that parse HTTP input, call a service, and return HTTP output. This separation made it easy to add features like tag management without touching route code.

The settings structure using nested models and `env_nested_delimiter` was driven by a real problem: the Docker Compose file sets environment variables that override the `.env` file mounted into the container. By using `database__DATABASE_URL` instead of `DATABASE_URL`, Pydantic Settings correctly populates the nested `settings.database.DATABASE_URL` field, and Docker's OS-level environment variables take precedence over the `.env` file values.

The `list` method naming conflict was an instructive Python gotcha. Because all service methods are `@staticmethod` inside a class, naming a method `list` caused it to shadow the built-in `list` type within the class namespace. When Python later evaluated `list[str]` type annotations in other method signatures, it tried to subscript the `staticmethod` descriptor object instead of the built-in type, raising `TypeError: 'staticmethod' object is not subscriptable`. Renaming the methods to `get_all` resolved the shadowing.

#### How to Run

Prerequisites: Docker, Docker Compose, Node.js 20+.

```bash
docker-compose up -d                    # Start PostgreSQL and backend
cd frontend && npm install && npm run dev  # Start the frontend
cp frontend/.env.local.example frontend/.env.local  # If needed
```

The API will be available at `http://localhost:8030`, the frontend at `http://localhost:5173`, and interactive API docs at `http://localhost:8030/docs`.
