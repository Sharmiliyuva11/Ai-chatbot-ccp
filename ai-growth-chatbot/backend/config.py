# backend/config.py

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-default-secret')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
