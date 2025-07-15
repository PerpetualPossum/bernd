from peewee_migrate import Router
from bernd.constants import DATABASE

router = Router(DATABASE)


def run_migrations():
    """Run all migrations."""
    try:
        # Running migrations
        router.run()
    except Exception as e:
        print(f"Error running migrations: {e}")
        raise
