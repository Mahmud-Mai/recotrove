import { useState } from "react"
import { Modal } from "./modal"
import { Search, Loader2, Plus, AlertCircle, ExternalLink } from "lucide-react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import axios from "axios"
import { useAuth } from "../context/auth-context"
import type { Resource } from "./resource-card"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8030/api/v1"

interface AddResourceModalProps {
  isOpen: boolean
  onClose: () => void
  roomId: string
}

export function AddResourceModal({ isOpen, onClose, roomId }: AddResourceModalProps) {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  const [search, setSearch] = useState("")
  const [error, setError] = useState<string | null>(null)

  const { data: searchResults, isLoading: isSearching } = useQuery<Resource[]>({
    queryKey: ["resource-search", search],
    queryFn: async () => {
      if (!search || search.length < 2) return []
      const response = await axios.get(`${API_URL}/resources/search?q=${search}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    enabled: search.length >= 2
  })

  const addMutation = useMutation({
    mutationFn: async (resourceId: string) => {
      const response = await axios.post(
        `${API_URL}/rooms/${roomId}/resources`,
        { resource_id: resourceId },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["room-resources", roomId] })
      onClose()
      setSearch("")
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || "Failed to add resource to circle.")
    }
  })

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Add to Circle" className="max-w-2xl">
      <div className="space-y-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            placeholder="Search existing resources by title..."
            className="flex h-12 w-full rounded-xl border border-input bg-background pl-10 pr-4 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            autoFocus
          />
        </div>

        <div className="min-h-[300px] max-h-[400px] overflow-y-auto pr-2 space-y-2">
          {isSearching ? (
            <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
              <Loader2 className="h-8 w-8 animate-spin mb-2" />
              <p className="text-sm">Searching the trove...</p>
            </div>
          ) : search.length < 2 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-sm text-muted-foreground">Type at least 2 characters to search.</p>
            </div>
          ) : searchResults?.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-sm text-muted-foreground mb-4">No resources found matching "{search}"</p>
              <a 
                href={`/resources/new?roomId=${roomId}`} 
                className="text-sm font-medium text-primary hover:underline"
              >
                Create a new one instead →
              </a>
            </div>
          ) : (
            searchResults?.map((res) => (
              <div 
                key={res.id}
                className="group flex items-center justify-between p-4 rounded-xl border border-border/50 bg-card/50 hover:border-border hover:bg-accent/50 transition-all"
              >
                <div className="flex-1 min-w-0 pr-4">
                  <h4 className="font-semibold text-sm truncate">{res.title}</h4>
                  <p className="text-xs text-muted-foreground line-clamp-1">{res.description || "No description"}</p>
                </div>
                <button
                  onClick={() => addMutation.mutate(res.id)}
                  disabled={addMutation.isPending}
                  className="inline-flex items-center justify-center rounded-lg bg-primary/10 px-3 py-1.5 text-xs font-bold text-primary hover:bg-primary hover:text-primary-foreground transition-all disabled:opacity-50"
                >
                  {addMutation.isPending ? <Loader2 className="h-3 w-3 animate-spin" /> : <Plus className="h-3 w-3 mr-1" />}
                  Add
                </button>
              </div>
            ))
          )}
        </div>

        {error && (
          <div className="flex items-center gap-2 text-sm text-destructive bg-destructive/10 p-3 rounded-md border border-destructive/20">
            <AlertCircle size={14} />
            <span>{error}</span>
          </div>
        )}

        <div className="pt-4 border-t border-border/40 flex items-center justify-between text-xs">
          <p className="text-muted-foreground italic">Can't find it?</p>
          <a 
            href={`/resources/new?roomId=${roomId}`} 
            className="inline-flex items-center gap-1 font-semibold text-primary hover:underline"
          >
            Create New Resource
            <ExternalLink size={12} />
          </a>
        </div>
      </div>
    </Modal>
  )
}
