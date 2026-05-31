import { useQuery } from "@tanstack/react-query"
import { useParams, useNavigate } from "react-router-dom"
import axios from "axios"
import { useAuth } from "../context/auth-context"
import { ResourceCard } from "../components/resource-card"
import type { Resource } from "../components/resource-card"
import { RatingModal } from "../components/rating-modal"
import { AddResourceModal } from "../components/add-resource-modal"
import { Loader2, Plus, Users, Shield, Copy, Check, MoreVertical, MessageSquare } from "lucide-react"
import { useState } from "react"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8030/api/v1"

interface Room {
  id: string
  name: string
  description?: string
  owner_id: string
  invite_code: string
  created_at: string
  member_count: number
}

interface RoomResource {
  room_id: string
  resource_id: string
  added_by: string
  added_at: string
  resource: Resource
}

export default function RoomDetailPage() {
  const { id } = useParams()
  const { token } = useAuth()
  const navigate = useNavigate()
  const [copied, setCopied] = useState(false)
  
  // Modal states
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)
  const [ratingResource, setRatingResource] = useState<{ id: string, title: string } | null>(null)

  const { data: room, isLoading: isLoadingRoom } = useQuery<Room>({
    queryKey: ["room", id],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/rooms/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    enabled: !!token && !!id
  })

  const { data: roomResources, isLoading: isLoadingResources } = useQuery<RoomResource[]>({
    queryKey: ["room-resources", id],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/rooms/${id}/resources`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    enabled: !!token && !!id
  })

  const copyInvite = () => {
    if (room?.invite_code) {
      navigator.clipboard.writeText(room.invite_code)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  if (isLoadingRoom) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    )
  }

  if (!room) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <h2 className="text-2xl font-bold mb-2">Circle not found</h2>
        <p className="text-muted-foreground mb-8">It might have been deleted or you don't have access.</p>
        <button onClick={() => navigate("/rooms")} className="px-4 py-2 bg-primary text-primary-foreground rounded-md font-medium">
          Back to Circles
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-10 animate-in fade-in duration-700">
      {/* Room Header */}
      <div className="relative overflow-hidden rounded-3xl border border-border/50 bg-card/30 backdrop-blur-md p-8 md:p-12 shadow-2xl">
        <div className="absolute top-0 right-0 p-4">
          <button className="p-2 rounded-full hover:bg-accent/50 transition-colors text-muted-foreground">
            <MoreVertical size={20} />
          </button>
        </div>

        <div className="flex flex-col md:flex-row md:items-end justify-between gap-8">
          <div className="space-y-4 max-w-2xl">
            <div className="flex items-center gap-2 text-indigo-500">
              <Shield size={18} />
              <span className="text-xs font-bold uppercase tracking-[0.2em]">Private Circle</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight">{room.name}</h1>
            {room.description && (
              <p className="text-lg text-muted-foreground leading-relaxed">
                {room.description}
              </p>
            )}
            <div className="flex items-center gap-6 pt-4">
              <div className="flex items-center gap-2 text-sm font-medium">
                <Users size={16} className="text-muted-foreground" />
                <span>{room.member_count} {room.member_count === 1 ? 'Member' : 'Members'}</span>
              </div>
              <div className="flex items-center gap-2 text-sm font-medium">
                <MessageSquare size={16} className="text-muted-foreground" />
                <span>{roomResources?.length || 0} Resources</span>
              </div>
            </div>
          </div>

          <div className="flex flex-col gap-3 min-w-[240px]">
            <div className="flex items-center justify-between p-3 rounded-xl bg-background/50 border border-border/40">
              <div className="flex flex-col">
                <span className="text-[10px] uppercase font-bold text-muted-foreground tracking-wider mb-0.5">Invite Code</span>
                <code className="text-sm font-mono">{room.invite_code}</code>
              </div>
              <button 
                onClick={copyInvite}
                className="p-2 rounded-lg hover:bg-accent transition-all text-muted-foreground hover:text-foreground active:scale-95"
              >
                {copied ? <Check size={16} className="text-green-500" /> : <Copy size={16} />}
              </button>
            </div>
            <button 
              onClick={() => setIsAddModalOpen(true)}
              className="inline-flex items-center justify-center gap-2 w-full py-3 bg-primary text-primary-foreground rounded-xl text-sm font-semibold shadow-lg hover:shadow-primary/20 transition-all hover:-translate-y-0.5"
            >
              <Plus size={18} />
              Add to Circle
            </button>
          </div>
        </div>
      </div>

      {/* Resource Grid */}
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold tracking-tight">Circle Resources</h2>
        </div>

        {isLoadingResources ? (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="aspect-[3/4] rounded-xl bg-muted animate-pulse" />
            ))}
          </div>
        ) : !roomResources || roomResources.length === 0 ? (
          <div className="flex min-h-[300px] flex-col items-center justify-center rounded-2xl border border-dashed border-border/60 bg-muted/30 text-center p-12">
            <div className="bg-background p-4 rounded-full shadow-sm mb-4">
              <Plus className="h-6 w-6 text-muted-foreground" />
            </div>
            <h2 className="text-xl font-semibold mb-2">No private curations</h2>
            <p className="text-muted-foreground max-w-sm mb-6">
              Start sharing exclusive recommendations that only members of this circle can see.
            </p>
            <button 
              onClick={() => setIsAddModalOpen(true)}
              className="inline-flex items-center justify-center rounded-md bg-primary px-6 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90"
            >
              Add first resource
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {roomResources.map((rr) => (
              <ResourceCard 
                key={rr.resource_id} 
                resource={rr.resource} 
                isRoomContext
                onRate={() => setRatingResource({ id: rr.resource_id, title: rr.resource.title })}
              />
            ))}
          </div>
        )}
      </div>

      {/* Modals */}
      <AddResourceModal 
        isOpen={isAddModalOpen} 
        onClose={() => setIsAddModalOpen(false)} 
        roomId={id!} 
      />
      
      {ratingResource && (
        <RatingModal
          isOpen={!!ratingResource}
          onClose={() => setRatingResource(null)}
          resourceId={ratingResource.id}
          resourceTitle={ratingResource.title}
          roomId={id}
        />
      )}
    </div>
  )
}
