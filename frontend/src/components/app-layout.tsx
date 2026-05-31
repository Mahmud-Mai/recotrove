import { ReactNode } from "react"
import { Navbar } from "./navbar"

interface AppLayoutProps {
  children: ReactNode
}

export function AppLayout({ children }: AppLayoutProps) {
  return (
    <div className="relative flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <div className="container px-4 py-8 md:px-8">
          {children}
        </div>
      </main>
      <footer className="border-t border-border/40 py-6 md:px-8 md:py-0">
        <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
          <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
            Built for elite curation. © 2026 RecoTrove.
          </p>
        </div>
      </footer>
    </div>
  )
}
