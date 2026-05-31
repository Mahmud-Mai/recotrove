import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import { useAuth } from "../context/auth-context"
import { Loader2, Plus, Shield, ArrowRight, Copy, Check, Users } from "lucide-react"
import { Link } from "react-router-dom"
import { useState } from "react"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8030/api/v1"

interface Room {
  id: string
  name: string
  description?: string
  owner_id: string
  invite_code: string
  created_at: string
}

export default function RoomsPage() {
  const { token, user } = useAuth()
  const [copiedId, setCopiedId] = useState<string | null>(null)

  const { data: rooms, isLoading } = useQuery<Room[]>({
    queryKey: ["rooms"],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/rooms`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    enabled: !!token
  })

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  if (isLoading) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    )
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Your Circles</h1>
          <p className="text-muted-foreground">
            Manage your private sharing spaces and trusted communities.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Link 
            to="/rooms/join" 
            className="inline-flex items-center justify-center rounded-md border border-border px-4 py-2 text-sm font-medium hover:bg-accent transition-colors"
          >
            Join with Code
          </Link>
          <Link 
            to="/rooms/new" 
            className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90"
          >
            <Plus className="mr-2 h-4 w-4" />
            Create Circle
          </Link>
        </div>
      </div>

      {!rooms || rooms.length === 0 ? (
        <div className="flex min-h-[300px] flex-col items-center justify-center rounded-2xl border border-dashed border-border/60 bg-muted/30 text-center p-12">
          <div className="bg-background p-4 rounded-full shadow-sm mb-4">
            <Users className="h-6 w-6 text-muted-foreground" />
          </div>
          <h2 className="text-xl font-semibold mb-2">No circles yet</h2>
          <p className="text-muted-foreground max-w-sm mb-6">
            Private rooms are where the best curations happen. Create one for your team or inner circle.
          </p>
          <Link 
            to="/rooms/new" 
            className="inline-flex items-center justify-center rounded-md bg-primary px-6 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90"
          >
            Start your first circle
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {rooms.map((room) => (
            <div 
              key={room.id}
              className="group relative flex flex-col rounded-xl border border-border/50 bg-card/50 backdrop-blur-sm p-6 transition-all hover:border-border hover:shadow-md"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="bg-indigo-500/10 p-2 rounded-lg text-indigo-500">
                  <Shield size={20} />
                </div>
                {room.owner_id === user?.id && (
                  <span className="text-[10px] font-bold uppercase tracking-wider bg-primary/10 text-primary px-2 py-0.5 rounded-full">
                    Owner
                  </span>
                )}
              </div>

              <h3 className="text-lg font-semibold mb-1 group-hover:text-primary transition-colors">
                {room.name}
              </h3>
              
              {room.description ? (
                <p className="text-sm text-muted-foreground line-clamp-2 mb-6 flex-1">
                  {room.description}
                </p>
              ) : (
                <p className="text-sm text-muted-foreground italic mb-6 flex-1">
                  No description provided.
                </p>
              )}

              <div className="flex flex-col gap-3 mt-auto">
                <div className="flex items-center justify-between p-2 rounded-md bg-muted/50 border border-border/40">
                  <code className="text-xs font-mono text-muted-foreground">
                    {room.invite_code}
                  </code>
                  <button 
                    onClick={() => copyToClipboard(room.invite_code, room.id)}
                    className="text-muted-foreground hover:text-foreground transition-colors"
                    title="Copy invite code"
                  >
                    {copiedId === room.id ? <Check size={14} className="text-green-500" /> : <Copy size={14} />}
                  </button>
                </div>
                
                <Link 
                  to={`/rooms/${room.id}`}
                  className="inline-flex items-center justify-center gap-2 w-full py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium hover:bg-secondary/80 transition-colors"
                >
                  Enter Circle
                  <ArrowRight size={14} />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
