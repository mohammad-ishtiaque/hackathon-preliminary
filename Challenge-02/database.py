import sqlite_utils
from pathlib import Path

DATABASE_NAME = "kitchen_buddy.db"
DB_PATH = Path(__file__).parent / DATABASE_NAME
db = sqlite_utils.Database(str(DB_PATH))

def init_db():
  """Initialize the database. Create tables if they don't exist."""
  db.create_table("ingredients",
    {"id": int, "name": str, "quantity": float, "unit": str, "date_added": str},
    pk="id"
  )
  db.create_table("recipes",
    {"id": int, "name": str, "cuisine_type": str, "taste": str, "reviews": str, "preparation_time": str, "ingredients": str},
    pk="id"
  )

if not DB_PATH.exists():
    init_db()