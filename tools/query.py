from mcp.server.fastmcp import FastMCP
from db import db
from security import validate_readonly_query


def register_query_tools(mcp: FastMCP):
    """Register advanced query tools with security validation."""

    @mcp.tool()
    def run_readonly_sql(query: str) -> dict:
        """
        Execute readonly SQL queries against the employee database.

        Security: Only SELECT queries are allowed. No INSERT, UPDATE, DELETE, DROP, or ALTER operations.

        Args:
            query: SQL SELECT query

        Returns:
            List of result dictionaries
        """
        # Validate query safety
        is_safe, error_msg = validate_readonly_query(query)
        if not is_safe:
            return {"error": error_msg}

        try:
            rows = db.execute_query(query)

            # Get column names from query execution
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            cols = [d[0] for d in cursor.description]
            conn.close()

            # Convert to list of dictionaries
            results = [dict(zip(cols, row)) for row in rows]
            return {"success": True, "count": len(results), "data": results}
        except Exception as e:
            return {"error": f"Query execution failed: {str(e)}"}
