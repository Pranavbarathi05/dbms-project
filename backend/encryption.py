from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64
import os

# Generate a key from a password (in production, use environment variable)
# DO NOT hardcode this in production - use environment variables or key management service
ENCRYPTION_PASSWORD = os.getenv("ENCRYPTION_KEY", "change-this-encryption-key-in-production")
SALT = b'hospital_db_salt_2025'  # Use a unique salt, stored securely

def get_encryption_key():
    """Derive encryption key from password"""
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(ENCRYPTION_PASSWORD.encode()))
    return key

# Initialize Fernet cipher
cipher = Fernet(get_encryption_key())

def encrypt_field(plain_text: str) -> str:
    """Encrypt sensitive data"""
    if not plain_text:
        return None
    try:
        encrypted = cipher.encrypt(plain_text.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    except Exception as e:
        print(f"Encryption error: {str(e)}")
        return None

def decrypt_field(encrypted_text: str) -> str:
    """Decrypt sensitive data"""
    if not encrypted_text:
        return None
    try:
        decoded = base64.urlsafe_b64decode(encrypted_text.encode())
        decrypted = cipher.decrypt(decoded)
        return decrypted.decode()
    except Exception as e:
        print(f"Decryption error: {str(e)}")
        return None

def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """Mask sensitive data for display (e.g., phone numbers, SSN)"""
    if not data or len(data) <= visible_chars:
        return "****"
    return "*" * (len(data) - visible_chars) + data[-visible_chars:]

# Example usage:
# encrypted_phone = encrypt_field("555-1234-5678")
# decrypted_phone = decrypt_field(encrypted_phone)
# masked_phone = mask_sensitive_data("555-1234-5678")  # Returns "********5678"
