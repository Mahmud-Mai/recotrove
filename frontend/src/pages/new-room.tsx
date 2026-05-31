import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import axios from "axios"
import { useAuth } from "../context/auth-context"
import { ArrowLeft, Loader2, AlertCircle, Users, Layout } from "lucide-react"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8030/api/v1"

export default function NewRoomPage() {
  const { token } = useAuth()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [error, setError] = useState<string | null>(null)

  const mutation = useMutation({
    mutationFn: async (newRoom: { name: string; description?: string }) => {
      const response = await axios.post(`${API_URL}/rooms`, newRoom, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ["rooms"] })
      // Navigate to the room detail or back to dashboard
      navigate(`/rooms/${data.id}`)
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || "Failed to create room. Please try again.")
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    
    mutation.mutate({
      name,
      description: description || undefined
    })
  }

  return (
    <div className="max-w-2xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-4">
        <button 
          onClick={() => navigate(-1)}
          className="p-2 rounded-full hover:bg-accent transition-colors text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft size={20} />
        </button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Create Circle</h1>
          <p className="text-muted-foreground">Start a private space for your trusted recommendations.</p>
        </div>
      </div>

      <div className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-sm p-8 shadow-sm">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2" htmlFor="name">
              <Users size={14} className="text-muted-foreground" />
              Circle Name
            </label>
            <input
              id="name"
              placeholder="e.g., Book Club, Tech Leads, Family Hub"
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2" htmlFor="description">
              <Layout size={14} className="text-muted-foreground" />
              Description (Optional)
            </label>
            <textarea
              id="description"
              placeholder="What is this circle for?"
              className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 resize-y"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          {error && (
            <div className="flex items-center gap-2 text-sm text-destructive bg-destructive/10 p-4 rounded-md border border-destructive/20">
              <AlertCircle size={16} />
              <span>{error}</span>
            </div>
          )}

          <div className="flex gap-4 pt-4">
            <button
              type="button"
              onClick={() => navigate(-1)}
              className="flex-1 inline-flex items-center justify-center rounded-md border border-border px-4 py-2 text-sm font-medium hover:bg-accent transition-colors"
              disabled={mutation.isPending}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="flex-1 inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
              disabled={mutation.isPending}
            >
              {mutation.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Create Circle
            </button>
          </div>
        </form>
      </div>

      <div className="p-6 rounded-xl border border-indigo-500/20 bg-indigo-500/5">
        <h4 className="text-sm font-semibold text-indigo-500 mb-1">Privacy Guarantee</h4>
        <p className="text-xs text-indigo-500/70 leading-relaxed">
          Circles are private by default. Only members with your unique invite code can view or contribute to this space.
        </p>
      </div>
    </div>
  )
}
