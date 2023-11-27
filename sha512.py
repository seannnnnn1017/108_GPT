import hashlib

def sha512(input):
    hash = hashlib.sha512( str( input ).encode("utf-8") ).hexdigest()
    return hash


