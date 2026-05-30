# RecoTrove - Product Requirements Document (PRD)

**Version:** 1.0.0  
**Status:** MVP In Development  
**Last Updated:** 2026-05-30  
**Document Owner:** Development Team

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Product Vision](#product-vision)
4. [Target Audience & Personas](#target-audience--personas)
5. [Feature Roadmap](#feature-roadmap)
6. [MVP Scope (CS50 Capstone)](#mvp-scope-cs50-capstone)
7. [Phase 2 Features](#phase-2-features)
8. [Phase 3 Features (Enterprise Scale)](#phase-3-features-enterprise-scale)
9. [Non-Functional Requirements](#non-functional-requirements)
10. [Technical Architecture](#technical-architecture)
11. [Data Models](#data-models)
12. [API Design](#api-design)
13. [Security Considerations](#security-considerations)
14. [Success Metrics](#success-metrics)
15. [Risk Assessment](#risk-assessment)
16. [Future Opportunities](#future-opportunities)

---

## Executive Summary

**RecoTrove** is a social recommendation platform that enables users to share and discover quality resources (movies, books, anime, educational content, etc.) with friends, groups, or the public. Users can rate resources, write reviews, and create private rooms for curated sharing with specific circles.

The MVP focuses on core functionality: user authentication, resource creation, ratings, reviews, and private rooms with invite codes. Future phases will integrate AI-generated summaries, smart scoring, and enterprise-scale features.

**Unique Value Proposition:** Unlike traditional review platforms (Goodreads, IMDB) which are public-only, or social media which lacks structured recommendations, RecoTrove bridges the gap by offering both private group recommendations and public discovery with rich metadata and AI augmentation.

---

## Problem Statement

### Current Pain Points

| Problem | Impact |
|---------|--------|
| **Scattered recommendations** | Friends share links via WhatsApp/Discord/Twitter with no context, no rating, no organization |
| **No hybrid privacy** | Either fully public (Reddit) or fully private (DM). No middle ground for trusted groups |
| **Fragmented categories** | Books on Goodreads, Movies on IMDB, Courses on Coursera. No unified platform |
| **No AI augmentation** | Users must manually write summaries; no intelligent scoring or content analysis |
| **Review authenticity** | Public reviews suffer from spam, trolls, or fake reviews |

### Solution

RecoTrove provides:
- **Unified resource database** (any media type, user-extensible categories)
- **Dual visibility modes** (public + private rooms with invite codes)
- **AI-powered summaries and aggregate scores** (Phase 2)
- **Trust-based rating system** (room-specific + public ratings)

---

## Product Vision

**"Share what's worth your time — privately with friends, publicly with the world."**

### Guiding Principles

1. **Privacy-first:** Users control who sees their recommendations
2. **Extensible:** Categories and tags grow with user needs
3. **Intelligent:** AI enhances, not replaces, human curation
4. **Scalable:** Architecture supports millions of users from day one
5. **Developer-friendly:** Clean APIs, comprehensive docs

---

## Target Audience & Personas

### Primary Personas

| Persona | Characteristics | Needs |
|---------|----------------|-------|
| **Casual Sharer** | 25-35, active on social media, consumes varied content | Quick sharing, minimal friction, private group recommendations |
| **Curator** | 30-45, subject matter expert (book club leader, tech lead) | Organize resources by theme, manage multiple rooms, detailed metadata |
| **Discovery User** | 20-40, seeks quality recommendations before purchase | Public ratings, AI summaries, category browsing |
| **Admin** | Platform maintainer | Manage categories, flag inappropriate content, user moderation |

### Secondary Personas

| Persona | Characteristics |
|---------|----------------|
| **Content Creator** | Wants to share their own resources (courses, articles) |
| **Researcher** | Uses platform for literature reviews or media analysis |

---

## Feature Roadmap

```
Q2 2026 (MVP - CS50 Capstone)
├── User auth (email/password, JWT)
├── Resource CRUD (title, description, thumbnail, external link)
├── Categories (admin-seeded)
├── Ratings & reviews (1-10 score + text)
├── Public resource discovery
├── Private rooms with invite codes
└── Basic admin tools

Q3 2026 (Phase 2)
├── AI-generated summaries (OpenAI/HuggingFace)
├── AI aggregate scoring
├── User-suggested categories (admin approval)
├── Tags & sub-categories
├── Search & filters
└── Email notifications

Q4 2026 (Phase 3)
├── Social login (Google, GitHub)
├── Pagination & caching (Redis)
├── Rate limiting
├── Room roles (owner, member, viewer)
├── Advanced analytics
└── CI/CD pipeline (GitHub Actions → AWS/GCP)
```

---

## MVP Scope (CS50 Capstone)

### Core Features

| Feature | Description | Priority |
|---------|-------------|----------|
| **User Authentication** | Email/password registration, login, JWT tokens | P0 |
| **Role-Based Access** | User role (default) + Admin role (privileged) | P0 |
| **Category Management** | Admin creates main categories (Movies, Books, Anime, Educational) | P0 |
| **Resource Creation** | Authenticated users add: title, description, thumbnail URL, external link, category | P0 |
| **Public Resource Viewing** | Anyone can browse resources by category | P0 |
| **Ratings System** | 1-10 score rating + written review (one per user per resource) | P0 |
| **Average Rating Display** | Show average score and total review count | P0 |
| **Private Rooms** | Create room with unique invite code, add resources | P0 |
| **Room Invites** | Shareable invite code (UUID short code) | P0 |
| **Room-Specific Ratings** | Members can rate/review room resources (separate from public) | P0 |
| **Admin Seeding** | CLI script to create first admin user | P0 |
| **API Documentation** | Automatic Swagger UI (/docs) | P1 |

### Out of Scope for MVP

- Email verification
- Password reset
- Social login (Google, GitHub)
- File uploads (thumbnails hosted externally)
- Real-time notifications
- Search functionality
- Pagination (assume <500 resources for MVP)
- Mobile app (responsive web only)

### Technical Constraints

| Constraint | Limit |
|------------|-------|
| Resource title length | 255 characters |
| Description length | 5000 characters |
| Review text length | 1000 characters |
| File uploads | None (external URLs only) |
| Concurrent users | 50 (MVP scale) |
| Response time | <500ms (p95) |

---

## Phase 2 Features

### AI Integration

| Feature | Description | Technology |
|---------|-------------|------------|
| **AI Summary Generation** | Accept title + description → return enticing summary | OpenAI GPT-4 / HuggingFace BART |
| **AI Aggregate Score** | Combine user ratings + content analysis → weighted score | Custom ML model / OpenAI |
| **Content Categorization** | Suggest categories based on title/description | Zero-shot classification |
| **Sentiment Analysis** | Analyze review texts for authenticity | Transformers (RoBERTa) |

### Enhanced Social Features

| Feature | Description |
|---------|-------------|
| **Follow System** | Follow users to see their public recommendations |
| **Activity Feed** | Chronological feed of friends' activities |
| **Room Chat** | Real-time discussion within private rooms |
| **Resource Collections** | Curated lists (e.g., "Top 10 Python courses") |

### User-Generated Taxonomy

| Feature | Description |
|---------|-------------|
| **Suggested Categories** | Users propose new top-level categories (admin approves) |
| **Tags** | User-created tags (non-hierarchical, no approval) |
| **Tag Moderation** | Admin can delete inappropriate tags |

### Search & Discovery

| Feature | Description |
|---------|-------------|
| **Full-Text Search** | Search resources by title, description, tags |
| **Advanced Filters** | By rating, category, date, popularity |
| **Elasticsearch Integration** | For fast, scalable search (Phase 3 preparation) |

---

## Phase 3 Features (Enterprise Scale)

### Infrastructure & DevOps

| Feature | Description |
|---------|-------------|
| **Horizontal Scaling** | Stateless backend, multiple instances |
| **Database Sharding** | By resource_id or user_id |
| **CDN Integration** | CloudFront for thumbnails |
| **Redis Caching** | Cache popular resources, average ratings |
| **Read Replicas** | Separate DB for analytics queries |
| **Kubernetes Deployment** | For auto-scaling and rollbacks |

### Advanced Security

| Feature | Description |
|---------|-------------|
| **Rate Limiting** | Per user/IP: 100 requests/minute |
| **2-Factor Authentication** | TOTP (Google Authenticator) |
| **OAuth2 Providers** | Google, GitHub, LinkedIn |
| **Audit Logs** | Track all admin actions |
| **GDPR Compliance** | Data export, account deletion |

### Enterprise Features

| Feature | Description |
|---------|-------------|
| **Organizations** | Team accounts with shared rooms |
| **SSO** | SAML/OIDC for corporate customers |
| **API Keys** | For third-party integrations |
| **Webhooks** | Real-time notifications for resource creation |
| **Analytics Dashboard** | Usage metrics, popular resources |

---

## Non-Functional Requirements

### Performance

| Metric | Target |
|--------|--------|
| API response time (p95) | <500ms |
| Database query time | <100ms |
| Concurrent users | 1000 (Phase 2), 100,000 (Phase 3) |
| Uptime (SLA) | 99.9% (Phase 3) |

### Security

| Requirement | Implementation |
|-------------|----------------|
| Password storage | bcrypt (cost factor 12) |
| JWT expiration | 30 minutes (access), 7 days (refresh) |
| SQL injection prevention | SQLAlchemy ORM (parameterized queries) |
| XSS prevention | Input sanitization, CSP headers |
| CORS | Whitelist allowed origins only |

### Scalability

| Layer | Strategy |
|-------|----------|
| Backend | Stateless → horizontal scaling |
| Database | Connection pooling, read replicas, sharding |
| Cache | Redis for session store + query cache |
| File storage | S3/MinIO (not local disk) |

### Maintainability

| Aspect | Standard |
|--------|----------|
| Code style | PEP 8, Black formatter, mypy types |
| Documentation | OpenAPI (Swagger), inline comments |
| Testing | pytest (unit: 80% coverage, integration: critical paths) |
| CI/CD | GitHub Actions (lint, test, build, deploy) |

### Accessibility (WCAG 2.1 AA)

- Semantic HTML
- Keyboard navigation
- ARIA labels
- Color contrast ratio ≥ 4.5:1

---

## Technical Architecture

### High-Level Architecture (MVP → Enterprise)

```
[React/TypeScript Frontend - CDN]
           │
           │ HTTPS
           ▼
[Load Balancer - Nginx/ALB]
           │
           ├─── [FastAPI Backend - Multiple Instances]
           │           │
           │           ├─── [PostgreSQL - Primary + Read Replicas]
           │           ├─── [Redis - Cache + Session Store]
           │           └─── [Celery + RabbitMQ - AI Tasks]
           │
           └─── [S3/MinIO - Thumbnail Storage]
```

### Technology Stack

| Layer | MVP | Phase 2 | Phase 3 |
|-------|-----|---------|---------|
| **Backend** | FastAPI + Uvicorn | Same + Celery | Same + Kubernetes |
| **Database** | PostgreSQL 16 | Same + Read Replicas | Same + Sharding |
| **Cache** | None | Redis | Redis Cluster |
| **Storage** | External URLs | MinIO (local) | S3 / CloudFront |
| **AI** | None | OpenAI API / HuggingFace | Fine-tuned models |
| **Frontend** | React + TypeScript | Same + Tailwind | Same + PWA |
| **DevOps** | Docker Compose | Same + GitHub Actions | Kubernetes + Terraform |
| **Monitoring** | None | Prometheus + Grafana | Datadog / New Relic |

### Database Schema (Core Tables)

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Categories
CREATE TABLE categories (
    id UUID PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    is_admin_created BOOLEAN DEFAULT true,
    parent_category_id UUID REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Resources
CREATE TABLE resources (
    id UUID PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    thumbnail_url TEXT,
    external_link TEXT,
    category_id UUID REFERENCES categories(id),
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Ratings (Public)
CREATE TABLE ratings (
    id UUID PRIMARY KEY,
    resource_id UUID REFERENCES resources(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 10),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(resource_id, user_id)

-- Rooms
CREATE TABLE rooms (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id UUID REFERENCES users(id),
    invite_code VARCHAR(50) UNIQUE NOT NULL,
    is_private BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Room Members
CREATE TABLE room_members (
    room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (room_id, user_id)
);

-- Room Resources
CREATE TABLE room_resources (
    room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
    resource_id UUID REFERENCES resources(id) ON DELETE CASCADE,
    added_by UUID REFERENCES users(id),
    added_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (room_id, resource_id)
);

-- Room Ratings (separate from public ratings)
CREATE TABLE room_ratings (
    id UUID PRIMARY KEY,
    room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
    resource_id UUID REFERENCES resources(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 10),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(room_id, resource_id, user_id)
);

-- Indexes for Performance
CREATE INDEX idx_resources_category ON resources(category_id);
CREATE INDEX idx_resources_created_at ON resources(created_at DESC);
CREATE INDEX idx_ratings_resource ON ratings(resource_id);
CREATE INDEX idx_ratings_user ON ratings(user_id);
CREATE INDEX idx_room_members_user ON room_members(user_id);
CREATE INDEX idx_room_resources_room ON room_resources(room_id);
```

---

## API Design

### RESTful Principles

| Convention | Example |
|------------|---------|
| Nouns for resources | `/resources`, `/categories` |
| HTTP methods | GET, POST, PUT, DELETE |
| Status codes | 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found |
| Versioning | `/api/v1/` prefix |
| Pagination | `?limit=20&offset=40` (Phase 2) |

### Core Endpoints (MVP)

#### Authentication
```
POST   /api/v1/auth/register      - Register new user
POST   /api/v1/auth/login         - Login (returns JWT)
POST   /api/v1/auth/refresh       - Refresh access token
GET    /api/v1/auth/me            - Get current user
```

#### Categories
```
GET    /api/v1/categories         - List all categories
GET    /api/v1/categories/{id}    - Get single category
POST   /api/v1/categories         - Create category (admin only)
PUT    /api/v1/categories/{id}    - Update category (admin only)
DELETE /api/v1/categories/{id}    - Delete category (admin only)
```

#### Resources
```
GET    /api/v1/resources          - List resources (filter by category)
GET    /api/v1/resources/{id}     - Get single resource
POST   /api/v1/resources          - Create resource (auth required)
PUT    /api/v1/resources/{id}     - Update resource (owner only)
DELETE /api/v1/resources/{id}     - Delete resource (owner only)
```

#### Ratings
```
GET    /api/v1/resources/{id}/ratings     - Get all public ratings
POST   /api/v1/resources/{id}/ratings     - Add/update rating (auth)
GET    /api/v1/resources/{id}/average     - Get average rating
```

#### Rooms
```
GET    /api/v1/rooms               - List user's rooms
POST   /api/v1/rooms               - Create room (auth required)
GET    /api/v1/rooms/{id}          - Get room details
PUT    /api/v1/rooms/{id}          - Update room (owner only)
DELETE /api/v1/rooms/{id}          - Delete room (owner only)
POST   /api/v1/rooms/{id}/join     - Join room with invite code
GET    /api/v1/rooms/{id}/resources - List resources in room
POST   /api/v1/rooms/{id}/resources - Add resource to room
GET    /api/v1/rooms/{id}/ratings/{resource_id} - Get room ratings
POST   /api/v1/rooms/{id}/ratings/{resource_id} - Rate resource in room
```

### Request/Response Examples

**POST /api/v1/resources**
```json
// Request
{
  "title": "Clean Code",
  "description": "A handbook of agile software craftsmanship",
  "thumbnail_url": "https://example.com/cleancode.jpg",
  "external_link": "https://amazon.com/dp/0132350882",
  "category_id": "123e4567-e89b-12d3-a456-426614174000"
}

// Response (201 Created)
{
  "id": "123e4567-e89b-12d3-a456-426614174001",
  "title": "Clean Code",
  "description": "A handbook of agile software craftsmanship",
  "thumbnail_url": "https://example.com/cleancode.jpg",
  "external_link": "https://amazon.com/dp/0132350882",
  "category": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Educational"
  },
  "created_by": {
    "id": "user-123",
    "full_name": "Alice Wonderland"
  },
  "average_rating": 0.0,
  "total_ratings": 0,
  "created_at": "2026-05-30T12:00:00Z"
}
```

---

## Security Considerations

### Authentication & Authorization

| Layer | Implementation |
|-------|----------------|
| **Password storage** | bcrypt with salt (12 rounds) |
| **JWT tokens** | HS256, expires in 30 minutes |
| **Refresh tokens** | Stored in httpOnly cookie or client memory |
| **Rate limiting** | 100 requests/minute per user (Phase 2) |
| **Brute force protection** | Login attempts: 5 failures → 15 minute lockout |

### Data Protection

| Risk | Mitigation |
|------|------------|
| **SQL injection** | SQLAlchemy ORM (no raw queries) |
| **XSS** | Input sanitization, output encoding, CSP |
| **CSRF** | SameSite cookies, CSRF tokens for state-changing ops |
| **Data leakage** | Never log passwords or tokens, redact PII in logs |
| **Man-in-the-middle** | Enforce HTTPS in production (HSTS) |

### External Links Security

**Policy:**
- Only allow `https://` URLs (reject `http://` for external links)
- Reject `javascript:`, `data:`, `file:` protocols
- Add `rel="noopener noreferrer"` to all external links
- No automatic fetching or embedding of external content

**Rationale:** External links are safe when treated as plain text. The risk is zero if you never execute or fetch the URL content.

### Admin Access

- Admin role seeded via CLI script (not via API)
- Admin actions logged (audit trail in Phase 2)
- Additional 2FA for admin accounts (Phase 3)

---

## Success Metrics

### MVP Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| User registration | 50+ during testing | Database count |
| Resources created | 100+ during testing | Database count |
| API response time | <500ms p95 | Uvicorn logs |
| Zero security breaches | 0 incidents | Manual review |

### Phase 2 Success Criteria

| Metric | Target |
|--------|--------|
| Daily Active Users (DAU) | 500 |
| Resources per user | 5+ |
| AI summary usage | 80% of new resources |
| User retention (30 days) | 40% |

### Phase 3 Success Criteria

| Metric | Target |
|--------|--------|
| DAU | 10,000 |
| Concurrent users | 1,000 |
| Uptime | 99.9% |
| Average session duration | 10 minutes |
| Room creation rate | 100/day |

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **PostgreSQL performance degradation** | Medium | High | Connection pooling, read replicas, caching |
| **JWT token theft** | Low | High | Short expiry, refresh tokens, httpOnly cookies |
| **Docker resource exhaustion** | Medium | Medium | Resource limits in docker-compose |
| **AI API rate limiting** | High (Phase 2) | Medium | Queue with Celery, retry logic, fallback |
| **Database migration conflicts** | Low | Medium | Alembic version control, test migrations |

### Business Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Low user adoption** | Medium | High | Focus on UX, simple onboarding, seed data |
| **Spam/low-quality resources** | High | Medium | Admin moderation, user flagging (Phase 2) |
| **Category explosion** | Medium | Low | Admin-only top-level categories, user tags for flexibility |

---

## Future Opportunities

### Immediate Post-MVP (3-6 months)

1. **Browser Extension** - One-click save resources from any website
2. **Import from Goodreads/IMDB** - CSV upload or API integration
3. **Weekly Digest Email** - Popular resources in user's categories
4. **Mobile App** - React Native or Flutter

### Long-term (6-12 months)

1. **Affiliate Links** - Monetize through Amazon, Udemy, etc. (optional for users)
2. **Public API** - Allow third-party apps to read/write resources
3. **Recommendation Engine** - Collaborative filtering ("Users who liked X also liked Y")
4. **Decentralized Identity** - Self-sovereign identity for power users
5. **Blockchain Badges** - NFT-style achievement badges for top curators

### Research Opportunities

- **Federated Learning** - Train recommendation models without centralizing user data
- **Zero-Knowledge Proofs** - Verify user reputation without revealing identity
- **ActivityPub Integration** - Federate with Mastodon/Lemmy (Fediverse)

---

## Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Resource** | Any recommendable item (movie, book, course, etc.) |
| **Room** | Private space for sharing resources with invite-only members |
| **Tag** | User-generated keyword for categorization (non-hierarchical) |
| **JWT** | JSON Web Token - stateless authentication token |
| **ASGI** | Asynchronous Server Gateway Interface (FastAPI uses this) |

### Appendix B: References

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org)
- [OWASP Top Ten Security Risks](https://owasp.org/www-project-top-ten/)
- [Bruno API Client](https://www.usebruno.com)

### Appendix C: Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1.0 | 2026-05-25 | Initial draft | Development Team |
| 0.2.0 | 2026-05-28 | Added DB schema, API design | Development Team |
| 1.0.0 | 2026-05-30 | MVP scope finalized, security review | Development Team |

---

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Owner | [TBD] | 2026-05-30 | Approved |
| Tech Lead | [TBD] | 2026-05-30 | Approved |
| Security Lead | [TBD] | 2026-05-30 | Approved |

---

**Next Steps:**
1. ✅ PRD approved
2. ⬜ Sprint 0-1 complete (Auth + DB)
3. ⬜ Sprint 2 (Categories + Resources)
4. ⬜ Sprint 3 (Ratings + Reviews)
5. ⬜ Sprint 4 (Private Rooms)
6. ⬜ Sprint 5 (Frontend Integration)
7. ⬜ Sprint 6 (AI Features)
8. ⬜ Sprint 7 (Production Deployment)
9. ⬜ CS50 Capstone Submission

---

*End of PRD*
