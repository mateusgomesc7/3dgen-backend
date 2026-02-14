## 3D Gen Backend

3D Gen Backend is the **API service** for the 3D Gen project. It is built with **FastAPI** and is responsible for AI processing, code generation, and data persistence for the 3D Gen frontend.

The project is designed to run **inside Docker** and uses **Alembic** for database migrations.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/mateusgomesc7/3dgen-backend.git
cd 3dgen-backend
```

---

## ⚙️ Environment Setup

Copy the example environment file:

```bash
cp .env.example .env
```

Edit the `.env` file and configure the required environment variables (database and API keys).

---

## ▶️ Running the Project (Development)

> ⚠️ Docker is required to run this project.

Build and start the containers:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## 🗄️ Database Migrations (Alembic)

Run migrations using Alembic inside the container:

```bash
docker compose exec api alembic upgrade head
```

Create a new migration:

```bash
docker compose exec api alembic revision --autogenerate -m "migration message"
```

---

## 🌱 Seed Data

A seed runner script is available to populate the database with initial data:

```bash
docker compose exec api python seeds/runner.py
```

---

## 📂 Project Structure

```text
.
├── app/              # FastAPI application
├── migrations/       # Alembic migrations
└── seeds/             # Seed scripts
    └── runner.py
```

---

## 🔗 Related Project

This backend is used by the frontend project:

- **3D Gen Frontend** – AI chat interface

---

## 📄 License

MIT © Mateus Gomes
