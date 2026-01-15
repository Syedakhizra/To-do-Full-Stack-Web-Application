#!/usr/bin/env python3
"""
Debug script to check what routes are actually available in the app
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.main import app

def main():
    print("=== All Routes in the App ===")
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            print(f"{route.methods} {route.path}")
        elif hasattr(route, 'path'):  # Some routes might not have methods attribute
            print(f"N/A {route.path}")

    print("\n=== Auth-related Routes ===")
    for route in app.routes:
        if hasattr(route, 'path') and ('auth' in route.path.lower()):
            methods = getattr(route, 'methods', 'N/A')
            print(f"{methods} {route.path}")

    print("\n=== Login/Register Routes ===")
    for route in app.routes:
        if hasattr(route, 'path') and any(endpoint in route.path for endpoint in ['/login', '/register']):
            methods = getattr(route, 'methods', 'N/A')
            print(f"{methods} {route.path}")

if __name__ == "__main__":
    main()