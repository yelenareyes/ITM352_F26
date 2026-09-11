from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

encoded_text = cipher_suite.encrypt(b"Hello, World!")
print("Encoded text:", encoded_text)
decoded_text = cipher_suite.decrypt(encoded_text)
print("Decoded text:", decoded_text)


