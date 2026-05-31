import { useState, useMemo } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import axios from "axios"
import { useAuth } from "../context/auth-context"
import { TagInput } from "../components/tag-input"
import { AlertCircle, Loader2, ArrowLeft, Link as LinkIcon, Image as ImageIcon, Type, FileText, Check } from "lucide-react"
import { cn } from "../lib/utils"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8030/api/v1"

interface Category {
  id: string
  name: string
  children: Category[]
}

export default function NewResourcePage() {
  const { token } = useAuth()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const queryClient = useQueryClient()
  
  const roomId = searchParams.get("roomId")
  
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [thumbnailUrl, setThumbnailUrl] = useState("")
  const [externalLink, setExternalLink] = useState("")
  const [tags, setTags] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)

  // Taxonomy State
  const [typeId, setTypeId] = useState("")
  const [categoryId, setCategoryId] = useState("")

  const { data: taxonomy, isLoading: isLoadingTaxonomy } = useQuery<Category[]>({
    queryKey: ["taxonomy"],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/categories?only_top_level=true`)
      return response.data
    }
  })

  const selectedType = useMemo(() => 
    taxonomy?.find(t => t.id === typeId), 
    [taxonomy, typeId]
  )

  const mutation = useMutation({
    mutationFn: async (newResource: any) => {
      // 1. Create the resource
      const response = await axios.post(`${API_URL}/resources`, newResource, {
        headers: { Authorization: `Bearer ${token}` }
      })
      const createdResource = response.data

      // 2. If roomId is present, add it to the room
      if (roomId) {
        await axios.post(
          `${API_URL}/rooms/${roomId}/resources`, 
          { resource_id: createdResource.id },
          { headers: { Authorization: `Bearer ${token}` } }
        )
      }
      
      return createdResource
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resources"] })
      if (roomId) {
        queryClient.invalidateQueries({ queryKey: ["room-resources", roomId] })
        navigate(`/rooms/${roomId}`)
      } else {
        navigate("/resources")
      }
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || "Failed to create resource. Please try again.")
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    
    const finalCategoryId = categoryId || typeId
    if (!finalCategoryId) {
      setError("Please select at least a resource type (e.g., Books)")
      return
    }

    mutation.mutate({
      title,
      description: description || null,
      thumbnail_url: thumbnailUrl || null,
      external_link: externalLink || null,
      category_id: finalCategoryId,
      tags
    })
  }

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div className="flex items-center gap-4">
        <button 
          onClick={() => navigate(-1)}
          className="p-2 rounded-full hover:bg-accent transition-colors text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft size={20} />
        </button>
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Add Resource</h1>
          <p className="text-muted-foreground">Share a recommendation with the community.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Form */}
        <div className="lg:col-span-2 space-y-6">
          <div className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-sm p-8 shadow-sm space-y-6">
            <form id="resource-form" onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <label className="text-sm font-medium flex items-center gap-2" htmlFor="title">
                  <Type size={14} className="text-muted-foreground" />
                  Title
                </label>
                <input
                  id="title"
                  placeholder="e.g., Clean Code, Interstellar, Attack on Titan"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium flex items-center gap-2" htmlFor="externalLink">
                  <LinkIcon size={14} className="text-muted-foreground" />
                  External Link
                </label>
                <input
                  id="externalLink"
                  placeholder="https://example.com/..."
                  type="url"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50"
                  value={externalLink}
                  onChange={(e) => setExternalLink(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium flex items-center gap-2" htmlFor="thumbnailUrl">
                  <ImageIcon size={14} className="text-muted-foreground" />
                  Thumbnail URL
                </label>
                <input
                  id="thumbnailUrl"
                  placeholder="https://images.unsplash.com/..."
                  type="url"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50"
                  value={thumbnailUrl}
                  onChange={(e) => setThumbnailUrl(e.target.value)}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium flex items-center gap-2" htmlFor="description">
                  <FileText size={14} className="text-muted-foreground" />
                  Description
                </label>
                <textarea
                  id="description"
                  placeholder="Tell others why this is worth their time..."
                  className="flex min-h-[150px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 resize-y"
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
            </form>
          </div>
        </div>

        {/* Curation Sidebar (Taxonomy & Tags) */}
        <div className="space-y-6">
          <div className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-sm p-6 shadow-sm space-y-6">
            <h3 className="font-semibold text-sm uppercase tracking-wider text-muted-foreground">Classification</h3>
            
            <div className="space-y-4">
              {/* Step 1: Resource Type */}
              <div className="space-y-2">
                <label className="text-xs font-medium text-muted-foreground">1. Resource Type</label>
                <div className="grid grid-cols-2 gap-2">
                  {isLoadingTaxonomy ? (
                    <div className="col-span-2 flex justify-center py-4">
                      <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
                    </div>
                  ) : (
                    taxonomy?.map((type) => (
                      <button
                        key={type.id}
                        type="button"
                        onClick={() => { setTypeId(type.id); setCategoryId(""); }}
                        className={cn(
                          "px-3 py-2 text-xs font-medium rounded-md border transition-all text-left flex justify-between items-center",
                          typeId === type.id 
                            ? "bg-primary text-primary-foreground border-primary shadow-sm" 
                            : "bg-background hover:bg-accent border-border/50 text-muted-foreground hover:text-foreground"
                        )}
                      >
                        {type.name}
                        {typeId === type.id && <Check size={12} />}
                      </button>
                    ))
                  )}
                </div>
              </div>

              {/* Step 2: Category (Dynamic based on Type) */}
              {selectedType && selectedType.children.length > 0 && (
                <div className="space-y-2 animate-in fade-in slide-in-from-top-2 duration-300">
                  <label className="text-xs font-medium text-muted-foreground">2. Category</label>
                  <div className="grid grid-cols-1 gap-2">
                    {selectedType.children.map((cat) => (
                      <button
                        key={cat.id}
                        type="button"
                        onClick={() => setCategoryId(cat.id)}
                        className={cn(
                          "px-3 py-2 text-xs font-medium rounded-md border transition-all text-left flex justify-between items-center",
                          categoryId === cat.id 
                            ? "bg-secondary text-secondary-foreground border-secondary shadow-sm" 
                            : "bg-background hover:bg-accent border-border/50 text-muted-foreground hover:text-foreground"
                        )}
                      >
                        {cat.name}
                        {categoryId === cat.id && <Check size={12} />}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Step 3: Granular Genres/Tags */}
              <div className="space-y-2 pt-2 border-t border-border/40">
                <label className="text-xs font-medium text-muted-foreground">3. Genres & Tags</label>
                <TagInput 
                  tags={tags} 
                  setTags={setTags} 
                  placeholder={selectedType ? `e.g., thriller, action...` : "Select a type first..."} 
                />
                <p className="text-[10px] text-muted-foreground italic">
                  Enter to add. Use granular tags for better discovery.
                </p>
              </div>
            </div>

            <div className="pt-4">
              <button
                form="resource-form"
                type="submit"
                className="w-full inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                disabled={mutation.isPending}
              >
                {mutation.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Publish Curation
              </button>
            </div>
          </div>

          <div className="p-4 rounded-xl border border-indigo-500/20 bg-indigo-500/5">
            <h4 className="text-xs font-semibold text-indigo-500 mb-1">Elite Tip</h4>
            <p className="text-[10px] text-indigo-500/70 leading-relaxed">
              Detailed metadata helps others find your recommendations. Adding 3-5 genres is recommended for high-quality curations.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
