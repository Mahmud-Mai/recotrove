# RecoTrove — Foundational Mandates

This file defines the core technical standards, architectural patterns, and design tokens for the RecoTrove project. These mandates take precedence over general defaults.

## 1. Security & Integrity
- **JWT Handling**: Store access tokens in memory (AuthContext); use `httpOnly` cookies for refresh tokens if possible, or secure local storage for MVP.
- **External Links**: All external resource links must have `rel="noopener noreferrer"`.
- **Environment**: Never commit `.env` files. Use `VITE_` prefix for frontend environment variables.

## 2. Technical Stack
- **Frontend**: React 18+ (TypeScript), Vite, Tailwind CSS.
- **State Management**: React Context for Auth; TanStack Query (React Query) for server state.
- **Icons**: Lucide React.
- **Backend**: FastAPI (already established, see `AGENTS.md`).

## 3. "Elite" Design System (Tailwind Tokens)
To maintain a matured, minimalistic, and elite aesthetic:
- **Colors**:
  - **Primary**: Indigo (600/500) for accents.
  - **Neutrals**: Zinc or Slate (Zinc 950 for deep dark mode, Zinc 50 for light mode backgrounds).
  - **Borders**: Zinc-200 (light) / Zinc-800 (dark).
- **Typography**:
  - Font: Inter or Geist (Sans-serif).
  - Headers: Tight tracking (`tracking-tight`), semi-bold.
- **Spacing**: Generous whitespace (minimum `p-4`, prefer `p-6` or `p-8` for sections).
- **Subtlety**: Use `shadow-sm` or `shadow-md` with low opacity. Avoid heavy gradients. Use glassmorphism (`backdrop-blur`) for Navbars.

## 4. Development Workflow
- **Surgical Edits**: Prefer `replace` tool for precise modifications.
- **Testing**: Add unit tests for utility functions and integration tests for critical user flows (Login, Room Creation).
- **Reference**: Consult `AGENTS.md` for backend API structure and port mapping (8030).

---
*Note: This file is a living document and should be updated as architectural decisions evolve.*
