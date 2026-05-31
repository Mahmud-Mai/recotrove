import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import axios from "axios"
import { useAuth } from "../context/auth-context"
import { AlertCircle, Loader2, ArrowLeft, Link as LinkIcon, Image as ImageIcon, Type, FileText } from "lucide-react"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8030/api/v1"

interface Category {
  id: string
  name: string
}

export default function NewResourcePage() {
  const { token } = useAuth()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [thumbnailUrl, setThumbnailUrl] = useState("")
  const [externalLink, setExternalLink] = useState("")
  const [categoryId, setCategoryId] = useState("")
  const [error, setError] = useState<string | null>(null)

  const { data: categories, isLoading: isLoadingCategories } = useQuery<Category[]>({
    queryKey: ["categories"],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/categories`)
      return response.data
    }
  })

  const mutation = useMutation({
    mutationFn: async (newResource: any) => {
      const response = await axios.post(`${API_URL}/resources`, newResource, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["resources"] })
      navigate("/resources")
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || "Failed to create resource. Please try again.")
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    
    if (!categoryId) {
      setError("Please select a category")
      return
    }

    mutation.mutate({
      title,
      description: description || null,
      thumbnail_url: thumbnailUrl || null,
      external_link: externalLink || null,
      category_id: categoryId
    })
  }

  return (
    <div className="max-w-2xl mx-auto space-y-8">
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

      <div className="rounded-2xl border border-border/50 bg-card/50 backdrop-blur-sm p-8 shadow-sm">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2" htmlFor="title">
              <Type size={14} className="text-muted-foreground" />
              Title
            </label>
            <input
              id="title"
              placeholder="Clean Code"
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2" htmlFor="category">
              Category
            </label>
            <select
              id="category"
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 appearance-none cursor-pointer"
              value={categoryId}
              onChange={(e) => setCategoryId(e.target.value)}
              disabled={isLoadingCategories}
              required
            >
              <option value="">Select a category</option>
              {categories?.map((cat) => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center gap-2" htmlFor="externalLink">
              <LinkIcon size={14} className="text-muted-foreground" />
              External Link
            </label>
            <input
              id="externalLink"
              placeholder="https://amazon.com/..."
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
              Create Resource
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
