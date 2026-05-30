from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    invite_code = Column(String(50), unique=True, nullable=False)
    is_private = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Room {self.name}>"

class RoomMember(Base):
    __tablename__ = "room_members"

    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<RoomMember room={self.room_id} user={self.user_id}>"

class RoomResource(Base):
    __tablename__ = "room_resources"

    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True)
    resource_id = Column(UUID(as_uuid=True), ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True)
    added_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<RoomResource room={self.room_id} resource={self.resource_id}>"

class RoomRating(Base):
    __tablename__ = "room_ratings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    room_id = Column(UUID(as_uuid=True), ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    resource_id = Column(UUID(as_uuid=True), ForeignKey("resources.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("room_id", "resource_id", "user_id", name="uq_room_rating"),
    )

    def __repr__(self):
        return f"<RoomRating {self.rating}/10 by {self.user_id} in {self.room_id}>"
