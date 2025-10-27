def normalize_node_recursive_minimal(node):
    """
    Recursive minimal normalizer:
    - 'content': joined immediate paragraph texts (local only)
    - 'children': list of normalized section children (recursively)
    - returns a NEW node dict; does not mutate the input
    """
    # defensive defaults
    children = node.get("children", []) or []

    # collect immediate paragraph texts (local content)
    paragraphs = []
    for child in children:
        if child.get("type") == "paragraph":
            text = child.get("text", "")
            if text and text.strip():
                paragraphs.append(text.strip())

    content = "\n".join(paragraphs) if paragraphs else ""

    # process section children recursively
    normalized_children = []
    for child in children:
        if child.get("type") == "section":
            normalized_children.append(normalize_node_recursive_minimal(child))

    # build new node (keep selected top-level metadata)
    new_node = {
        "type": "section",
        "title": node.get("title"),
        "level": node.get("level"),
        "style": node.get("style"),
        "content": content,
        "children": normalized_children
    }

    return new_node
