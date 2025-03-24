from fastapi import FastAPI  # Import FastAPI from the fastapi package
from routes import (
    auth,
    post,
)  # Import the auth and post modules from the routes package
from database import (
    create_tables,
)  # Import the create_tables function from the database module

app = FastAPI()  # Create an instance of the FastAPI class

# Create the tables in the database
create_tables()

# Include the auth router in the FastAPI app
app.include_router(auth.router)
# Include the post router in the FastAPI app
app.include_router(post.router)

# Command to start the FastAPI application using uvicorn with auto-reload enabled
# start uvicorn main:app --reload
