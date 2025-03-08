from Cryptodome.Cipher import DES3
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes

def generate_3des_key():
    # Generate a 24-byte key (3DES requires a 24-byte key)
    while True:
        key = get_random_bytes(24)
        try:
            # Ensure the key is a valid 3DES key
            DES3.adjust_key_parity(key)
            return key
        except ValueError:
            continue  # Generate a new key if parity adjustment fails

def encrypt_3des(message, key):
    # Create a 3DES cipher object with CBC mode
    cipher = DES3.new(key, DES3.MODE_CBC)
    
    # Pad the message to make it a multiple of 8 bytes (DES block size)
    padded_message = pad(message.encode(), DES3.block_size)
    
    # Encrypt the message
    ciphertext = cipher.encrypt(padded_message)

    # Return IV + ciphertext
    return cipher.iv + ciphertext

def decrypt_3des(ciphertext, key):
    # Extract IV
    iv = ciphertext[:DES3.block_size]
    
    # Create a cipher object
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    
    # Decrypt and unpad the message
    decrypted_message = unpad(cipher.decrypt(ciphertext[DES3.block_size:]), DES3.block_size)
    
    return decrypted_message.decode()

# Example usage
key_3des = generate_3des_key()
message = "Hello, World!"

encrypted_3des = encrypt_3des(message, key_3des)
decrypted_3des = decrypt_3des(encrypted_3des, key_3des)

print("Original message:", message)
print("Encrypted message (3DES):", encrypted_3des)
print("Decrypted message (3DES):", decrypted_3des)
