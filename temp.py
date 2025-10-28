def convert_json_to_raptor_format(node):
    """
    Converts a deeply nested DOCX-parsed JSON node into RAPTOR-compatible format.

    RAPTOR expects each node to have:
      - 'title': heading/title of the section
      - 'content': text content (may be raw_text, text, or empty string)
      - 'children': list of similarly structured child nodes

    This function:
      - Recursively walks the tree
      - Does NOT join paragraphs
      - Does NOT include paragraph lists, metadata, or type fields
      - Handles any node that has 'children' (not just type=='section')
    """

    # --- local content ---
    # Prefer node’s own raw_text/text, fallback to empty string
    content = node.get("raw_text") or node.get("text") or ""

    # --- recursively process children ---
    children = node.get("children", []) or []
    normalized_children = []
    for child in children:
        # if this node itself has nested items, process recursively
        if child.get("children"):
            normalized_children.append(convert_json_to_raptor_format(child))

    # --- build RAPTOR node ---
    new_node = {
        "title": node.get("title"),
        "content": content,
        "children": normalized_children
    }

    return new_node
