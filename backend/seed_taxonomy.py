#!/usr/bin/env python
"""
Run this script to seed the initial hierarchical taxonomy.
Usage: python seed_taxonomy.py
"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.category import Category

async def seed_taxonomy():
    engine = create_async_engine(settings.database.DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    # Note: Sub-category names are prefixed with Type to avoid UniqueViolation
    # since 'Series' might exist under both 'Anime' and 'Kdrama'.
    taxonomy = {
        "Books": ["Fiction", "Non-Fiction", "Academic", "Graphic Novels"],
        "Movies": ["Feature Film", "Documentary", "Short Film", "Animation"],
        "Anime": ["Anime Series", "Anime Movie", "OVA", "ONA"],
        "Kdrama": ["Kdrama Series", "Kdrama Movie", "Special"],
        "Courses": ["Programming", "Design", "Business", "Personal Development"]
    }

    async with async_session() as db:
        for type_name, subcats in taxonomy.items():
            # Create Top Level
            result = await db.execute(select(Category).where(Category.name == type_name))
            parent = result.scalar_one_or_none()
            if not parent:
                parent = Category(name=type_name, is_admin_created=True)
                db.add(parent)
                await db.flush()
                print(f"Created Type: {type_name}")
            else:
                print(f"Type already exists: {type_name}")
            
            # Create Subcategories
            for sub_name in subcats:
                result = await db.execute(
                    select(Category).where(
                        Category.name == sub_name, 
                        Category.parent_category_id == parent.id
                    )
                )
                if not result.scalar_one_or_none():
                    subcat = Category(name=sub_name, parent_category_id=parent.id, is_admin_created=True)
                    db.add(subcat)
                    print(f"  - Created Sub-category: {sub_name}")
        
        await db.commit()
        print("\n✅ Taxonomy seeded successfully.")

if __name__ == "__main__":
    asyncio.run(seed_taxonomy())
