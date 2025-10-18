from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from hackathon.routes import (
    users,
    hackathon,
    registration,
    submissions,
)
from hackathon.auth import auth
from hackathon.file_upload import file_upload
from hackathon.notification import email_utils

app = FastAPI(
    title="Hackathon Platform API",
    description="Backend API for managing hackathons, registrations, submissions, users, and authentication.",
    version="1.0.0"
)

# ✅ CORS Middleware (so frontend can access the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. Later restrict by frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include Routers
app.include_router(users.router)
app.include_router(hackathon.router)
app.include_router(registration.router)
app.include_router(submissions.router)
app.include_router(auth.router)
app.include_router(file_upload.router)

# ✅ Root Endpoint
@app.get("/")
def root():
    return {"message": "🚀 Hackathon Platform API is running successfully!"}
