import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def new(uinp):
    password = uinp.encode() # Convert to type bytes
    salt=os.urandom(256)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    file = open('key.key', 'wb')
    file.write(key)
    file.close()
    return True

def decrypt(name,orgi):
    file = open(name, 'rb')
    filedata = file.read()
    file.close()
    file2 = open('key.key', 'rb')
    key2 = file2.read()
    file2.close()
    ff = Fernet(key2)
    decrpd = ff.decrypt(filedata)
    with open(orgi, 'wb') as fd:
        fd.write(decrpd)
    os.remove(name)


def encrypt(name,namepath):
    file1 = open('key.key', 'rb')
    key = file1.read()
    print("Key opened")
    file1.close()
    file2 = open(namepath, 'rb')
    filedata = file2.read()
    print("file opened")
    file2.close()
    f = Fernet(key)
    encrpd = f.encrypt(filedata)
    with open('{}.bcpt'.format(name), 'wb') as f:
        f.write(encrpd)
        print("Encrypted")