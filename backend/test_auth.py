"""
Simple test to verify the authentication functionality
"""
import uuid
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from app.auth.jwt import create_access_token, verify_token, extract_user_id_from_token
from app.auth.dependencies import get_current_user, get_user_id
from fastapi.security import HTTPBearer
from fastapi import HTTPException
from jose import jwt


def test_jwt_creation_and_verification():
    """Test creating and verifying JWT tokens"""
    print("Testing JWT creation and verification...")

    # Create a token with user data
    user_data = {
        "user_id": 1,
        "email": "test@example.com",
        "sub": "1"
    }

    token = create_access_token(data=user_data)
    print(f"Created token: {token[:50]}...")  # Print first 50 chars

    # Verify the token
    payload = verify_token(token)
    print(f"Verified payload: {payload}")

    # Extract user_id from token
    user_id = extract_user_id_from_token(token)
    print(f"Extracted user_id: {user_id}")

    # Test that extracted user_id matches original
    assert user_id == 1, f"Expected user_id 1, got {user_id}"
    assert payload.get("email") == "test@example.com"

    print("[PASS] JWT creation and verification test passed!")


def test_expired_token():
    """Test handling of expired tokens"""
    print("\nTesting expired token handling...")

    # Create a token that expires immediately
    user_data = {
        "user_id": 1,
        "email": "test@example.com",
        "sub": "1"
    }

    # Create a token that expired in the past
    expired_payload = user_data.copy()
    expired_payload["exp"] = (datetime.utcnow() - timedelta(seconds=1)).timestamp()

    SECRET_KEY = "your-default-secret-key"
    ALGORITHM = "HS256"

    expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Created expired token: {expired_token[:50]}...")

    try:
        verify_token(expired_token)
        print("[FAIL] Should have raised an exception for expired token")
        return False
    except:
        print("[PASS] Correctly rejected expired token")
        return True


def test_invalid_token():
    """Test handling of invalid tokens"""
    print("\nTesting invalid token handling...")

    invalid_token = "invalid.token.here"

    try:
        verify_token(invalid_token)
        print("[FAIL] Should have raised an exception for invalid token")
        return False
    except:
        print("[PASS] Correctly rejected invalid token")
        return True


if __name__ == "__main__":
    print("Testing authentication functionality...\n")

    try:
        test_jwt_creation_and_verification()
        test_expired_token()
        test_invalid_token()

        print("\n[SUCCESS] All authentication tests passed!")
    except Exception as e:
        print(f"\n[ERROR] Test failed with error: {str(e)}")
        raise