#!/usr/bin/env python3
"""
Weather Service Server Runner
Run this script to start the weather service MCP server.
"""
import asyncio
from weather import mcp

if __name__ == "__main__":
    print("Starting Weather Service MCP Server...")
    print("Use another terminal to interact with the service using commands like:")
    print("  mcp call weather get_forecast --latitude 39.9042 --longitude 116.4074")
    print("  mcp call weather get_alerts --state CN-11")
    print("\nPress Ctrl+C to stop the server.")
    
    mcp.run(transport='stdio') 