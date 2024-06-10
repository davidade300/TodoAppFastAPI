"""main file"""
from fastapi import FastAPI
import uvicorn
from database import engine
from routers import auth, todos, admin, users
from models import Base


app = FastAPI(debug=True)

Base.metadata.create_all(bind=engine)


@app.get("/healthy")
def healt_check():
    """endpoint for pytest"""
    return {"status": "Healthy"}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
