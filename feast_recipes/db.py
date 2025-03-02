from pymongo import MongoClient
import urllib.parse
username = "22adv3ari0016"
password = urllib.parse.quote_plus("Neelesh@3003")

# Add TLS options
MONGO_URI = f"mongodb+srv://{username}:{password}@feastfitdb.orybr.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true"

# MongoDB connection setup
client = MongoClient(MONGO_URI)
db = client['feastfit_database']  # Replace with your database name

# Export the collections you'll use
interactions_collection = db['feast_recipes_recipeinteraction']  # Replace with your recipes collection name
accounts_collection=db['accounts_profile']