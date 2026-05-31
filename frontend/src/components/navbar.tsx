import { Link } from "react-router-dom"
import { useAuth } from "../context/auth-context"
import { ThemeToggle } from "./theme-toggle"

export function Navbar() {
  const { user, logout } = useAuth()

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-4 md:px-8">
        <div className="flex items-center gap-8">
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
              RecoTrove
            </span>
          </Link>
          <div className="hidden md:flex items-center gap-6">
            <Link to="/resources" className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground">
              Resources
            </Link>
            <Link to="/rooms" className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground">
              Rooms
            </Link>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <ThemeToggle />
          
          <div className="h-6 w-[1px] bg-border/50 mx-1 hidden sm:block" />

          {user ? (
            <div className="flex items-center gap-4">
              <Link to="/profile" className="hidden sm:block text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                {user.full_name}
              </Link>
              <button 
                onClick={logout}
                className="text-sm font-medium text-muted-foreground hover:text-destructive transition-colors"
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2 sm:gap-4">
              <Link to="/login" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                Login
              </Link>
              <Link to="/register" className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring">
                Register
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}
