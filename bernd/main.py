from bernd.discord.bot import start_bot
from bernd.database.migrations import run_migrations

run_migrations()

start_bot()
