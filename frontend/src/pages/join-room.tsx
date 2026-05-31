import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import axios from "axios"
import { useAuth } from "../context/auth-context"
import { Loader2, AlertCircle, Hash, ShieldCheck } from "lucide-react"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8030/api/v1"

export default function JoinRoomPage() {
  const { token } = useAuth()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  
  const [inviteCode, setInviteCode] = useState("")
  const [error, setError] = useState<string | null>(null)

  const mutation = useMutation({
    mutationFn: async (code: string) => {
      const response = await axios.post(`${API_URL}/rooms/join`, { invite_code: code }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["rooms"] })
      navigate(`/rooms/${data.id || data.room_id || ""}`)
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || "Invalid invite code or already a member.")
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    
    if (!inviteCode.trim()) {
      setError("Please enter an invite code")
      return
    }

    mutation.mutate(inviteCode.trim())
  }

  return (
    <div className="max-w-md mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500 py-12">
      <div className="text-center space-y-2">
        <div className="inline-flex items-center justify-center p-3 rounded-full bg-primary/10 text-primary mb-4">
          <ShieldCheck size={32} />
        </div>
        <h1 className="text-3xl font-bold tracking-tight">Join a Circle</h1>
        <p className="text-muted-foreground">Enter a unique invite code to access a private room.</p>
      </div>

      <div className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-sm p-8 shadow-lg">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2" htmlFor="inviteCode">
              <Hash size={14} className="text-muted-foreground" />
              Invite Code
            </label>
            <input
              id="inviteCode"
              placeholder="e.g., ROOM-1234-ABCD"
              className="flex h-12 w-full rounded-md border border-input bg-background px-4 py-2 text-center text-lg font-mono tracking-widest ring-offset-background placeholder:text-muted-foreground placeholder:font-sans placeholder:tracking-normal focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50"
              value={inviteCode}
              onChange={(e) => setInviteCode(e.target.value)}
              required
              autoFocus
            />
          </div>

          {error && (
            <div className="flex items-center gap-2 text-sm text-destructive bg-destructive/10 p-4 rounded-md border border-destructive/20">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          <div className="flex flex-col gap-3">
            <button
              type="submit"
              className="w-full inline-flex items-center justify-center rounded-md bg-primary px-4 py-3 text-sm font-medium text-primary-foreground shadow-lg hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 transition-all active:scale-[0.98]"
              disabled={mutation.isPending}
            >
              {mutation.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Join Circle
            </button>
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="w-full inline-flex items-center justify-center rounded-md border border-border px-4 py-2 text-sm font-medium hover:bg-accent transition-colors"
            >
              Go Back
            </button>
          </div>
        </form>
      </div>

      <p className="text-center text-xs text-muted-foreground px-8">
        By joining a circle, your curations and ratings will be visible to other members of that room.
      </p>
    </div>
  )
}
