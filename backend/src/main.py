from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from courses.router import courses_router 

app = FastAPI()

# Enable CORS - FIXED
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                    "https://nu-schedule-maker.aidanjkelly.com"],  # Changed from ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your router
app.include_router(courses_router())

# Other routes
@app.get("/api/hello")
def hello():
    return {"message": "Hello from FastAPI!"}

@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe"}