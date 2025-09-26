from cryptography.fernet import Fernet
import secrets

fernet_key = Fernet.generate_key()
print(fernet_key.decode())  # your fernet_key, keep it in secured place!
print(secrets.token_hex(16))