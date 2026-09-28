# TechSphere API

An asynchronous backend REST API designed for project tracking and management. Built with FastAPI and MongoDB Atlas, this service features a fully modular architecture, secure endpoints via JSON Web Tokens (JWT), and real-time data streaming capabilities.

## Tech Stack
* **Framework:** FastAPI
* **Database:** MongoDB Atlas (AsyncIOMotorClient)
* **Authentication:** PyJWT, Passlib (Bcrypt), OAuth2
* **Data Validation:** Pydantic
* **Server:** Uvicorn

## Core Features
* **Asynchronous CRUD:** Non-blocking endpoints to create, read, update, and delete project records.
* **JWT Security:** User registration and login flow with hashed passwords and protected routes.
* **Real-Time WebSockets:** Persistent two-way communication channel (`/ws/realtime`) for live event processing.
* **Modular Architecture:** Clean separation of database connections, authentication logic, and main application routing to prevent circular dependencies.

## Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ayush0801singh-lgtm/TechCircle
   cd TechSphere-project
2. **Install Dependencies**: pip install -requirements.txt
3. **Configure environment variables:**
   Create a .env file in the root directory with the following keys:
   MONGO_URI=your_mongodb_atlas_connection_string
   JWT_SECRET=your_secure_random_secret_string
4. **Run the server:**
   uvicorn main:app --reload
