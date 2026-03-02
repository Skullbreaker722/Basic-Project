import os
from cryptography.fernet import Fernet

class EncryptionEngine:
    """Encryption and decryption logic using AES (Fernet)."""

    def __init__(self, key=None):
        self.key = key if key else self.generate_key()
        self.cipher = Fernet(self.key)

    def generate_key(self):
        """Generates a new AES-CBC/GCM equivalent key."""
        return Fernet.generate_key()

    def encrypt_file(self, file_path):
        """Encrypts a single file and appends .encrypted extension."""
        try:
            with open(file_path, "rb") as file:
                data = file.read()
            
            encrypted_data = self.cipher.encrypt(data)
            
            with open(file_path + ".encrypted", "wb") as file:
                file.write(encrypted_data)
            
            # Delete original file
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Encryption failed for {file_path}: {e}")
            return False

    def decrypt_file(self, encrypted_path):
        """Decrypts an encrypted file and restores the original."""
        try:
            if not encrypted_path.endswith(".encrypted"):
                return False
            
            with open(encrypted_path, "rb") as file:
                encrypted_data = file.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            original_path = encrypted_path.replace(".encrypted", "")
            with open(original_path, "wb") as file:
                file.write(decrypted_data)
            
            # Delete encrypted file
            os.remove(encrypted_path)
            return True
        except Exception as e:
            print(f"Decryption failed for {encrypted_path}: {e}")
            return False
