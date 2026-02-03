from app.models.provider import Provider
from app.schemas.enums import ProviderType

def seed(db):
    providers = [
        {"name": ProviderType.OLLAMA.value, "is_active": True},
        {"name": ProviderType.GOOGLE.value, "is_active": True},
    ]
    for p_data in providers:
        if not db.query(Provider).filter(Provider.name == p_data["name"]).first():
            db.add(Provider(**p_data))
            print(f"✅ Provider '{p_data['name']}' seeded.")