from peewee import SqliteDatabase
import os


DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
DATABASE = SqliteDatabase(os.getenv("DATABASE_PATH", "/data/database.db"))
