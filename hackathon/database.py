from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
db = client["hackathon_db"]

users_collection = db["Users"]
hackathon_collection = db["Hackathons"]
registrations_collection = db["Registrations"]
submissions_collection = db["Submissions"]
scores_collection = db["Scores"]