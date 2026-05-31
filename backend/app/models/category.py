from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    is_admin_created = Column(Boolean, default=True, nullable=False)
    parent_category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent", cascade="all, delete-orphan")
    resources = relationship("Resource", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"
