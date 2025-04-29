import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI",
    "mongodb://root:root_password@localhost:27017"
)
DB_NAME   = os.getenv("DB_NAME", "opobot")