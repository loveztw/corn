import base64

def encrypt(password):
    password_byte = password.encode(encoding="utf-8")
    enpass_byte = base64.encodebytes(password_byte)
    return enpass_byte.decode()
    

def decrypt(enpass):
    enpass_byte = enpass.encode(encoding="utf-8")
    pass_byte = base64.decodebytes(enpass_byte)
    return pass_byte.decode()