from app.models.user import User


def seed(db):
    initial_user = {'name': 'admin'}

    if not db.query(User).filter(User.name == initial_user['name']).first():
        db.add(User(**initial_user))
        print(f"✅ User '{initial_user['name']}' seeded.")
