import { useState } from "react"
import type { KeyboardEvent } from "react"
import { X, Plus } from "lucide-react"

interface TagInputProps {
  tags: string[]
  setTags: (tags: string[]) => void
  placeholder?: string
}

export function TagInput({ tags, setTags, placeholder = "Add genre (press Enter)..." }: TagInputProps) {
  const [inputValue, setInputValue] = useState("")

  const addTag = () => {
    const trimmed = inputValue.trim().toLowerCase()
    if (trimmed && !tags.includes(trimmed)) {
      setTags([...tags, trimmed])
      setInputValue("")
    }
  }

  const removeTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove))
  }

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      addTag()
    } else if (e.key === 'Backspace' && !inputValue && tags.length > 0) {
      removeTag(tags[tags.length - 1])
    }
  }

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2 min-h-[42px] p-1.5 rounded-md border border-input bg-background focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2 transition-all">
        {tags.map((tag) => (
          <span 
            key={tag} 
            className="inline-flex items-center gap-1 bg-secondary text-secondary-foreground px-2 py-1 rounded-md text-xs font-medium border border-border/50"
          >
            {tag}
            <button 
              type="button" 
              onClick={() => removeTag(tag)}
              className="hover:text-destructive transition-colors"
            >
              <X size={12} />
            </button>
          </span>
        ))}
        <input
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={tags.length === 0 ? placeholder : ""}
          className="flex-1 bg-transparent border-none outline-none text-sm min-w-[120px] placeholder:text-muted-foreground px-1"
        />
      </div>
      
      {inputValue.trim() && (
        <button
          type="button"
          onClick={addTag}
          className="text-xs flex items-center gap-1 text-muted-foreground hover:text-foreground transition-colors"
        >
          <Plus size={12} />
          Add "{inputValue.trim()}"
        </button>
      )}
    </div>
  )
}
