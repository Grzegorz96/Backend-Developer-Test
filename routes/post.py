from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Post
from schemas import PostCreate
from auth import verify_token
from cache import get_cached_posts, set_cached_posts, delete_cached_posts

router = APIRouter()


"""
Endpoint to add a new post.

Args:
    post (PostCreate): The post data to be created.
    token (str): The authentication token of the user.
    db (Session, optional): The database session. Defaults to Depends(get_db).

Returns:
    dict: A dictionary containing the ID of the newly created post.
"""


@router.post("/posts", status_code=status.HTTP_201_CREATED)
def add_post(post: PostCreate, token: str, db: Session = Depends(get_db)):
    user = verify_token(token, db)
    new_post = Post(text=post.text, owner_id=user.id)
    db.add(new_post)
    db.commit()
    return {"postID": new_post.id}


"""
Endpoint to retrieve posts for a user.

Args:
    token (str): The authentication token of the user.
    db (Session, optional): The database session dependency.

Returns:
    dict: A dictionary containing the user's posts.

Raises:
    HTTPException: If the token is invalid or the user is not authenticated.

This function first verifies the user's token and retrieves the user's information.
It then attempts to get the user's posts from the cache. If the posts are found in the cache,
they are returned immediately. If not, the function queries the database for the user's posts,
caches the result, and then returns the posts.
"""


@router.get("/posts")
def get_posts(token: str, db: Session = Depends(get_db)):
    user = verify_token(token, db)
    posts_data = get_cached_posts(user.id)
    if posts_data:
        return {"posts": posts_data}
    posts = db.query(Post).filter(Post.owner_id == user.id).all()
    posts_data = [{"id": post.id, "text": post.text} for post in posts]
    set_cached_posts(user.id, posts_data)
    return {"posts": posts_data}


"""
Delete a post.

Args:
    postID (int): The ID of the post to be deleted.
    token (str): The authentication token of the user.
    db (Session, optional): The database session. Defaults to Depends(get_db).

Raises:
    HTTPException: If the post is not found or the user is not authorized to delete the post.

Returns:
    dict: A message indicating that the post has been deleted.
"""


@router.delete("/posts")
def delete_post(postID: int, token: str, db: Session = Depends(get_db)):
    user = verify_token(token, db)
    post = db.query(Post).filter(Post.id == postID, Post.owner_id == user.id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    delete_cached_posts(user.id)
    return {"message": "Post deleted"}
