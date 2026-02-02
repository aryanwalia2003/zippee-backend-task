import base64

def encode_cursor(id):
    """
    Encode an ID into a base64 cursor string.
    """
    if not id: return None
    return base64.b64encode(str(id).encode('ascii')).decode('ascii')

def decode_cursor(cursor):
    """
    Decode a base64 cursor string back into an integer ID.
    """
    if not cursor: return None
    try:
        return int(base64.b64decode(cursor.encode('ascii')).decode('ascii'))
    except:
        return None
