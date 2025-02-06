import random

def random_odd(min_val, max_val):
    n = random.randint(min_val, max_val)
    return n if n % 2 == 1 else n + 1

# Grid configuration
WIDTH = random_odd(3, 9)   # Underlying grid width (odd)
HEIGHT = random_odd(3, 7)  # Underlying grid height (odd)
VISIT_PROB = 0.5         # Chance to visit an adjacent cell
EXTRA_CONN_PROB = 0.333  # Chance to add an extra connection

half_width = WIDTH // 2
half_height = HEIGHT // 2
MIN_X, MAX_X = -half_width, half_width
MIN_Y, MAX_Y = -half_height, half_height

def in_bounds(x, y):
    return MIN_X <= x <= MAX_X and MIN_Y <= y <= MAX_Y

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "dungeon_db"
COLLECTION_NAME = "rooms"

# Item configuration
ITEM_CONFIG = {
    "health potion": {"prob": 0.3, "max": 3, "ensure": True},
    "rusty sword":   {"prob": 0.2, "max": 1, "ensure": True},
    "shield":        {"prob": 0.2, "max": 1, "ensure": False},
    "magic scroll":  {"prob": 0.1, "max": 2, "ensure": False},
    "gold coin":     {"prob": 0.8, "max": 5, "ensure": False},
    "dagger":        {"prob": 0.2, "max": 2, "ensure": True},
    "elixir":        {"prob": 0.3, "max": 2, "ensure": False},
}

# Boss configuration
BOSS_ENEMY = "Dungeon Overlord"

# Direction definitions: (dx, dy, opposite)
DIRECTIONS = {
    "north": (0, 1, "south"),
    "south": (0, -1, "north"),
    "east":  (1, 0, "west"),
    "west":  (-1, 0, "east"),
}
