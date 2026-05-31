from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

# Many-to-Many association table for Resources and Tags
resource_tags = Table(
    "resource_tags",
    Base.metadata,
    Column("resource_id", UUID(as_uuid=True), ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    resources = relationship("Resource", secondary=resource_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag {self.name}>"
