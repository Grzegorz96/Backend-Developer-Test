import redis
import json

# Cache expiry time in seconds (5 minutes)
CACHE_EXPIRY = 300

# Initialize Redis client
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def get_cached_posts(user_id: int):
    """
    Retrieve cached posts for a given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: The cached posts if available, otherwise None.
    """
    cache_key = f"posts:{user_id}"
    cached_posts = redis_client.get(cache_key)
    if cached_posts:
        return json.loads(cached_posts)
    return None


def set_cached_posts(user_id: int, posts_data: list):
    """
    Cache posts data for a given user ID.

    Args:
        user_id (int): The ID of the user.
        posts_data (list): The posts data to cache.
    """
    cache_key = f"posts:{user_id}"
    redis_client.setex(cache_key, CACHE_EXPIRY, json.dumps(posts_data))


def delete_cached_posts(user_id: int):
    """
    Delete cached posts for a given user ID.

    Args:
        user_id (int): The ID of the user.
    """
    cache_key = f"posts:{user_id}"
    redis_client.delete(cache_key)
