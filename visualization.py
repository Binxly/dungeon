import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from mongodb_integration import get_mongo_collection

def build_graph_from_rooms(rooms):
    G = nx.Graph()
    pos = {}
    for room in rooms:
        room_id = room["roomId"]
        G.add_node(room_id, label=room.get("name", room_id))
        # RoomId format: "room_y_x"
        _, y_str, x_str = room_id.split('_')
        y, x = int(y_str), int(x_str)
        pos[room_id] = (x, -y)
    for room in rooms:
        room_id = room["roomId"]
        for direction, neighbor_id in room["connections"].items():
            if not G.has_edge(room_id, neighbor_id):
                G.add_edge(room_id, neighbor_id, direction=direction)
    return G, pos

def bfs_farthest(G, start_room):
    distances = {start_room: 0}
    queue = [start_room]
    while queue:
        current = queue.pop(0)
        for neighbor in G.neighbors(current):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    farthest_room = max(distances, key=distances.get)
    return farthest_room, distances[farthest_room]

def visualize_dungeon(G, pos, spawn_room_id, boss_room_id):
    node_labels = nx.get_node_attributes(G, "label")
    node_colors = []
    for node in G.nodes():
        if node == spawn_room_id:
            node_colors.append("green")
        elif node == boss_room_id:
            node_colors.append("red")
        else:
            node_colors.append("lightblue")
    plt.figure(figsize=(8, 8))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.7)
    plt.title("Dungeon Map (Spawn at 0,0)")
    plt.axis("off")
    plt.show()

def run_visualization():
    collection = get_mongo_collection()
    rooms = list(collection.find({}))
    G, pos = build_graph_from_rooms(rooms)
    spawn_room_id = "room_0_0"  # Explicitly define spawn
    boss_room_id, distance = bfs_farthest(G, spawn_room_id)
    print(f"Boss room determined as {boss_room_id} at distance {distance} from spawn.")
    visualize_dungeon(G, pos, spawn_room_id, boss_room_id)
