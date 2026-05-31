import { ExternalLink, Star, User } from "lucide-react"
import { cn } from "../lib/utils"

export interface Resource {
  id: string
  title: string
  description?: string
  thumbnail_url?: string
  external_link?: string
  category_id: string
  created_by: string
  created_at: string
  average_rating: number
  total_ratings: number
}

interface ResourceCardProps {
  resource: Resource
  className?: string
}

export function ResourceCard({ resource, className }: ResourceCardProps) {
  return (
    <div className={cn(
      "group relative flex flex-col overflow-hidden rounded-xl border border-border/50 bg-card/50 backdrop-blur-sm transition-all hover:border-border hover:shadow-lg hover:-translate-y-1",
      className
    )}>
      {resource.thumbnail_url ? (
        <div className="aspect-video w-full overflow-hidden">
          <img 
            src={resource.thumbnail_url} 
            alt={resource.title}
            className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
        </div>
      ) : (
        <div className="aspect-video w-full bg-muted flex items-center justify-center">
          <span className="text-muted-foreground text-sm font-medium italic">No preview</span>
        </div>
      )}

      <div className="flex flex-1 flex-col p-5">
        <div className="flex items-start justify-between gap-2 mb-2">
          <h3 className="font-semibold leading-tight text-foreground line-clamp-2">
            {resource.title}
          </h3>
          {resource.external_link && (
            <a 
              href={resource.external_link} 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-muted-foreground hover:text-primary transition-colors p-1"
            >
              <ExternalLink size={16} />
            </a>
          )}
        </div>

        {resource.description && (
          <p className="text-sm text-muted-foreground line-clamp-3 mb-4 flex-1">
            {resource.description}
          </p>
        )}

        <div className="flex items-center justify-between mt-auto pt-4 border-t border-border/40">
          <div className="flex items-center gap-1.5">
            <div className="flex items-center text-amber-500">
              <Star size={14} fill="currentColor" />
            </div>
            <span className="text-sm font-medium">
              {resource.average_rating > 0 ? resource.average_rating.toFixed(1) : "N/A"}
            </span>
            <span className="text-xs text-muted-foreground">
              ({resource.total_ratings})
            </span>
          </div>

          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <User size={12} />
            <span className="truncate max-w-[80px]">Curated</span>
          </div>
        </div>
      </div>
    </div>
  )
}
