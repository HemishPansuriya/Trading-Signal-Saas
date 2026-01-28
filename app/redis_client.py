# # app/redis_client.py
# """
# Single Redis connection used everywhere.
# """

# import redis
# from app.config import REDIS_URL

# redis_client = redis.Redis.from_url(
#     REDIS_URL,
#     decode_responses=True  # return strings instead of bytes
# )
