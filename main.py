from dungeon import generate_dungeon
from mongodb_integration import get_mongo_collection, store_dungeon, update_spawn_and_boss
from visualization import run_visualization

def main():
    # Generate the dungeon.
    spawn_coord, boss_coord, dungeon_map = generate_dungeon()
    spawn_room_id = f"room_{spawn_coord[1]}_{spawn_coord[0]}"
    
    # Store dungeon in MongoDB.
    collection = get_mongo_collection()
    store_dungeon(collection, dungeon_map)
    
    # Update spawn and boss room documents.
    boss_room = dungeon_map[boss_coord]
    update_spawn_and_boss(collection, spawn_room_id, boss_room)
    
    # Run visualization.
    run_visualization()

if __name__ == "__main__":
    main()
