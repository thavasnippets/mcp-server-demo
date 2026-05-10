"""
Security utilities for MCP server.
Validates queries to prevent dangerous operations.
"""

FORBIDDEN_KEYWORDS = [
    "drop",
    "delete",
    "update",
    "insert",
    "alter",
    "truncate",
    "replace",
    "create",
    "attach",
    "detach"
]


def validate_readonly_query(query: str) -> tuple[bool, str]:
    """
    Validate that a query is safe to execute (read-only).

    Returns:
        Tuple of (is_safe, error_message)
    """
    query_lower = query.lower().strip()

    # Check for forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in query_lower:
            return False, f"Forbidden operation: {keyword.upper()} is not allowed"

    # Check if query starts with SELECT
    if not query_lower.startswith("select"):
        return False, "Only SELECT queries are allowed"

    return True, ""
