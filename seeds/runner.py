import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from seeds import providers_seed, users_seed


def run():
    db = SessionLocal()
    try:
        print('🌱 Starting data seeding...')

        providers_seed.seed(db)
        users_seed.seed(db)

        db.commit()
        print('✨ Database successfully seeded!')
    except Exception as e:
        print(f'❌ Fatal error during seeding: {e}')
        db.rollback()
    finally:
        db.close()


if __name__ == '__main__':
    run()
