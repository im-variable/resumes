from fastapi import FastAPI
from middlewares.middleware import GlobalMiddleware
from settings.routing import router
from settings.database import engine, Base

# ✅ Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Add Middleware
app.add_middleware(GlobalMiddleware)

# ✅ Include API routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Project"}