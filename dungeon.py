import random
from collections import deque
from config import (WIDTH, HEIGHT, VISIT_PROB, EXTRA_CONN_PROB, in_bounds,
                    MIN_X, MAX_X, MIN_Y, MAX_Y, ITEM_CONFIG, DIRECTIONS, BOSS_ENEMY)

# Global counters and containers.
ITEM_COUNTS = {item: 0 for item in ITEM_CONFIG}
dungeon = {}
visited = set()

def create_room(x, y):
    room_id = f"room_{y}_{x}"
    items = []
    for item, config in ITEM_CONFIG.items():
        if random.random() < config["prob"] and ITEM_COUNTS[item] < config["max"]:
            items.append(item)
            ITEM_COUNTS[item] += 1
    return {
        "roomId": room_id,
        "name": f"Room {y},{x}",
        "description": f"A mysterious room at coordinates ({x}, {y}).",
        "connections": {},
        "contents": {"items": items, "enemies": []},
        "visited": False,
        "coords": {"x": x, "y": y}
    }

def dfs(x, y):
    visited.add((x, y))
    dungeon[(x, y)] = create_room(x, y)
    directions = list(DIRECTIONS.items())
    random.shuffle(directions)
    for dir_name, (dx, dy, opposite) in directions:
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny) and (nx, ny) not in visited:
            if random.random() < VISIT_PROB:
                dfs(nx, ny)
                if (nx, ny) in dungeon:
                    current_room = dungeon[(x, y)]
                    neighbor_room = dungeon[(nx, ny)]
                    current_room["connections"][dir_name] = neighbor_room["roomId"]
                    neighbor_room["connections"][opposite] = current_room["roomId"]

def add_extra_connections():
    for (x, y), room in dungeon.items():
        for dir_name, (dx, dy, opposite) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and (nx, ny) in dungeon:
                if dir_name not in room["connections"] and random.random() < EXTRA_CONN_PROB:
                    neighbor_room = dungeon[(nx, ny)]
                    room["connections"][dir_name] = neighbor_room["roomId"]
                    neighbor_room["connections"][opposite] = room["roomId"]

def bfs(start_coord):
    queue = deque([(start_coord, 0)])
    distances = {start_coord: 0}
    while queue:
        (x, y), dist = queue.popleft()
        current_room = dungeon[(x, y)]
        for neighbor_id in current_room["connections"].values():
            parts = neighbor_id.split("_")
            ny, nx = int(parts[1]), int(parts[2])
            neighbor_coord = (nx, ny)
            if neighbor_coord not in distances:
                distances[neighbor_coord] = dist + 1
                queue.append((neighbor_coord, dist + 1))
    return distances

def choose_boss_room(spawn_coord):
    distances = bfs(spawn_coord)
    if len(distances) > 1 and spawn_coord in distances:
        filtered = {coord: d for coord, d in distances.items() if coord != spawn_coord}
        boss_coord = max(filtered, key=filtered.get)
    else:
        boss_coord = max(distances, key=distances.get)
    boss_room = dungeon[boss_coord]
    boss_room["contents"]["enemies"].append(BOSS_ENEMY)
    boss_room["name"] += " (Boss Room)"
    boss_room["description"] += " This room emanates an ominous presence..."
    return boss_coord

def ensure_items(boss_coord):
    for item, config in ITEM_CONFIG.items():
        if config.get("ensure", False):
            found = False
            for coord, room in dungeon.items():
                if coord == boss_coord:
                    continue
                if item in room["contents"]["items"]:
                    found = True
                    break
            if not found:
                non_boss_rooms = [coord for coord in dungeon if coord != boss_coord]
                if non_boss_rooms:
                    chosen_coord = random.choice(non_boss_rooms)
                    dungeon[chosen_coord]["contents"]["items"].append(item)
                    ITEM_COUNTS[item] += 1

def reduce_boss_connections(boss_coord):
    boss_room = dungeon[boss_coord]
    if len(boss_room["connections"]) > 1:
        keep_dir = random.choice(list(boss_room["connections"].keys()))
        for d in list(boss_room["connections"].keys()):
            if d != keep_dir:
                removed_neighbor_id = boss_room["connections"].pop(d)
                parts = removed_neighbor_id.split("_")
                rem_y, rem_x = int(parts[1]), int(parts[2])
                neighbor_room = dungeon[(rem_x, rem_y)]
                for ndir, nconn in list(neighbor_room["connections"].items()):
                    if nconn == boss_room["roomId"]:
                        neighbor_room["connections"].pop(ndir)
                        break

def generate_dungeon(min_rooms=10):
    global dungeon, visited, ITEM_COUNTS
    while True:
        # Reset global containers
        dungeon = {}
        visited = set()
        ITEM_COUNTS = {item: 0 for item in ITEM_CONFIG}
        
        spawn_coord = (0, 0)
        dfs(*spawn_coord)
        add_extra_connections()
        
        # Check if we have reached the minimum room count.
        if len(dungeon) >= min_rooms:
            boss_coord = choose_boss_room(spawn_coord)
            ensure_items(boss_coord)
            reduce_boss_connections(boss_coord)
            return spawn_coord, boss_coord, dungeon
