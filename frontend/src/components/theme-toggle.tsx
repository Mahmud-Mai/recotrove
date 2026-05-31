import { Sun, Moon, Laptop, User, LogOut } from "lucide-react"
import { useTheme } from "./theme-provider"
import { cn } from "../lib/utils"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <div className="flex items-center gap-1 bg-muted/50 p-1 rounded-full border border-border/50">
      <button
        onClick={() => setTheme("light")}
        className={cn(
          "p-1.5 rounded-full transition-all",
          theme === "light" ? "bg-background shadow-sm text-foreground" : "text-muted-foreground hover:text-foreground"
        )}
      >
        <Sun size={16} />
      </button>
      <button
        onClick={() => setTheme("dark")}
        className={cn(
          "p-1.5 rounded-full transition-all",
          theme === "dark" ? "bg-background shadow-sm text-foreground" : "text-muted-foreground hover:text-foreground"
        )}
      >
        <Moon size={16} />
      </button>
      <button
        onClick={() => setTheme("system")}
        className={cn(
          "p-1.5 rounded-full transition-all",
          theme === "system" ? "bg-background shadow-sm text-foreground" : "text-muted-foreground hover:text-foreground"
        )}
      >
        <Laptop size={16} />
      </button>
    </div>
  )
}
