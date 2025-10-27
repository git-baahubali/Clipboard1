def normalize_node_minimal(node):
    """
    Minimal normalization:
    - node['content'] <- joining immediate paragraph children (if any)
    - node['children'] <- list of normalized section children only
    """
    # combine immediate paragraph texts
    paragraphs = [
        child.get("text", "").strip()
        for child in node.get("children", [])
        if child.get("type") == "paragraph" and child.get("text", "").strip()
    ]
    node["content"] = "\n".join(paragraphs) if paragraphs else ""

    # recursively keep only section children
    new_children = []
    for child in node.get("children", []):
        if child.get("type") == "section":
            new_children.append(normalize_node_minimal(child))
    node["children"] = new_children

    # Optionally drop other keys you don't need (runs/raw_text) if desired
    # e.g., for cleanliness: node.pop('runs', None); node.pop('raw_text', None)
    return node
