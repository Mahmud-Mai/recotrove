import { useState } from "react"
import { Modal } from "./modal"
import { Star, Loader2, AlertCircle } from "lucide-react"
import { cn } from "../lib/utils"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import axios from "axios"
import { useAuth } from "../context/auth-context"

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8030/api/v1"

interface RatingModalProps {
  isOpen: boolean
  onClose: () => void
  resourceId: string
  resourceTitle: string
  roomId?: string // Optional, for room-specific ratings
}

export function RatingModal({ isOpen, onClose, resourceId, resourceTitle, roomId }: RatingModalProps) {
  const { token } = useAuth()
  const queryClient = useQueryClient()
  const [rating, setRating] = useState(0)
  const [hoveredRating, setHoveredRating] = useState(0)
  const [review, setReview] = useState("")
  const [error, setError] = useState<string | null>(null)

  const mutation = useMutation({
    mutationFn: async () => {
      const url = roomId 
        ? `${API_URL}/rooms/${roomId}/ratings/${resourceId}`
        : `${API_URL}/resources/${resourceId}/ratings`
      
      const response = await axios.post(
        url,
        { rating, review_text: review },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: roomId ? ["room-resources", roomId] : ["resources"] })
      onClose()
      setRating(0)
      setReview("")
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || "Failed to submit rating.")
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (rating === 0) {
      setError("Please select a rating.")
      return
    }
    mutation.mutate()
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title={`Rate "${resourceTitle}"`}>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="flex flex-col items-center justify-center space-y-2">
          <div className="flex items-center gap-1">
            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((star) => (
              <button
                key={star}
                type="button"
                className="transition-transform active:scale-90"
                onMouseEnter={() => setHoveredRating(star)}
                onMouseLeave={() => setHoveredRating(0)}
                onClick={() => setRating(star)}
              >
                <Star
                  size={24}
                  className={cn(
                    "transition-colors",
                    (hoveredRating || rating) >= star
                      ? "fill-amber-500 text-amber-500"
                      : "text-muted-foreground/30"
                  )}
                />
              </button>
            ))}
          </div>
          <span className="text-sm font-medium h-5">
            {(hoveredRating || rating) > 0 ? `${hoveredRating || rating} / 10` : ""}
          </span>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="review">
            Review (Optional)
          </label>
          <textarea
            id="review"
            placeholder="Share your thoughts on this resource..."
            className="flex min-h-[100px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 resize-none"
            value={review}
            onChange={(e) => setReview(e.target.value)}
          />
        </div>

        {error && (
          <div className="flex items-center gap-2 text-sm text-destructive bg-destructive/10 p-3 rounded-md border border-destructive/20">
            <AlertCircle size={14} />
            <span>{error}</span>
          </div>
        )}

        <div className="flex gap-3 justify-end">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium hover:bg-accent rounded-md transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={mutation.isPending}
            className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 disabled:opacity-50"
          >
            {mutation.isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Submit Rating
          </button>
        </div>
      </form>
    </Modal>
  )
}
