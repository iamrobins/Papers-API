import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE
MONGO_URI = os.getenv("MONGO_URI")


# CACHE
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT")) 
REDIS_DB = int(os.getenv("REDIS_DB"))  

# SECURITY
JWT_SECRET = os.getenv("JWT_SECRET")