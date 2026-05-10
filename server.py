import os
from mcp.server.fastmcp import FastMCP

# Import tool modules
from tools.employees import register_employee_tools
from tools.department import register_department_tools
from tools.swipe import register_swipe_tools
from tools.education import register_education_tools
from tools.query import register_query_tools

# Host/port (ONLY for your reference or external server wrapper)
HOST = os.getenv("MCP_HOST", "0.0.0.0")
PORT = int(os.getenv("MCP_PORT", "8000"))

# Initialize FastMCP server with configured host/port for HTTP transport
mcp = FastMCP(
    "HR Database Assistant",
    host=HOST,
    port=PORT,
)

# Register tools
register_employee_tools(mcp)
register_department_tools(mcp)
register_swipe_tools(mcp)
register_education_tools(mcp)
register_query_tools(mcp)

if __name__ == "__main__":
    print(
        f"Starting MCP server on http://{HOST}:{PORT}{mcp.settings.streamable_http_path}"
    )

    mcp.run(transport="streamable-http")
