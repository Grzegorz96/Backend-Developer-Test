from fastapi import FastAPI  # Import FastAPI from the fastapi package
from routes import (
    auth,
    post,
)  # Import the auth and post modules from the routes package

app = FastAPI()  # Create an instance of the FastAPI class

# Include the auth router in the FastAPI app
app.include_router(auth.router)
# Include the post router in the FastAPI app
app.include_router(post.router)

# Command to start the FastAPI application using uvicorn with auto-reload enabled
# start uvicorn main:app --reload
