import json

def filter_by_min_distance(data, max_results):
    documents = data["documents"][0]  # Extract documents
    metadatas = data["metadatas"][0]  # Extract metadatas
    distances = data["distances"][0]  # Extract distances

    # Create a mapping of item_id to (index, distance)
    min_distance_map = {}

    for i, metadata in enumerate(metadatas):
        item_id = metadata.get("item_id", None)  # Get item_id or None if not present
        if item_id:
            # Keep the entry with the smallest distance
            if item_id not in min_distance_map or distances[i] < min_distance_map[item_id][1]:
                min_distance_map[item_id] = (i, distances[i])

    # Indices to keep
    min_indices = set(idx for idx, _ in min_distance_map.values())

    # Filter data
    filtered_documents = [doc for i, doc in enumerate(documents) if i in min_indices]
    filtered_metadatas = [meta for i, meta in enumerate(metadatas) if i in min_indices]
    filtered_distances = [dist for i, dist in enumerate(distances) if i in min_indices]

    return {
        "documents": filtered_documents[:max_results],
        "metadatas": filtered_metadatas[:max_results],
        "distances": filtered_distances[:max_results]
    }