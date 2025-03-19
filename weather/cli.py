#!/usr/bin/env python3
"""
Weather Service CLI
A command-line interface for the weather service.
"""
import argparse
import asyncio
import sys
from typing import Optional

from . import get_alerts, get_forecast, DEFAULT_LATITUDE, DEFAULT_LONGITUDE

async def main_async(args: argparse.Namespace) -> None:
    """Main async function to handle CLI commands."""
    if args.command == "forecast":
        result = await get_forecast(args.latitude, args.longitude)
        print(result)
    elif args.command == "alerts":
        result = await get_alerts(args.state)
        print(result)

def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Weather Service CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Forecast command
    forecast_parser = subparsers.add_parser("forecast", help="Get weather forecast")
    forecast_parser.add_argument("--latitude", type=float, default=DEFAULT_LATITUDE,
                               help=f"Latitude (-90 to 90, default: {DEFAULT_LATITUDE} [Beijing])")
    forecast_parser.add_argument("--longitude", type=float, default=DEFAULT_LONGITUDE,
                               help=f"Longitude (-180 to 180, default: {DEFAULT_LONGITUDE} [Beijing])")
    
    # Alerts command
    alerts_parser = subparsers.add_parser("alerts", help="Get weather alerts")
    alerts_parser.add_argument("--state", type=str, required=True,
                             help="Two-letter US state code (e.g., CA)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    asyncio.run(main_async(args))

if __name__ == "__main__":
    main() 