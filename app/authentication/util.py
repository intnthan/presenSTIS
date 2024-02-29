import os
import hashlib
import binascii
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()

def hash_pass(password):
    """Hash a password for storing."""
    
    hashed = bcrypt.generate_password_hash(password)
    return hashed.decode('utf-8')

    # salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    # pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
    #                               salt, 100000)
    # pwdhash = binascii.hexlify(pwdhash)
    # return (salt + pwdhash)  # return bytes


def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""

    # stored_password = stored_password.decode('ascii')
    # salt = stored_password[:64]
    # stored_password = stored_password[64:]
    # pwdhash = hashlib.pbkdf2_hmac('sha512',
    #                               provided_password.encode('utf-8'),
    #                               salt.encode('ascii'),
    #                               100000)
    # pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    # print(pwdhash)
    pwdhash = hash_pass(provided_password)
    print (pwdhash)
    return pwdhash == stored_password
