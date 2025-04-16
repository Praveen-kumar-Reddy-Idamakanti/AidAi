from flask_mongoengine import MongoEngine
from pymongo import MongoClient
import os

db = MongoEngine()

# Initialize MongoDB client for direct access
mongo_client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/aidai_db'))
db_client = mongo_client.get_default_database()