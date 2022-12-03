from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings
import jwt


def tokenizeCard(payload):
    try:
        encode = jwt.encode({"data":payload}, settings.PAN_ENCRYPT_KEY, algorithm='HS512')
        return encode
    except Exception as e:
        print("Error occurred while tokenizing")
        print(e)
        return None

def deTokenizeCard(token):
    try:
        decode = jwt.decode(token, settings.PAN_ENCRYPT_KEY, algorithms=['HS512'])
        return decode['data'][0]
    except Exception as e:
        print("Error occurred while decoding card token")
        return None


def encrypt(pan):
    try:        
        pan = str(pan)
        cipher_pan = Fernet(settings.PAN_ENCRYPT_KEY)
        # print(cipher_pan)
        encrypt_pan = cipher_pan.encrypt(pan.encode('ascii'))
        encrypt_pan = base64.urlsafe_b64encode(encrypt_pan).decode("ascii") 
        return encrypt_pan
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


def decrypt(pan):
    try:
        pan = base64.urlsafe_b64decode(pan)
        cipher_pan = Fernet(settings.PAN_ENCRYPT_KEY)
        decod_pan = cipher_pan.decrypt(pan).decode("ascii")     
        return decod_pan
    except Exception as e:
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None