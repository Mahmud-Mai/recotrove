import { useQuery } from "@tanstack/react-query"
import axios from "axios"
import { ResourceCard } from "../components/resource-card"
import type { Resource } from "../components/resource-card"
import { RatingModal } from "../components/rating-modal"
import { Loader2, Plus, Filter } from "lucide-react"
import { Link } from "react-router-dom"
import { useState } from "react"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8030/api/v1"

export default function ResourcesPage() {
  const [ratingResource, setRatingResource] = useState<{ id: string, title: string } | null>(null)

  const { data: resources, isLoading, error } = useQuery<Resource[]>({
    queryKey: ["resources"],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/resources`)
      return response.data
    }
  })

  if (isLoading) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-[400px] flex-col items-center justify-center text-center">
        <p className="text-destructive font-medium">Failed to load resources</p>
        <p className="text-sm text-muted-foreground mt-1">Please check if the backend is running.</p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Resources</h1>
          <p className="text-muted-foreground">
            Explore curated recommendations from our community.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button className="inline-flex items-center justify-center rounded-md border border-border px-4 py-2 text-sm font-medium hover:bg-accent transition-colors">
            <Filter className="mr-2 h-4 w-4" />
            Filter
          </button>
          <Link 
            to="/resources/new" 
            className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90"
          >
            <Plus className="mr-2 h-4 w-4" />
            Add Resource
          </Link>
        </div>
      </div>

      {!resources || resources.length === 0 ? (
        <div className="flex min-h-[300px] flex-col items-center justify-center rounded-2xl border border-dashed border-border/60 bg-muted/30 text-center p-12">
          <div className="bg-background p-4 rounded-full shadow-sm mb-4">
            <Plus className="h-6 w-6 text-muted-foreground" />
          </div>
          <h2 className="text-xl font-semibold mb-2">No resources found</h2>
          <p className="text-muted-foreground max-w-sm mb-6">
            Be the first to share something worth everyone's time.
          </p>
          <Link 
            to="/resources/new" 
            className="inline-flex items-center justify-center rounded-md bg-primary px-6 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90"
          >
            Add your first resource
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {resources.map((resource) => (
            <ResourceCard 
              key={resource.id} 
              resource={resource} 
              onRate={() => setRatingResource({ id: resource.id, title: resource.title })}
            />
          ))}
        </div>
      )}

      {ratingResource && (
        <RatingModal
          isOpen={!!ratingResource}
          onClose={() => setRatingResource(null)}
          resourceId={ratingResource.id}
          resourceTitle={ratingResource.title}
        />
      )}
    </div>
  )
}
