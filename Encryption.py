from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import base64

# Function to adjust key length to 24 bytes
def adjust_key(key):
    key = key.encode('utf-8')
    while len(key) < 24:
        key += b" "  # Padding if key is too short
    return key[:24]  # Truncate if too long

# PKCS5 Padding
def pad(text):
    pad_len = 8 - (len(text) % 8)
    return text + chr(pad_len) * pad_len

def unpad(text):
    return text[:-ord(text[-1])]

# Encryption function using Triple DES
def encrypt(message, key):
    key = adjust_key(key)  # Ensure key is 24 bytes
    cipher = DES3.new(key, DES3.MODE_CBC, get_random_bytes(8))  # Generate IV
    padded_message = pad(message)
    encrypted_message = cipher.iv + cipher.encrypt(padded_message.encode('utf-8'))
    return base64.b64encode(encrypted_message).decode('utf-8')

# Decryption function using Triple DES
def decrypt(encrypted_message, key):
    key = adjust_key(key)  # Ensure key is 24 bytes
    encrypted_message = base64.b64decode(encrypted_message)
    iv = encrypted_message[:8]  # Extract IV
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    decrypted_message = cipher.decrypt(encrypted_message[8:]).decode('utf-8')
    return unpad(decrypted_message)

# Example usage
message = "Hello, world!"
key = "mysecretkey123456"

# Encryption
encrypted_message = encrypt(message, key)
print("Encrypted message:", encrypted_message)

# Decryption
decrypted_message = decrypt(encrypted_message, key)
print("Decrypted message:", decrypted_message)
"""
# Encryption function
def encrypt(message, key):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            if char.isupper():
                encrypted_char = chr((ord(char) - ord('A') + key) % 26 + ord('A'))
            else:
                encrypted_char = chr((ord(char) - ord('a') + key) % 26 + ord('a'))
            encrypted_message += encrypted_char
        else:
            encrypted_message += char
    return encrypted_message

# Decryption function
def decrypt(encrypted_message, key):
    decrypted_message = ""
    for char in encrypted_message:
        if char.isalpha():
            if char.isupper():
                decrypted_char = chr((ord(char) - ord('A') - key) % 26 + ord('A'))
            else:
                decrypted_char = chr((ord(char) - ord('a') - key) % 26 + ord('a'))
            decrypted_message += decrypted_char
        else:
            decrypted_message += char
    return decrypted_message

# Example usage
message = "Hello, world!"
key = 3

# Encryption
encrypted_message = encrypt(message, key)
print("Encrypted message:", encrypted_message)

# Decryption
decrypted_message = decrypt(encrypted_message, key)
print("Decrypted message:", decrypted_message)
"""