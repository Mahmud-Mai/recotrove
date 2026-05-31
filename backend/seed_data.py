import asyncio
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings
from app.models.category import Category
from app.models.resource import Resource
from app.models.user import User
from app.models.tag import Tag

async def get_or_create_tags(db: AsyncSession, tag_names: list[str]) -> list[Tag]:
    tags = []
    for name in tag_names:
        name = name.lower().strip()
        result = await db.execute(select(Tag).where(Tag.name == name))
        tag = result.scalar_one_or_none()
        if not tag:
            tag = Tag(name=name)
            db.add(tag)
        tags.append(tag)
    return tags

async def seed_data():
    engine = create_async_engine(settings.database.DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as db:
        # 1. Get Admin User
        result = await db.execute(select(User).where(User.role == "admin"))
        admin = result.scalars().first()
        if not admin:
            print("❌ Admin user not found. Run seed_admin.py first.")
            return

        # 2. Get Categories
        result = await db.execute(select(Category))
        categories = result.scalars().all()
        cat_map = {c.name: c.id for c in categories}

        # Popular data to seed
        popular_resources = [
            {
                "title": "Interstellar",
                "description": "When Earth becomes uninhabitable, a team of ex-pilots and scientists is tasked with finding a new home for mankind through a wormhole.",
                "thumbnail_url": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg",
                "external_link": "https://www.imdb.com/title/tt0816692/",
                "category": "Movies",
                "tags": ["Sci-Fi", "Drama", "Nolan"]
            },
            {
                "title": "Inception",
                "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "thumbnail_url": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg",
                "external_link": "https://www.imdb.com/title/tt1375666/",
                "category": "Movies",
                "tags": ["Sci-Fi", "Action", "Dreams"]
            },
            {
                "title": "Clean Code",
                "description": "A Handbook of Agile Software Craftsmanship. Essential reading for any developer.",
                "thumbnail_url": "https://m.media-amazon.com/images/I/41-gcWbz7ML._SX373_BO1,204,203,200_.jpg",
                "external_link": "https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882",
                "category": "Books",
                "tags": ["Programming", "Education", "Software"]
            },
            {
                "title": "Attack on Titan",
                "description": "After his hometown is destroyed and his mother is killed, young Eren Jaeger vows to cleanse the earth of the giant humanoid Titans that have brought humanity to the brink of extinction.",
                "thumbnail_url": "https://m.media-amazon.com/images/M/MV5BNDFjYTIxMjctYTQ2ZC00OGQ4LWE3OGYtZTMzOWZlZNZiM2UxXkEyXkFqcGdeQXVyMTUzMTg2ODkz._V1_SX300.jpg",
                "external_link": "https://myanimelist.net/anime/16498/Shingeki_no_Kyojin",
                "category": "Anime",
                "tags": ["Action", "Dark Fantasy", "Titans"]
            },
            {
                "title": "1984",
                "description": "In a totalitarian future society, a man whose daily work is rewriting history tries to rebel by falling in love.",
                "thumbnail_url": "https://m.media-amazon.com/images/I/71kxa1-0mfL.jpg",
                "external_link": "https://www.goodreads.com/book/show/40961427-1984",
                "category": "Books",
                "tags": ["Dystopian", "Classic", "Politics"]
            }
        ]

        for res_data in popular_resources:
            cat_name = res_data["category"]
            if cat_name not in cat_map:
                print(f"⚠️ Category {cat_name} not found, skipping {res_data['title']}")
                continue
            
            # Check if exists
            check_res = await db.execute(select(Resource).where(Resource.title == res_data["title"]))
            if check_res.scalar_one_or_none():
                print(f"⏩ Resource already exists: {res_data['title']}")
                continue

            tag_names = res_data.pop("tags")
            cat_name = res_data.pop("category")
            
            resource = Resource(
                **res_data,
                category_id=cat_map[cat_name],
                created_by=admin.id
            )
            resource.tags = await get_or_create_tags(db, tag_names)
            db.add(resource)
            print(f"✨ Seeded Resource: {res_data['title']}")

        await db.commit()
        print("\n✅ Data seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_data())
