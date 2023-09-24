import secrets

token = secrets.token_hex(32)  # generates a 32-character long token
print(token)