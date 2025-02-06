from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

def get_mongo_collection():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

def store_dungeon(collection, dungeon):
    collection.delete_many({}) # Clears existing rooms.
    collection.insert_many(list(dungeon.values())) # Inserts new dungeon data.

def update_spawn_and_boss(collection, spawn_room_id, boss_room):
    # Mark spawn room.
    collection.update_one(
        {"roomId": spawn_room_id},
        {"$set": {"name": f"Spawn",
                  "description": "This is the starting room for the player."}}
    )
    # Update boss room.
    collection.update_one(
        {"roomId": boss_room["roomId"]},
        {"$set": {"name": "Boss",
                  "description": boss_room["description"]},
         "$push": {"contents.enemies": boss_room["contents"]["enemies"][0]}}
    )
