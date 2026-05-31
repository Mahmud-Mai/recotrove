import { ThemeProvider } from "./components/theme-provider"
import { AuthProvider } from "./context/auth-context"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom"
import { AppLayout } from "./components/app-layout"
import LoginPage from "./pages/login"
import RegisterPage from "./pages/register"
import ResourcesPage from "./pages/resources"
import NewResourcePage from "./pages/new-resource"
import RoomsPage from "./pages/rooms"
import NewRoomPage from "./pages/new-room"
import JoinRoomPage from "./pages/join-room"
import RoomDetailPage from "./pages/room-detail"

const queryClient = new QueryClient()

function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-20rem)] text-center py-12">
      <div className="space-y-4 max-w-3xl">
        <h1 className="text-4xl font-bold tracking-tight sm:text-7xl">
          Share what's worth your time
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          The elite social recommendation platform. Curate resources, rate with precision, and share privately in trusted circles.
        </p>
        <div className="flex gap-4 justify-center pt-8">
          <Link 
            to="/register" 
            className="px-8 py-3 bg-primary text-primary-foreground rounded-full font-medium shadow-lg hover:shadow-primary/20 transition-all hover:-translate-y-0.5"
          >
            Start Curating
          </Link>
          <Link 
            to="/resources" 
            className="px-8 py-3 border border-border rounded-full font-medium hover:bg-accent transition-colors"
          >
            Explore Publicly
          </Link>
        </div>
      </div>

      <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl">
        {[
          { title: "Universal Resources", desc: "Books, movies, courses, or any link. One platform for everything." },
          { title: "Private Rooms", desc: "Create invite-only spaces for your book club, team, or inner circle." },
          { title: "Trusted Ratings", desc: "Dual-layer ratings: public consensus and private room-specific reviews." }
        ].map((feat, i) => (
          <div key={i} className="p-8 rounded-2xl border border-border/50 bg-card/50 backdrop-blur-sm text-left hover:border-border transition-colors">
            <h3 className="text-lg font-semibold mb-2">{feat.title}</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">{feat.desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider defaultTheme="system" storageKey="recotrove-ui-theme">
        <AuthProvider>
          <Router>
            <AppLayout>
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/resources" element={<ResourcesPage />} />
                <Route path="/resources/new" element={<NewResourcePage />} />
                <Route path="/rooms" element={<RoomsPage />} />
                <Route path="/rooms/new" element={<NewRoomPage />} />
                <Route path="/rooms/join" element={<JoinRoomPage />} />
                <Route path="/rooms/:id" element={<RoomDetailPage />} />
              </Routes>
            </AppLayout>
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

export default App
